#!/usr/bin/env python3
"""
Scan profile artifacts for restricted filename and content patterns.

Examples:
  python3 scripts/security_policy_check.py --profile public
  python3 scripts/security_policy_check.py --profile public --path docs/derived/public
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from policy_utils import (
    collect_text_files,
    compile_content_rules,
    compile_patterns,
    load_policy,
    read_text_safe,
    relative_display,
)

REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_POLICY = REPO_ROOT / "config" / "data_policy.json"

# Files that DEFINE the policy patterns (the policy JSON, the scanner itself,
# and its helper module) are exempt from content scanning. A pattern like
# `(?i)PACE\s*-\s*GT\s*Login` is expected to appear in data_policy.json — it
# is the rule, not a leak. Scanning these would always self-match.
POLICY_TOOLING_BASENAMES = frozenset({
    "data_policy.json",
    "security_policy_check.py",
    "policy_utils.py",
})

DEFAULT_PUBLIC_PATHS = (
    REPO_ROOT / "docs" / "derived" / "public",
    REPO_ROOT / "codex" / "references" / "public",
    REPO_ROOT / "dist" / "public",
)
DEFAULT_INTERNAL_PATHS = (
    REPO_ROOT / "docs" / "PACE Documentation",
    REPO_ROOT / "codex" / "references",
)


def default_scan_paths(profile: str) -> list[Path]:
    if profile == "internal":
        return [path for path in DEFAULT_INTERNAL_PATHS if path.exists()]
    return [path for path in DEFAULT_PUBLIC_PATHS if path.exists()]


def normalize_paths(raw_paths: list[str] | None, profile: str) -> tuple[list[Path], list[str]]:
    if not raw_paths:
        return default_scan_paths(profile), []

    normalized: list[Path] = []
    missing: list[str] = []
    for raw in raw_paths:
        path = Path(raw).expanduser()
        if not path.is_absolute():
            path = (Path.cwd() / path).resolve(strict=False)
        if path.exists():
            normalized.append(path)
        else:
            missing.append(str(path))
    return normalized, missing


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Scan profile artifacts for restricted markers")
    parser.add_argument("--profile", choices=("internal", "public"), default="public")
    parser.add_argument(
        "--policy-config",
        default=str(DEFAULT_POLICY),
        help="Path to data policy config JSON",
    )
    parser.add_argument(
        "--path",
        action="append",
        help="Path to scan (repeatable). If omitted, profile defaults are used.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    policy = load_policy(Path(args.policy_config).expanduser().resolve())
    profile_config = policy.get("profiles", {}).get(args.profile)
    if not isinstance(profile_config, dict):
        print(f"Missing profile config in policy file: {args.profile}")
        return 1

    allow_restricted = bool(profile_config.get("allow_restricted_content", False))
    errors: list[str] = []
    deny_patterns = compile_patterns(profile_config.get("deny_filename_patterns", []), errors=errors)
    content_rules = compile_content_rules(policy.get("restricted_content_rules", []), errors=errors)
    for error in errors:
        print(f"WARNING: {error}")

    scan_paths, missing_paths = normalize_paths(args.path, args.profile)
    for missing in missing_paths:
        print(f"WARNING: scan path not found: {missing}")
    if not scan_paths:
        print(
            "FAIL: no scan paths found for the selected profile. "
            "Generate profile artifacts first or pass --path."
        )
        return 1

    violations: list[str] = []
    warnings: list[str] = []
    scanned = 0
    for root in scan_paths:
        for file_path in collect_text_files(root):
            if file_path.name in POLICY_TOOLING_BASENAMES:
                continue
            scanned += 1
            display = relative_display(file_path)
            for pattern in deny_patterns:
                if pattern.search(file_path.name):
                    violations.append(
                        f"{display}: filename matches restricted rule `{pattern.pattern}`"
                    )
            text = read_text_safe(file_path, warnings=warnings)
            for line_no, line in enumerate(text.splitlines(), start=1):
                for name, pattern in content_rules:
                    if pattern.search(line):
                        violations.append(
                            f"{display}:{line_no}: content matches `{name}` ({pattern.pattern})"
                        )

    print(f"Profile: {args.profile}")
    print(f"Scanned files: {scanned}")
    if warnings:
        for warning in warnings:
            print(f"WARNING: {warning}")

    if not violations:
        print("PASS: no restricted matches found")
        return 0

    for violation in violations:
        print(f"VIOLATION: {violation}")

    if allow_restricted:
        print("PASS: restricted matches are allowed for this profile")
        return 0

    print("FAIL: restricted matches are not allowed for this profile")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
