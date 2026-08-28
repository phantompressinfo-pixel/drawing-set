"""Building-code Q&A backend for the Eigelberger office assistant.

Deployed as a Google Cloud Function (2nd gen) or Cloud Run service. Reads
the building code text out of knowledge/building-code/, answers with
Claude Sonnet 5 first, and escalates to Claude Opus 5 only when Sonnet
itself flags the question as needing deeper reasoning (cross-referencing
sections, resolving a conflict) rather than a direct lookup. This keeps
the common case cheap without giving up quality on the hard cases.

This backend answers ONLY building-code questions from
knowledge/building-code/ - it does not touch the office-standards/
contracts Google Drive folder. That's a separate, later integration.
"""

import json
import logging
import os
from pathlib import Path
from typing import Optional

import anthropic
import functions_framework
from flask import Request, jsonify
from pydantic import BaseModel, Field

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

KNOWLEDGE_DIR = Path(__file__).resolve().parent.parent / "knowledge" / "building-code"
SONNET_MODEL = "claude-sonnet-5"
OPUS_MODEL = "claude-opus-5"

# Lock this down to the office's actual Google Sites origin before going
# live - "*" is only for local testing.
ALLOWED_ORIGIN = os.environ.get("ALLOWED_ORIGIN", "*")

SYSTEM_INSTRUCTIONS = """You are the building-code assistant for Eigelberger Architecture & Design, answering non-technical office staff (not architects or code officials).

Rules:
- Answer ONLY using the building code text provided below. Never use general training knowledge about building codes - codes are jurisdiction- and edition-specific, and a plausible-sounding guess here is a liability problem, not just an inconvenience.
- If the provided text doesn't cover the question, say so plainly in "answer" (e.g. "That's not covered by the documents loaded yet - ask a licensed architect") and leave "sources" empty. Do not guess.
- Keep "answer" short: the direct answer first, then one or two sentences of "why" only if it's not obvious. Plain English, no unexplained jargon, no essay.
- Always name which document (and section/page, if visible) the answer came from in "sources".
- Whenever the question touches code compliance, safety, or anything that would end up on a stamped drawing, end "answer" with a one-line reminder that this is a starting point for a licensed architect to verify, never a substitute for one. Skip that line only for a pure definitional question with no compliance decision attached.
- Set "escalate" to true only when answering genuinely requires cross-referencing multiple sections, resolving an apparent conflict between sections, or a judgment call beyond a direct lookup - not just because the topic sounds complex. Most questions should NOT escalate.
"""


class CodeAnswer(BaseModel):
    answer: str = Field(description="The plain-English answer for the staff member.")
    sources: list[str] = Field(description="Document names / sections the answer came from. Empty if not found in the documents.")
    escalate: bool = Field(description="True only if this question needs deeper reasoning than a direct lookup.")


def load_code_text() -> str:
    """Concatenate all building code documents into one block for the prompt cache.

    Only .txt/.md files are read directly - a PDF needs to be converted to
    text first (see backend/README.md) since this backend does no
    PDF parsing itself.
    """
    if not KNOWLEDGE_DIR.exists():
        return ""
    parts = []
    for path in sorted(KNOWLEDGE_DIR.glob("*.txt")) + sorted(KNOWLEDGE_DIR.glob("*.md")):
        if path.name.lower() == "readme.md":
            continue
        parts.append(f"=== {path.name} ===\n{path.read_text(encoding='utf-8', errors='ignore')}")
    return "\n\n".join(parts)


def build_system_block(code_text: str) -> list[dict]:
    """One cached block: instructions + all code text share a single cache_control breakpoint.

    Every staff member's question shares this same prefix, so the whole
    office rides on one cache entry - the point of the exercise. Any byte
    changed here (including load_code_text() output) invalidates it, so
    this stays static between document updates.
    """
    if not code_text:
        code_text = "(No building code documents have been loaded into knowledge/building-code/ yet.)"
    combined = f"{SYSTEM_INSTRUCTIONS}\n\nBUILDING CODE DOCUMENTS:\n\n{code_text}"
    return [{"type": "text", "text": combined, "cache_control": {"type": "ephemeral", "ttl": "1h"}}]


def ask(client: anthropic.Anthropic, model: str, system_blocks: list[dict], question: str):
    response = client.messages.parse(
        model=model,
        max_tokens=1024,
        system=system_blocks,
        messages=[{"role": "user", "content": question}],
        output_format=CodeAnswer,
    )
    return response.parsed_output, response


def _cors_headers() -> dict:
    return {"Access-Control-Allow-Origin": ALLOWED_ORIGIN}


def _cors_preflight():
    headers = {
        **_cors_headers(),
        "Access-Control-Allow-Methods": "POST, OPTIONS",
        "Access-Control-Allow-Headers": "Content-Type",
        "Access-Control-Max-Age": "3600",
    }
    return "", 204, headers


@functions_framework.http
def building_code_qa(request: Request):
    if request.method == "OPTIONS":
        return _cors_preflight()

    body = request.get_json(silent=True) or {}
    question = (body.get("question") or "").strip()
    if not question:
        return jsonify({"error": "Missing 'question'."}), 400, _cors_headers()

    client = anthropic.Anthropic()  # reads ANTHROPIC_API_KEY from the environment
    code_text = load_code_text()
    system_blocks = build_system_block(code_text)

    parsed, response = ask(client, SONNET_MODEL, system_blocks, question)
    model_used = SONNET_MODEL

    if parsed.escalate:
        logger.info("Escalating to Opus 5: %r", question)
        parsed, response = ask(client, OPUS_MODEL, system_blocks, question)
        model_used = OPUS_MODEL

    logger.info(
        "model=%s cache_read=%s cache_write=%s input=%s output=%s",
        model_used,
        response.usage.cache_read_input_tokens,
        response.usage.cache_creation_input_tokens,
        response.usage.input_tokens,
        response.usage.output_tokens,
    )

    return jsonify(
        {
            "answer": parsed.answer,
            "sources": parsed.sources,
            "model_used": model_used,
        }
    ), 200, _cors_headers()
