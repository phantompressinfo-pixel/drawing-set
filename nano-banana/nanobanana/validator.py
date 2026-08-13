"""Checks a generated prompt against the template's own quality checklist.

Errors mean the prompt is structurally wrong and should be regenerated.
Warnings mean it is usable but thin.
"""

from __future__ import annotations

import re
import sqlite3
from dataclasses import dataclass, field
from typing import Any

from . import db, seed_data


@dataclass
class Report:
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)

    @property
    def ok(self) -> bool:
        return not self.errors

    def __str__(self) -> str:
        lines = [f"ERROR   {e}" for e in self.errors]
        lines += [f"WARN    {w}" for w in self.warnings]
        return "\n".join(lines) or "OK      all checks passed"


def _dig(body: dict[str, Any], path: str) -> Any:
    node: Any = body
    for step in path.split("."):
        if not isinstance(node, dict) or step not in node:
            return None
        node = node[step]
    return node


def _text_of(node: Any) -> str:
    """Flatten any nested value into one searchable string."""
    if isinstance(node, str):
        return node
    if isinstance(node, dict):
        return " ".join(_text_of(v) for v in node.values())
    if isinstance(node, (list, tuple)):
        return " ".join(_text_of(v) for v in node)
    return "" if node is None else str(node)


def validate(body: dict[str, Any], conn: sqlite3.Connection) -> Report:
    report = Report()

    if not isinstance(body, dict):
        report.errors.append("prompt is not a JSON object")
        return report

    expected = db.sections(conn)
    for section in expected:
        value = _dig(body, section["json_path"])
        if value is None:
            report.errors.append(f"missing section `{section['json_path']}`")
        elif value in ("", {}, []):
            report.errors.append(f"section `{section['json_path']}` is empty")

    known = {s["key"] for s in expected} | {"_commentary"}
    for key in body:
        if key not in known:
            report.warnings.append(f"unexpected top-level key `{key}`")

    _check_quality_keywords(body, report)
    _check_mood(body, report)
    _check_materials(body, report)
    _check_lighting(body, report)
    _check_filler(body, report)

    return report


def _check_quality_keywords(body: dict[str, Any], report: Report) -> None:
    qk = body.get("quality_keywords")
    if not isinstance(qk, dict):
        return
    for key in ("include", "avoid", "reference"):
        if key not in qk:
            report.errors.append(f"quality_keywords.{key} is missing")
    for key in ("include", "avoid"):
        value = qk.get(key)
        if value is not None and not isinstance(value, list):
            report.errors.append(f"quality_keywords.{key} must be an array")
    baseline = {t for b, t in seed_data.QUALITY_KEYWORDS if b == "avoid"}
    avoid = qk.get("avoid")
    if isinstance(avoid, list):
        missing = baseline - {str(t).lower() for t in avoid}
        # Only the four the template calls mandatory.
        mandatory = missing & {
            "digital artifacts",
            "oversaturated colors",
            "unrealistic proportions",
            "flat lighting",
        }
        if mandatory:
            report.warnings.append(
                "quality_keywords.avoid is missing baseline terms: "
                + ", ".join(sorted(mandatory))
            )


def _check_mood(body: dict[str, Any], report: Report) -> None:
    mood = _dig(body, "composition_controls.mood")
    if mood is None:
        report.errors.append("composition_controls.mood is missing")
        return
    words = [w for w in re.split(r"[,\s]+", _text_of(mood).strip()) if w]
    if not 3 <= len(words) <= 6:
        report.warnings.append(
            f"composition_controls.mood should be 3-5 descriptive words, got {len(words)}"
        )


def _check_materials(body: dict[str, Any], report: Report) -> None:
    materials = body.get("material_properties")
    if not isinstance(materials, dict):
        return
    described = [
        k
        for k, v in materials.items()
        if _text_of(v).strip().lower() not in ("", "none", "n/a", "neutral")
    ]
    if len(described) < 3:
        report.warnings.append(
            f"only {len(described)} material surface(s) described; the template asks for 3+"
        )


def _check_lighting(body: dict[str, Any], report: Report) -> None:
    lighting = _text_of(_dig(body, "style_definition.lighting")).lower()
    if not lighting:
        report.errors.append("style_definition.lighting is missing")
        return
    temperature = ("warm", "cool", "neutral", "golden", "tungsten", "daylight", "cold")
    if not any(word in lighting for word in temperature):
        report.warnings.append(
            "style_definition.lighting does not state a colour temperature"
        )
    direction = (
        "back", "side", "front", "top", "overhead", "directional",
        "ambient", "diffused", "rim", "recessed", "above", "window",
    )
    if not any(word in lighting for word in direction):
        report.warnings.append("style_definition.lighting does not state a direction")


def _check_filler(body: dict[str, Any], report: Report) -> None:
    sections = {k: v for k, v in body.items() if k != "_commentary"}
    haystack = _text_of(sections).lower()
    hits = sorted(
        {w for w in seed_data.FILLER_WORDS if re.search(rf"\b{re.escape(w)}\b", haystack)}
    )
    if hits:
        report.warnings.append("generic filler words present: " + ", ".join(hits))
