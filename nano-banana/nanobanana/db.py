"""SQLite access layer for the Nano Banana prompt database."""

from __future__ import annotations

import hashlib
import json
import os
import sqlite3
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable

from . import seed_data

SCHEMA_PATH = Path(__file__).with_name("schema.sql")
DEFAULT_DB = Path(os.environ.get("NANO_BANANA_DB", "prompts.db"))


def connect(path: Path | str | None = None) -> sqlite3.Connection:
    db_path = Path(path) if path else DEFAULT_DB
    db_path.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def init(conn: sqlite3.Connection, *, reseed: bool = False) -> None:
    """Create the schema and load the template. Safe to run repeatedly."""
    conn.executescript(SCHEMA_PATH.read_text())
    if reseed:
        conn.executescript(
            "DELETE FROM fields; DELETE FROM sections;"
            "DELETE FROM vocabulary; DELETE FROM quality_keywords;"
        )
    _seed(conn)
    conn.commit()


def _seed(conn: sqlite3.Connection) -> None:
    conn.executemany(
        "INSERT OR REPLACE INTO sections (key, ordinal, json_path, description)"
        " VALUES (?, ?, ?, ?)",
        seed_data.SECTIONS,
    )
    section_ids = {
        row["key"]: row["id"] for row in conn.execute("SELECT id, key FROM sections")
    }
    conn.executemany(
        "INSERT OR REPLACE INTO fields (section_id, key, guidance, examples)"
        " VALUES (?, ?, ?, ?)",
        [
            (section_ids[section], key, guidance, examples)
            for section, key, guidance, examples in seed_data.FIELDS
        ],
    )
    conn.executemany(
        "INSERT OR REPLACE INTO vocabulary (kind, trigger, value) VALUES (?, ?, ?)",
        seed_data.VOCABULARY,
    )
    conn.executemany(
        "INSERT OR REPLACE INTO quality_keywords (bucket, term) VALUES (?, ?)",
        seed_data.QUALITY_KEYWORDS,
    )


# --- template reads -------------------------------------------------------


def sections(conn: sqlite3.Connection) -> list[sqlite3.Row]:
    return list(conn.execute("SELECT * FROM sections ORDER BY ordinal"))


def fields_for(conn: sqlite3.Connection, section_id: int) -> list[sqlite3.Row]:
    return list(
        conn.execute("SELECT * FROM fields WHERE section_id = ? ORDER BY id", (section_id,))
    )


def vocabulary(conn: sqlite3.Connection, kind: str | None = None) -> list[sqlite3.Row]:
    if kind:
        return list(
            conn.execute(
                "SELECT * FROM vocabulary WHERE kind = ? ORDER BY trigger", (kind,)
            )
        )
    return list(conn.execute("SELECT * FROM vocabulary ORDER BY kind, trigger"))


def quality_terms(conn: sqlite3.Connection, bucket: str) -> list[str]:
    return [
        row["term"]
        for row in conn.execute(
            "SELECT term FROM quality_keywords WHERE bucket = ? ORDER BY id", (bucket,)
        )
    ]


# --- prompt writes/reads --------------------------------------------------


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def save_prompt(
    conn: sqlite3.Connection,
    *,
    body: dict[str, Any],
    model: str,
    source_path: str | None = None,
    image_sha: str | None = None,
    note: str | None = None,
    commentary: str | None = None,
) -> int:
    composition = body.get("composition_controls") or {}
    mood = composition.get("mood") if isinstance(composition, dict) else None
    reference = (body.get("quality_keywords") or {}).get("reference")
    cur = conn.execute(
        "INSERT INTO prompts"
        " (created_at, source_path, image_sha256, model, scene_type, mood, note, body, commentary)"
        " VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
        (
            datetime.now(timezone.utc).isoformat(timespec="seconds"),
            source_path,
            image_sha,
            model,
            reference if isinstance(reference, str) else None,
            mood if isinstance(mood, str) else None,
            note,
            json.dumps(body, indent=2, ensure_ascii=False),
            commentary,
        ),
    )
    conn.commit()
    return int(cur.lastrowid)


def get_prompt(conn: sqlite3.Connection, prompt_id: int) -> sqlite3.Row | None:
    return conn.execute("SELECT * FROM prompts WHERE id = ?", (prompt_id,)).fetchone()


def list_prompts(conn: sqlite3.Connection, limit: int = 20) -> list[sqlite3.Row]:
    return list(
        conn.execute(
            "SELECT * FROM prompts ORDER BY datetime(created_at) DESC, id DESC LIMIT ?",
            (limit,),
        )
    )


def search_prompts(conn: sqlite3.Connection, term: str, limit: int = 20) -> list[sqlite3.Row]:
    like = f"%{term}%"
    return list(
        conn.execute(
            "SELECT * FROM prompts"
            " WHERE body LIKE ? OR mood LIKE ? OR note LIKE ? OR source_path LIKE ?"
            " ORDER BY id DESC LIMIT ?",
            (like, like, like, like, limit),
        )
    )


def save_render(
    conn: sqlite3.Connection, *, prompt_id: int, model: str, output_path: str
) -> int:
    cur = conn.execute(
        "INSERT INTO renders (prompt_id, created_at, model, output_path) VALUES (?, ?, ?, ?)",
        (
            prompt_id,
            datetime.now(timezone.utc).isoformat(timespec="seconds"),
            model,
            output_path,
        ),
    )
    conn.commit()
    return int(cur.lastrowid)


def renders_for(conn: sqlite3.Connection, prompt_id: int) -> list[sqlite3.Row]:
    return list(
        conn.execute("SELECT * FROM renders WHERE prompt_id = ? ORDER BY id", (prompt_id,))
    )


def export(conn: sqlite3.Connection, rows: Iterable[sqlite3.Row]) -> str:
    """JSONL export — one prompt per line."""
    lines = []
    for row in rows:
        lines.append(
            json.dumps(
                {
                    "id": row["id"],
                    "created_at": row["created_at"],
                    "source_path": row["source_path"],
                    "model": row["model"],
                    "mood": row["mood"],
                    "note": row["note"],
                    "commentary": row["commentary"],
                    "prompt": json.loads(row["body"]),
                },
                ensure_ascii=False,
            )
        )
    return "\n".join(lines)
