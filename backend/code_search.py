"""Search helpers for the Building Code Assistant backend.

These wrap the domain logic already built into the Claude Code skills so
the backend and Claude Code stay in sync instead of drifting into two
copies of the same rules:

- Model code (IBC/IRC/IEBC/ADA) search reuses
  .claude/skills/us-building-codes/scripts/codesearch.py directly - same
  corpus walk, same amendment/DPO flagging. A hit here means the same
  thing it would from that script's command line.
- Aspen/Pitkin local code search is a plain regex grep over
  code-library/aspen/ and code-library/pitkin/, per
  .claude/skills/aspen-pitkin-code/SKILL.md's own instructions ("search
  these files with Grep").
"""

import csv
import importlib.util
import os
import re
from pathlib import Path
from typing import Optional

def _find_repo_root() -> Path:
    """Locate the directory containing code-library/ and .claude/.

    In a normal checkout that's the repo root, one level above this file
    (backend/code_search.py). In a Cloud Functions deploy bundle built by
    prepare_deploy.sh, code-library/ and .claude/ are copied as siblings
    of this file instead (Cloud Functions requires main.py, and whatever
    it imports, at the top of --source), so check that layout too rather
    than hardcoding one. CODE_ASSISTANT_ROOT overrides both if set.
    """
    override = os.environ.get("CODE_ASSISTANT_ROOT")
    if override:
        return Path(override).resolve()
    here = Path(__file__).resolve().parent
    for candidate in (here, here.parent):
        if (candidate / "code-library").is_dir():
            return candidate
    return here.parent  # dev-repo layout, even if code-library/ isn't populated yet


REPO_ROOT = _find_repo_root()
CODE_LIBRARY = REPO_ROOT / "code-library"

csv.field_size_limit(10_000_000)


def _load_codesearch_module():
    path = REPO_ROOT / ".claude" / "skills" / "us-building-codes" / "scripts" / "codesearch.py"
    spec = importlib.util.spec_from_file_location("codesearch", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


_codesearch = _load_codesearch_module()


class _Filters:
    """Duck-types the argparse.Namespace codesearch.matches() expects."""

    def __init__(self, section, category, responsibility, occupancy, ifc_type, phase):
        self.section = section
        self.category = category
        self.responsibility = responsibility
        self.occupancy = occupancy
        self.ifc_type = ifc_type
        self.phase = phase


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
    """Search the model building code dataset (IBC/IRC/IEBC/ADA text as adopted
    by Colorado and GSA). Returns hits with amendment/DPO flags already
    resolved - treat those flags as authoritative, not as something to
    double check yourself.
    """
    filters = _Filters(section, category, responsibility, occupancy, ifc_type, phase)
    pattern = re.compile(query, re.IGNORECASE) if query else None
    amended = _codesearch.load_amended()
    dpo = _codesearch.load_dpo()

    hits = []
    total = 0
    blind = [0]
    for path, juris, edition in _codesearch.corpus(jurisdiction, code, chapter):
        chapter_name = os.path.basename(path)[:-4]
        with open(path, newline="", encoding="utf-8") as fh:
            for row in csv.DictReader(fh):
                if not _codesearch.matches(row, filters, pattern, blind):
                    continue
                total += 1
                if len(hits) >= limit:
                    continue
                sec_id = (row.get("id") or "").strip()
                body = (row.get("body") or "").strip()
                key = (edition.split("-")[0].lower(), sec_id.lower())
                who = amended.get(key)
                kind = dpo.get(key)
                hits.append(
                    {
                        "jurisdiction": juris,
                        "edition": edition,
                        "chapter": chapter_name,
                        "section": sec_id,
                        "title": row.get("title", ""),
                        "body": body[:1500],
                        "superseded_locally_by": who,
                        "not_icc_model_text_colorado_amended": kind,
                    }
                )
    return {"total_matches": total, "shown": len(hits), "hits": hits}


_LOCAL_DIRS = {"aspen": CODE_LIBRARY / "aspen", "pitkin": CODE_LIBRARY / "pitkin"}


def search_local_code(
    query: str,
    jurisdiction: Optional[str] = None,
    context_lines: int = 3,
    limit: int = 10,
) -> dict:
    """Grep the City of Aspen Municipal Code and/or Pitkin County Code / Land
    Use Code text for a query. jurisdiction: "aspen", "pitkin", or omit to
    search both.
    """
    pattern = re.compile(query, re.IGNORECASE)
    dirs = [_LOCAL_DIRS[jurisdiction]] if jurisdiction in _LOCAL_DIRS else list(_LOCAL_DIRS.values())

    hits = []
    for d in dirs:
        if not d.exists():
            continue
        for path in sorted(d.glob("*.txt")):
            lines = path.read_text(encoding="utf-8", errors="ignore").splitlines()
            for i, line in enumerate(lines):
                if len(hits) >= limit:
                    break
                if not pattern.search(line):
                    continue
                start = max(0, i - context_lines)
                end = min(len(lines), i + context_lines + 1)
                hits.append(
                    {
                        "jurisdiction": d.name,
                        "file": path.name,
                        "line": i + 1,
                        "excerpt": "\n".join(lines[start:end]),
                    }
                )
            if len(hits) >= limit:
                break
        if len(hits) >= limit:
            break
    return {"shown": len(hits), "hits": hits}
