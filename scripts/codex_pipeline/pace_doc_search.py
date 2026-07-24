#!/usr/bin/env python3
"""
Search and navigate local PACE markdown docs.

Examples:
  uv run python scripts/pace_doc_search.py list
  uv run python scripts/pace_doc_search.py list --cluster all
  uv run python scripts/pace_doc_search.py find "pace-quota qos account" --cluster phoenix
  uv run python scripts/pace_doc_search.py headings --doc "Using Slurm on ICE"
  uv run python scripts/pace_doc_search.py show --doc 3 --start 120 --end 220
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, Optional

from pace_doc_common import HEADING_RE, detect_cluster, is_noise


@dataclass
class Doc:
    index: int
    path: Path
    title: str
    cluster: str
    canonical: bool = True
    duplicate_of: Optional[str] = None
    quality_score: int = 0


def repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def codex_root() -> Path:
    # References live at codex/references/. The script is dev tooling under
    # scripts/codex_pipeline/, so we resolve via repo_root().
    return repo_root() / "codex"


def docs_root(profile: str) -> Path:
    if profile == "internal":
        return repo_root() / "docs" / "PACE Documentation"
    return repo_root() / "docs" / "derived" / profile / "PACE Documentation"


def missing_docs_message(profile: str, docs_dir: Path) -> str:
    if profile == "public":
        return (
            f"Public docs are not available under: {docs_dir}. "
            "Run `python3 scripts/build_doc_views.py --profile public --delete` first."
        )
    return f"No markdown docs found under: {docs_dir}"


def index_json_path(profile: str) -> Path:
    references = codex_root() / "references"
    profiled = references / profile / "doc-index.json"
    if profiled.exists():
        return profiled

    if profile == "internal":
        legacy = references / "doc-index.json"
        if legacy.exists():
            return legacy

    return profiled


def display_path(path: Path) -> str:
    candidates = (
        repo_root(),
        codex_root(),
    )
    for base in candidates:
        try:
            return str(path.relative_to(base))
        except ValueError:
            continue
    return str(path)


def safe_read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        print(f"WARNING: {path.name} is not valid UTF-8, using latin-1 fallback", file=sys.stderr)
        return path.read_text(encoding="latin-1")


def read_title(path: Path) -> str:
    for line in safe_read_text(path).splitlines():
        if HEADING_RE.match(line):
            return re.sub(r"^\s*#+\s*", "", line).strip()
    return path.stem


def load_index_metadata(profile: str) -> dict[str, dict]:
    idx = index_json_path(profile)
    if not idx.exists():
        return {}
    try:
        payload = json.loads(idx.read_text(encoding="utf-8"))
    except Exception:
        return {}
    items = payload.get("items", [])
    if not isinstance(items, list):
        return {}
    metadata: dict[str, dict] = {}
    for item in items:
        if isinstance(item, dict) and "filename" in item:
            metadata[str(item["filename"])] = item
    return metadata


def load_docs(profile: str) -> list[Doc]:
    root = docs_root(profile)
    files = sorted(root.glob("*.md"), key=lambda p: p.name.lower())
    metadata = load_index_metadata(profile)
    docs = []
    for idx, path in enumerate(files, start=1):
        meta = metadata.get(path.name, {})
        docs.append(
            Doc(
                index=idx,
                path=path,
                title=read_title(path),
                cluster=detect_cluster(path.name),
                canonical=bool(meta.get("canonical", True)),
                duplicate_of=meta.get("duplicate_of"),
                quality_score=int(meta.get("quality_score", 0)),
            )
        )
    return docs


def filter_docs(docs: Iterable[Doc], cluster: str) -> list[Doc]:
    if cluster == "all":
        return list(docs)
    return [doc for doc in docs if doc.cluster == cluster]


def resolve_doc(docs: list[Doc], selector: str) -> Doc:
    selector = selector.strip()
    if selector.isdigit():
        target = int(selector)
        for doc in docs:
            if doc.index == target:
                return doc
        raise ValueError(f"Document index {target} not found.")

    matches = []
    lower = selector.lower()
    for doc in docs:
        if lower in doc.path.name.lower() or lower in doc.title.lower():
            matches.append(doc)

    if not matches:
        raise ValueError(f"No document matched '{selector}'.")
    if len(matches) > 1:
        preview = ", ".join(f"{doc.index}:{doc.path.name}" for doc in matches[:5])
        raise ValueError(f"Multiple documents matched '{selector}': {preview}")
    return matches[0]


def cmd_list(args: argparse.Namespace, docs: list[Doc]) -> int:
    selected = filter_docs(docs, args.cluster)
    if not args.include_duplicates:
        selected = [doc for doc in selected if doc.canonical]
    if not selected:
        print("No documents found for the selected filter.")
        return 0
    selected.sort(key=lambda doc: (-doc.quality_score, doc.path.name.lower()))
    for doc in selected:
        rel = display_path(doc.path)
        print(f"{doc.index:>2}  [{doc.cluster}]  [score {doc.quality_score:>2}]  {doc.title}")
        if doc.duplicate_of:
            print(f"    duplicate_of: {doc.duplicate_of}")
        if args.paths:
            print(f"    {rel}")
    return 0


def cmd_headings(args: argparse.Namespace, docs: list[Doc]) -> int:
    if not args.doc:
        selected = filter_docs(docs, args.cluster)
        if not args.include_duplicates:
            selected = [doc for doc in selected if doc.canonical]
    else:
        selected = [resolve_doc(docs, args.doc)]

    for doc in selected:
        rel = display_path(doc.path)
        print(f"\n== {doc.index}: {doc.title} ({rel}) ==")
        for line_no, line in enumerate(safe_read_text(doc.path).splitlines(), start=1):
            if HEADING_RE.match(line):
                heading = re.sub(r"^\s*#+\s*", "", line).strip()
                print(f"{line_no:>4}: {heading}")
    return 0


def line_matches(query: str, text: str, mode: str) -> bool:
    terms = [term for term in query.lower().split() if term]
    lower = text.lower()
    if not terms:
        return False
    if mode == "phrase":
        return query.lower() in lower
    if mode == "all":
        return all(term in lower for term in terms)
    return any(term in lower for term in terms)


def cmd_find(args: argparse.Namespace, docs: list[Doc]) -> int:
    selected = filter_docs(docs, args.cluster)
    if not args.include_duplicates:
        selected = [doc for doc in selected if doc.canonical]
    if args.doc:
        selected = [resolve_doc(selected, args.doc)]

    hits = 0
    for doc in selected:
        lines = safe_read_text(doc.path).splitlines()
        current_heading = "(top)"
        for line_no, raw_line in enumerate(lines, start=1):
            line = raw_line.strip()
            if HEADING_RE.match(raw_line):
                current_heading = re.sub(r"^\s*#+\s*", "", raw_line).strip()
            if is_noise(raw_line):
                continue
            if line_matches(args.query, raw_line, args.mode):
                rel = display_path(doc.path)
                print(f"{rel}:{line_no} [{current_heading}]")
                print(f"  {line}")
                hits += 1
                if hits >= args.max:
                    return 0

    if hits == 0:
        print("No matches found.")
    return 0


def cmd_show(args: argparse.Namespace, docs: list[Doc]) -> int:
    doc = resolve_doc(docs, args.doc)
    lines = safe_read_text(doc.path).splitlines()

    start = max(args.start, 1)
    end = min(args.end, len(lines))
    if start > end:
        raise ValueError("--start must be <= --end.")

    rel = display_path(doc.path)
    print(f"== {doc.index}: {doc.title} ({rel}) lines {start}-{end} ==")
    for line_no in range(start, end + 1):
        line = lines[line_no - 1]
        if args.clean and is_noise(line):
            continue
        print(f"{line_no:>4}: {line}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Search local PACE documentation")
    parser.add_argument(
        "--profile",
        choices=("internal", "public"),
        default="internal",
        help="Profile docs scope (default: internal)",
    )
    sub = parser.add_subparsers(dest="command", required=True)

    list_parser = sub.add_parser("list", help="List available documents (default: phoenix)")
    list_parser.add_argument("--cluster", choices=("all", "phoenix", "ice", "common"), default="phoenix")
    list_parser.add_argument("--paths", action="store_true", help="Print relative file paths")
    list_parser.add_argument("--include-duplicates", action="store_true", help="Include duplicate docs")

    headings_parser = sub.add_parser("headings", help="Show headings for one or more docs")
    headings_parser.add_argument("--cluster", choices=("all", "phoenix", "ice", "common"), default="phoenix")
    headings_parser.add_argument("--doc", help="Doc index or substring match")
    headings_parser.add_argument("--include-duplicates", action="store_true", help="Include duplicate docs")

    find_parser = sub.add_parser("find", help="Find matching lines in docs")
    find_parser.add_argument("query", help="Search string")
    find_parser.add_argument("--cluster", choices=("all", "phoenix", "ice", "common"), default="phoenix")
    find_parser.add_argument("--doc", help="Restrict search to one doc (index or substring)")
    find_parser.add_argument("--mode", choices=("any", "all", "phrase"), default="all")
    find_parser.add_argument("--include-duplicates", action="store_true", help="Include duplicate docs")
    find_parser.add_argument("--max", type=int, default=20, help="Maximum hits to print")

    show_parser = sub.add_parser("show", help="Show a range of lines from one doc")
    show_parser.add_argument("--doc", required=True, help="Doc index or substring match")
    show_parser.add_argument("--start", type=int, default=1)
    show_parser.add_argument("--end", type=int, default=120)
    show_parser.add_argument("--clean", action="store_true", help="Hide known noise lines")

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    docs_dir = docs_root(args.profile)
    docs = load_docs(args.profile)
    if not docs:
        print(missing_docs_message(args.profile, docs_dir), file=sys.stderr)
        return 1

    try:
        if args.command == "list":
            return cmd_list(args, docs)
        if args.command == "headings":
            return cmd_headings(args, docs)
        if args.command == "find":
            return cmd_find(args, docs)
        if args.command == "show":
            return cmd_show(args, docs)
    except ValueError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
