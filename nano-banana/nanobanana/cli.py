"""Command line entry point.

    python -m nanobanana init
    python -m nanobanana generate photo.jpg
    python -m nanobanana render 3 -o out.png
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from . import db, gemini, instruction, validator


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="nanobanana",
        description="Nano Banana JSON prompt generator, backed by SQLite.",
    )
    parser.add_argument("--db", type=Path, default=None, help="database path (default prompts.db)")
    sub = parser.add_subparsers(dest="command", required=True)

    p = sub.add_parser("init", help="create the database and load the template")
    p.add_argument("--reseed", action="store_true", help="reset template rows to defaults")

    p = sub.add_parser("instruction", help="print the system instruction (paste into a Gem)")
    p.add_argument("-o", "--out", type=Path, help="write to a file instead of stdout")

    p = sub.add_parser("generate", help="turn an image into a JSON prompt")
    p.add_argument("image", type=Path)
    p.add_argument("-d", "--direction", help="extra steer for this image")
    p.add_argument("-n", "--note", help="note stored alongside the prompt")
    p.add_argument("-m", "--model", default=gemini.TEXT_MODEL)
    p.add_argument("-t", "--temperature", type=float, default=0.6)
    p.add_argument("--no-save", action="store_true", help="print only, do not store")

    p = sub.add_parser("render", help="generate an image from a stored prompt")
    p.add_argument("prompt_id", type=int)
    p.add_argument("-o", "--out", type=Path, default=None)
    p.add_argument("-m", "--model", default=gemini.IMAGE_MODEL)
    p.add_argument("--reference", type=Path, help="also pass an image as visual reference")

    p = sub.add_parser("list", help="list stored prompts")
    p.add_argument("-n", "--limit", type=int, default=20)
    p.add_argument("-s", "--search", help="filter by text")

    p = sub.add_parser("show", help="print one stored prompt")
    p.add_argument("prompt_id", type=int)

    p = sub.add_parser("validate", help="check a JSON prompt file against the checklist")
    p.add_argument("path", type=Path, help="'-' to read stdin")

    p = sub.add_parser("vocab", help="list the vocabulary table")
    p.add_argument("kind", nargs="?", choices=["lighting", "mood", "reference"])

    p = sub.add_parser("export", help="export stored prompts as JSONL")
    p.add_argument("-o", "--out", type=Path)
    p.add_argument("-n", "--limit", type=int, default=1000)

    args = parser.parse_args(argv)
    conn = db.connect(args.db)
    try:
        if args.command != "init":
            _require_initialised(conn)
        return _dispatch(args, conn)
    except gemini.GeminiError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1
    finally:
        conn.close()


def _require_initialised(conn) -> None:
    row = conn.execute(
        "SELECT name FROM sqlite_master WHERE type='table' AND name='sections'"
    ).fetchone()
    if not row:
        print("error: database not initialised. Run: python -m nanobanana init", file=sys.stderr)
        raise SystemExit(1)


def _dispatch(args, conn) -> int:
    handler = {
        "init": _cmd_init,
        "instruction": _cmd_instruction,
        "generate": _cmd_generate,
        "render": _cmd_render,
        "list": _cmd_list,
        "show": _cmd_show,
        "validate": _cmd_validate,
        "vocab": _cmd_vocab,
        "export": _cmd_export,
    }[args.command]
    return handler(args, conn)


def _cmd_init(args, conn) -> int:
    db.init(conn, reseed=args.reseed)
    counts = {
        table: conn.execute(f"SELECT count(*) FROM {table}").fetchone()[0]
        for table in ("sections", "fields", "vocabulary", "quality_keywords", "prompts")
    }
    print(f"database ready at {args.db or db.DEFAULT_DB}")
    print(", ".join(f"{k}: {v}" for k, v in counts.items()))
    return 0


def _cmd_instruction(args, conn) -> int:
    text = instruction.build(conn)
    if args.out:
        args.out.write_text(text)
        print(f"wrote {args.out} ({len(text)} chars)")
    else:
        print(text)
    return 0


def _cmd_generate(args, conn) -> int:
    if not args.image.is_file():
        print(f"error: no such image: {args.image}", file=sys.stderr)
        return 1

    data, mime = gemini.read_image(args.image)
    body = gemini.generate_prompt(
        image_bytes=data,
        mime_type=mime,
        system_instruction=instruction.build(conn),
        extra_direction=args.direction,
        model=args.model,
        temperature=args.temperature,
    )
    commentary = body.pop("_commentary", None)

    report = validator.validate(body, conn)
    print(json.dumps(body, indent=2, ensure_ascii=False))
    if commentary:
        print(f"\n{commentary}")
    print(f"\n{report}", file=sys.stderr)

    if args.no_save:
        return 0 if report.ok else 2

    prompt_id = db.save_prompt(
        conn,
        body=body,
        model=args.model,
        source_path=str(args.image),
        image_sha=db.sha256(data),
        note=args.note,
        commentary=commentary if isinstance(commentary, str) else None,
    )
    print(f"saved as prompt {prompt_id}", file=sys.stderr)
    return 0 if report.ok else 2


def _cmd_render(args, conn) -> int:
    row = db.get_prompt(conn, args.prompt_id)
    if not row:
        print(f"error: no prompt with id {args.prompt_id}", file=sys.stderr)
        return 1

    out = args.out or Path(f"renders/prompt-{args.prompt_id}.png")
    reference = gemini.read_image(args.reference) if args.reference else None
    path = gemini.render_image(
        prompt_body=json.loads(row["body"]),
        output_path=out,
        model=args.model,
        reference_image=reference,
    )
    db.save_render(conn, prompt_id=args.prompt_id, model=args.model, output_path=str(path))
    print(f"wrote {path}")
    return 0


def _cmd_list(args, conn) -> int:
    rows = (
        db.search_prompts(conn, args.search, args.limit)
        if args.search
        else db.list_prompts(conn, args.limit)
    )
    if not rows:
        print("no prompts stored yet")
        return 0
    for row in rows:
        source = Path(row["source_path"]).name if row["source_path"] else "-"
        renders = len(db.renders_for(conn, row["id"]))
        line = f"{row['id']:>4}  {row['created_at']}  {source:<28} {row['mood'] or '-'}"
        if renders:
            line += f"  [{renders} render{'s' if renders > 1 else ''}]"
        print(line)
    return 0


def _cmd_show(args, conn) -> int:
    row = db.get_prompt(conn, args.prompt_id)
    if not row:
        print(f"error: no prompt with id {args.prompt_id}", file=sys.stderr)
        return 1
    print(row["body"])
    if row["commentary"]:
        print(f"\n{row['commentary']}")
    for render in db.renders_for(conn, row["id"]):
        print(f"\nrender: {render['output_path']} ({render['model']})")
    return 0


def _cmd_validate(args, conn) -> int:
    raw = sys.stdin.read() if str(args.path) == "-" else args.path.read_text()
    try:
        body = json.loads(raw)
    except json.JSONDecodeError as exc:
        print(f"ERROR   not valid JSON: {exc}")
        return 1
    body.pop("_commentary", None)
    report = validator.validate(body, conn)
    print(report)
    return 0 if report.ok else 2


def _cmd_vocab(args, conn) -> int:
    for row in db.vocabulary(conn, args.kind):
        print(f"{row['kind']:<10} {row['trigger']:<28} {row['value']}")
    return 0


def _cmd_export(args, conn) -> int:
    text = db.export(conn, db.list_prompts(conn, args.limit))
    if args.out:
        args.out.write_text(text + "\n" if text else "")
        print(f"wrote {args.out}")
    else:
        print(text)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
