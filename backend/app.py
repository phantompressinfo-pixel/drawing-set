"""Building-code Q&A backend for the Eigelberger office assistant.

Deployed as a Google Cloud Function (2nd gen) or Cloud Run service.
Answers using Claude with two search tools over code-library/ (model
codes in code-library/us-building-codes/, and the City of Aspen /
Pitkin County code text in code-library/aspen/ and code-library/pitkin/)
instead of stuffing the whole library into context - code-library/ is far
too large for that; targeted search is both cheaper and how a person
would actually answer these questions.

Claude Sonnet 5 handles every question first, running its own search
loop. It can call escalate_to_expert_review instead of answering when a
question needs real cross-referencing or judgment rather than a direct
lookup; when it does, the question is re-run from scratch on Claude
Opus 5 with a fresh search loop.

This backend answers ONLY building-code questions - it does not touch
the office-standards/contracts Google Drive folder. That's a separate,
later integration.
"""

import logging
import os
from typing import Optional

import anthropic
import functions_framework
from anthropic import beta_tool
from flask import Request, jsonify

import code_search

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

SONNET_MODEL = "claude-sonnet-5"
OPUS_MODEL = "claude-opus-5"

# Lock this down to the office's actual Google Sites origin before going
# live - "*" is only for local testing.
ALLOWED_ORIGIN = os.environ.get("ALLOWED_ORIGIN", "*")

SYSTEM_INSTRUCTIONS = """You are the building-code assistant for Eigelberger Architecture & Design, answering non-technical office staff (not architects or code officials).

You have two search tools over the office's stored code library - use them, never answer from memory:
- search_model_codes: the model code text (IBC/IRC/IEBC, ADA standards) as adopted by Colorado and GSA.
- search_local_code: the City of Aspen Municipal Code and Pitkin County Code / Land Use Code.

Critical rule specific to this library: Aspen and Pitkin County both amend a
number of IBC/IRC sections locally, and Colorado's own adopted text already
diverges from the ICC model in places. search_model_codes results carry two
flags for this:
- "superseded_locally_by": the model text in this result is NOT current - a
  local jurisdiction amends this section. Before answering, call
  search_local_code for that jurisdiction and quote ITS text as the actual
  requirement, and say explicitly that the model code text is superseded.
- "not_icc_model_text_colorado_amended": Colorado has already modified this
  section away from the ICC model text, but Aspen/Pitkin still adopt the ICC
  version - so this stored row is not what applies to an Aspen/Pitkin
  project. Say so plainly rather than presenting it as the requirement.
Never present flagged text as the current requirement without surfacing the flag.

General rules:
- Answer ONLY from what your searches return. If nothing relevant turns up, say so plainly and suggest asking a licensed architect - do not fill the gap from general training knowledge about codes.
- Keep the answer short: the direct answer first, one or two sentences of "why" only if useful. Plain English, no unexplained jargon, no essay.
- Always name what you're citing: jurisdiction, document/edition, and section/title (e.g. "Aspen Municipal Code Title 8" or "Colorado IBC 2021 Section 1015.2").
- Whenever the question touches code compliance, safety, or anything that would end up on a stamped drawing, end with one line: this is a starting point for a licensed architect to verify, never a substitute for one. Skip that line only for a pure definitional question with no compliance decision attached.
- If the parcel's jurisdiction (City of Aspen vs. unincorporated Pitkin County) isn't given and it changes the answer, ask rather than guessing.

If a question genuinely requires cross-referencing multiple sections, resolving a conflict between them, or a judgment call beyond a direct lookup - not just because the topic sounds complex - call escalate_to_expert_review instead of answering yourself, then stop.
"""


def _build_tools(escalation: dict):
    @beta_tool
    def search_model_codes(
        query: Optional[str] = None,
        jurisdiction: Optional[str] = None,
        code: Optional[str] = None,
        chapter: Optional[int] = None,
        section: Optional[str] = None,
        category: Optional[str] = None,
        responsibility: Optional[str] = None,
        occupancy: Optional[str] = None,
        ifc_type: Optional[str] = None,
        phase: Optional[str] = None,
        limit: int = 15,
    ) -> dict:
        """Search the model building code dataset: IBC, IRC, IEBC, and the ADA standards.

        Args:
            query: regex searched over section id, title, and body. Omit to filter by metadata only.
            jurisdiction: "colorado", "gsa", or "ada".
            code: "ibc", "irc", or "iebc".
            chapter: chapter number.
            section: exact section id, e.g. "1015.2".
            category: code_category, e.g. "means_of_egress".
            responsibility: e.g. "architect", "structural_engineer".
            occupancy: e.g. "Residential (R)" or just "R".
            ifc_type: e.g. "Stair", "Guard", "Wall".
            phase: "concept", "sd", "dd", "cd", or "ca".
            limit: max hits to return (default 15).
        """
        return code_search.search_model_codes(
            query=query,
            jurisdiction=jurisdiction,
            code=code,
            chapter=chapter,
            section=section,
            category=category,
            responsibility=responsibility,
            occupancy=occupancy,
            ifc_type=ifc_type,
            phase=phase,
            limit=limit,
        )

    @beta_tool
    def search_local_code(query: str, jurisdiction: Optional[str] = None, limit: int = 10) -> dict:
        """Search the City of Aspen Municipal Code and Pitkin County Code / Land Use Code text.

        Args:
            query: regex searched over the code text.
            jurisdiction: "aspen", "pitkin", or omit to search both.
            limit: max hits to return (default 10).
        """
        return code_search.search_local_code(query, jurisdiction=jurisdiction, limit=limit)

    @beta_tool
    def escalate_to_expert_review(reason: str) -> str:
        """Flag that this question needs deeper review on a stronger model instead of a direct answer.

        Only call this for genuine cross-referencing/judgment calls, not because
        a topic sounds complex. After calling this, stop - do not attempt your
        own answer.

        Args:
            reason: why this question needs deeper reasoning.
        """
        escalation["flag"] = True
        escalation["reason"] = reason
        return "Noted - this question will be re-run for deeper review."

    return [search_model_codes, search_local_code, escalate_to_expert_review]


def run_agent(client: anthropic.Anthropic, model: str, question: str):
    """Runs the search/answer loop once on the given model.

    Returns (answer_text, escalated, escalation_reason, tool_log).
    """
    escalation = {"flag": False, "reason": None}
    tools = _build_tools(escalation)

    runner = client.beta.messages.tool_runner(
        model=model,
        max_tokens=4096,
        system=[{"type": "text", "text": SYSTEM_INSTRUCTIONS, "cache_control": {"type": "ephemeral"}}],
        tools=tools,
        messages=[{"role": "user", "content": question}],
    )

    tool_log = []
    last = None
    for message in runner:
        last = message
        for block in message.content:
            if block.type == "tool_use":
                tool_log.append({"tool": block.name, "input": block.input})

    answer_text = "".join(b.text for b in last.content if b.type == "text") if last else ""
    return answer_text, escalation["flag"], escalation["reason"], tool_log


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

    answer, escalated, reason, tool_log = run_agent(client, SONNET_MODEL, question)
    model_used = SONNET_MODEL

    if escalated:
        logger.info("Escalating to Opus 5: %r (reason: %s)", question, reason)
        answer, _, _, opus_tool_log = run_agent(client, OPUS_MODEL, question)
        model_used = OPUS_MODEL
        tool_log += opus_tool_log

    logger.info("model=%s tool_calls=%s", model_used, [t["tool"] for t in tool_log])

    return (
        jsonify(
            {
                "answer": answer,
                "model_used": model_used,
                "searches_run": len(tool_log),
            }
        ),
        200,
        _cors_headers(),
    )
