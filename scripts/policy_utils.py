#!/usr/bin/env python3
"""Shared policy helpers for profile-gated docs scripts."""

from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]

TEXT_SUFFIXES = {
    ".json",
    ".md",
    ".py",
    ".sbatch",
    ".sh",
    ".toml",
    ".txt",
    ".yaml",
    ".yml",
}


def load_policy(path: Path) -> dict:
    payload = json.loads(path.read_text(encoding="utf-8"))
    validate_policy(payload)
    return payload


def validate_policy(policy: dict) -> None:
    if not isinstance(policy, dict):
        raise ValueError("policy must be a JSON object")
    if "profiles" not in policy:
        raise ValueError("policy missing required key: profiles")
    profiles = policy["profiles"]
    if not isinstance(profiles, dict):
        raise ValueError("policy.profiles must be an object")
    for name in ("internal", "public"):
        if name not in profiles:
            raise ValueError(f"policy.profiles missing required profile: {name}")
        profile = profiles[name]
        if not isinstance(profile, dict):
            raise ValueError(f"policy.profiles.{name} must be an object")
        if "deny_filename_patterns" not in profile:
            raise ValueError(f"policy.profiles.{name} missing deny_filename_patterns")
        if not isinstance(profile["deny_filename_patterns"], list):
            raise ValueError(
                f"policy.profiles.{name}.deny_filename_patterns must be a list"
            )
        if "allow_restricted_content" not in profile:
            raise ValueError(f"policy.profiles.{name} missing allow_restricted_content")
    if "restricted_content_rules" not in policy:
        raise ValueError("policy missing required key: restricted_content_rules")
    if not isinstance(policy["restricted_content_rules"], list):
        raise ValueError("policy.restricted_content_rules must be a list")
    if "public_variant_sources" not in policy:
        raise ValueError("policy missing required key: public_variant_sources")
    if "public_variant_replacements" not in policy:
        raise ValueError("policy missing required key: public_variant_replacements")


def compile_patterns(
    patterns: list[str], errors: list[str] | None = None
) -> list[re.Pattern[str]]:
    compiled: list[re.Pattern[str]] = []
    for pattern in patterns:
        try:
            compiled.append(re.compile(pattern))
        except re.error as exc:
            message = f"invalid regex pattern {pattern!r}: {exc}"
            if errors is not None:
                errors.append(message)
            else:
                raise ValueError(message) from exc
    return compiled


def compile_content_rules(
    rules: list, errors: list[str] | None = None
) -> list[tuple[str, re.Pattern[str]]]:
    compiled: list[tuple[str, re.Pattern[str]]] = []
    for rule in rules:
        if not isinstance(rule, dict):
            message = f"content rule is not an object: {rule!r}"
            if errors is not None:
                errors.append(message)
                continue
            raise ValueError(message)
        name = str(rule.get("name", "unnamed-rule"))
        pattern = str(rule.get("pattern", ""))
        if not pattern:
            message = f"content rule {name!r} has empty pattern"
            if errors is not None:
                errors.append(message)
                continue
            raise ValueError(message)
        try:
            compiled.append((name, re.compile(pattern)))
        except re.error as exc:
            message = f"invalid regex in content rule {name!r}: {exc}"
            if errors is not None:
                errors.append(message)
            else:
                raise ValueError(message) from exc
    return compiled


def relative_display(path: Path) -> str:
    try:
        return str(path.relative_to(REPO_ROOT))
    except ValueError:
        return str(path)


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def collect_text_files(root: Path) -> list[Path]:
    if root.is_file():
        if root.suffix.lower() in TEXT_SUFFIXES:
            return [root]
        return []
    files: list[Path] = []
    for path in sorted(root.rglob("*"), key=lambda p: str(p).lower()):
        if not path.is_file() or path.is_symlink():
            continue
        if path.suffix.lower() in TEXT_SUFFIXES:
            files.append(path)
    return files


def read_text_safe(path: Path, warnings: list[str] | None = None) -> str:
    raw = path.read_bytes()
    try:
        return raw.decode("utf-8")
    except UnicodeDecodeError:
        if warnings is not None:
            warnings.append(
                f"{relative_display(path)}: not valid UTF-8; restricted content may be missed"
            )
        return raw.decode("utf-8", errors="replace")
