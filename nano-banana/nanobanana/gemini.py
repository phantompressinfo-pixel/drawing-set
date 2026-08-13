"""Gemini API calls: image -> JSON prompt, and JSON prompt -> image.

The SDK is imported lazily so the rest of the CLI (init, instruction, validate,
list, export) works with no dependencies installed and no API key set.
"""

from __future__ import annotations

import json
import mimetypes
import os
import re
from pathlib import Path
from typing import Any

# Overridable so you can point at a newer model without touching code.
TEXT_MODEL = os.environ.get("NANO_BANANA_TEXT_MODEL", "gemini-2.5-flash")
IMAGE_MODEL = os.environ.get("NANO_BANANA_IMAGE_MODEL", "gemini-2.5-flash-image")


class GeminiError(RuntimeError):
    pass


def _sdk():
    try:
        from google import genai
        from google.genai import types
    except ImportError as exc:  # pragma: no cover - depends on install
        raise GeminiError(
            "google-genai is not installed. Run: pip install -r requirements.txt"
        ) from exc
    return genai, types


_CLIENT = None


def _client():
    """Cached. A Client that goes out of scope closes its own HTTP transport,
    which kills any call still in flight on it."""
    global _CLIENT
    if _CLIENT is None:
        genai, _ = _sdk()
        key = os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY")
        if not key:
            raise GeminiError(
                "Set GEMINI_API_KEY (get one at https://aistudio.google.com/apikey)"
            )
        _CLIENT = genai.Client(api_key=key)
    return _CLIENT


def _types():
    return _sdk()[1]


def _call(**kwargs):
    """generate_content with API errors flattened into GeminiError."""
    from google.genai import errors

    try:
        return _client().models.generate_content(**kwargs)
    except errors.APIError as exc:
        message = getattr(exc, "message", None) or str(exc)
        raise GeminiError(f"{kwargs.get('model')}: {message}") from exc


def read_image(path: Path) -> tuple[bytes, str]:
    data = path.read_bytes()
    mime = mimetypes.guess_type(path.name)[0] or "image/jpeg"
    if not mime.startswith("image/"):
        raise GeminiError(f"{path} does not look like an image ({mime})")
    return data, mime


def generate_prompt(
    *,
    image_bytes: bytes,
    mime_type: str,
    system_instruction: str,
    extra_direction: str | None = None,
    model: str = TEXT_MODEL,
    temperature: float = 0.6,
) -> dict[str, Any]:
    """Send the image to Gemini and get the 7-section prompt back."""
    types = _types()
    ask = "Write the Nano Banana JSON prompt for this image."
    if extra_direction:
        ask += f"\n\nAdditional direction from the user: {extra_direction}"

    response = _call(
        model=model,
        contents=[
            types.Part.from_bytes(data=image_bytes, mime_type=mime_type),
            ask,
        ],
        config=types.GenerateContentConfig(
            system_instruction=system_instruction,
            response_mime_type="application/json",
            temperature=temperature,
        ),
    )
    text = (response.text or "").strip()
    if not text:
        raise GeminiError(f"empty response from {model}")
    return _parse_json(text)


def _parse_json(text: str) -> dict[str, Any]:
    """response_mime_type should give us clean JSON; fall back if it doesn't."""
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        pass
    fenced = re.search(r"```(?:json)?\s*(.+?)```", text, re.S)
    candidate = fenced.group(1) if fenced else text[text.find("{") : text.rfind("}") + 1]
    try:
        return json.loads(candidate)
    except json.JSONDecodeError as exc:
        raise GeminiError(f"model did not return valid JSON: {exc}") from exc


def render_image(
    *,
    prompt_body: dict[str, Any],
    output_path: Path,
    model: str = IMAGE_MODEL,
    reference_image: tuple[bytes, str] | None = None,
) -> Path:
    """Feed a stored prompt to the image model and write the result to disk."""
    types = _types()
    body = {k: v for k, v in prompt_body.items() if k != "_commentary"}
    contents: list[Any] = []
    if reference_image:
        data, mime = reference_image
        contents.append(types.Part.from_bytes(data=data, mime_type=mime))
    contents.append(
        "Generate an image matching this specification exactly:\n\n"
        + json.dumps(body, indent=2, ensure_ascii=False)
    )

    response = _call(model=model, contents=contents)

    candidates = getattr(response, "candidates", None) or []
    for candidate in candidates:
        for part in getattr(candidate.content, "parts", None) or []:
            inline = getattr(part, "inline_data", None)
            if inline and inline.data:
                output_path.parent.mkdir(parents=True, exist_ok=True)
                output_path.write_bytes(inline.data)
                return output_path

    reason = getattr(candidates[0], "finish_reason", None) if candidates else None
    raise GeminiError(
        f"{model} returned no image"
        + (f" (finish_reason={reason})" if reason else "")
        + ". The prompt may have been blocked, or the model name may be wrong for your key."
    )
