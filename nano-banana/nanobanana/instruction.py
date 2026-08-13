"""Builds the Gemini system instruction out of the template stored in the database.

Edit a row in `sections`, `fields`, `vocabulary` or `quality_keywords` and the
instruction changes on the next run — no code edit needed. The same text is what
you paste into a Gemini Gem or AI Studio if you'd rather not run the API.
"""

from __future__ import annotations

import json
import sqlite3

from . import db

HEADER = """You generate structured JSON image prompts using the Gemini Nano Banana template.

Given an image, produce a prompt detailed enough to recreate that image's mood,
materials, lighting and composition in an AI image generator. You are describing
what is actually in front of you — not inventing a new scene."""

OUTPUT_RULES = """## Output rules

1. Output only valid JSON. No markdown fences, no preamble, no trailing commas.
2. Every section above must be present. If a section does not apply, use "none"
   or "neutral" as its value — never omit the key.
3. Prefer nested objects over flat strings for complex sections. For example,
   material_properties.surfaces may itself be an object with named keys.
4. Double quotes throughout. Single quotes break JSON parsers.
5. Put your 1-2 sentence read of the image in the "_commentary" key at the top
   level: what the emotional core of the image is, and what you emphasised
   (lighting choice, composition decision, mood vocabulary). This is the only
   key permitted outside the template sections.

## Before you answer, check

- All sections present, including technical_specifications.physics_accuracy
- Lighting described with temperature, quality and direction
- At least 3 specific material surfaces described
- composition_controls.mood is 3-5 words
- quality_keywords.reference matches the image's editorial benchmark
- No filler: never "beautiful", "nice lighting", "stunning" or similar"""


def build(conn: sqlite3.Connection) -> str:
    parts = [HEADER, "", _template_block(conn), "", _section_guide(conn), ""]
    parts.append(_vocabulary_block(conn))
    parts.append("")
    parts.append(_quality_block(conn))
    parts.append("")
    parts.append(OUTPUT_RULES)
    return "\n".join(parts)


def _template_block(conn: sqlite3.Connection) -> str:
    """The literal shape of the expected output."""
    skeleton: dict[str, object] = {}
    for section in db.sections(conn):
        keys = [f["key"] for f in db.fields_for(conn, section["id"])]
        path = section["json_path"].split(".")
        target = skeleton
        for step in path[:-1]:
            target = target.setdefault(step, {})  # type: ignore[assignment]
        leaf = {k: "..." for k in keys}
        if isinstance(target.get(path[-1]), dict):
            target[path[-1]].update(leaf)  # type: ignore[union-attr]
        else:
            target[path[-1]] = leaf
    return "## Required shape\n\n```json\n" + json.dumps(skeleton, indent=2) + "\n```"


def _section_guide(conn: sqlite3.Connection) -> str:
    lines = ["## Section guide", ""]
    for section in db.sections(conn):
        lines.append(f"### {section['ordinal']}. `{section['json_path']}`")
        lines.append(section["description"])
        lines.append("")
        for field in db.fields_for(conn, section["id"]):
            entry = f"- `{field['key']}` — {field['guidance']}"
            if field["examples"]:
                entry += f" e.g. {field['examples']}"
            lines.append(entry)
        lines.append("")
    return "\n".join(lines).rstrip()


def _vocabulary_block(conn: sqlite3.Connection) -> str:
    lines = ["## Vocabulary", ""]
    labels = {
        "lighting": "Lighting — match the light in the image, then use this phrasing",
        "mood": "Mood — for composition_controls.mood, when the scene matches",
        "reference": "Reference benchmarks — for quality_keywords.reference",
    }
    for kind, label in labels.items():
        rows = db.vocabulary(conn, kind)
        if not rows:
            continue
        lines.append(f"**{label}:**")
        for row in rows:
            lines.append(f"- {row['trigger']} → `{row['value']}`")
        lines.append("")
    lines.append(
        "These are starting points, not a closed set. If the image does not match "
        "any entry, write something equally specific."
    )
    return "\n".join(lines)


def _quality_block(conn: sqlite3.Connection) -> str:
    include = db.quality_terms(conn, "include")
    avoid = db.quality_terms(conn, "avoid")
    return (
        "## Quality keyword defaults\n\n"
        f"Baseline `include`: {json.dumps(include)}\n"
        f"Baseline `avoid`: {json.dumps(avoid)}\n\n"
        "Start from these and add whatever the specific image needs."
    )
