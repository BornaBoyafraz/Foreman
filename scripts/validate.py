#!/usr/bin/env python3
"""Validate the Foreman plugin: manifests parse, and every skill/agent/command
has the frontmatter Claude Code needs to discover it. No third-party deps.

Usage:  python3 scripts/validate.py
Exit 0 = OK, exit 1 = problems found (printed).
"""
from __future__ import annotations
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
errors: list[str] = []
checked = 0


def err(msg: str) -> None:
    errors.append(msg)


def load_json(rel: str) -> dict | None:
    p = ROOT / rel
    if not p.exists():
        err(f"missing file: {rel}")
        return None
    try:
        return json.loads(p.read_text())
    except json.JSONDecodeError as e:
        err(f"invalid JSON in {rel}: {e}")
        return None


def frontmatter(path: Path) -> dict[str, str] | None:
    """Parse a minimal `key: value` YAML frontmatter block. Returns None if absent."""
    text = path.read_text()
    if not text.startswith("---"):
        return None
    end = text.find("\n---", 3)
    if end == -1:
        return None
    block = text[3:end].strip().splitlines()
    fm: dict[str, str] = {}
    for line in block:
        if ":" in line and not line.lstrip().startswith("#"):
            key, _, val = line.partition(":")
            fm[key.strip()] = val.strip()
    return fm


# 1. plugin.json
plugin = load_json(".claude-plugin/plugin.json")
if plugin:
    checked += 1
    for field in ("name", "version", "description"):
        if not plugin.get(field):
            err(f"plugin.json missing required field: {field}")

# 2. marketplace.json
market = load_json(".claude-plugin/marketplace.json")
if market:
    checked += 1
    if not market.get("plugins"):
        err("marketplace.json has no plugins[]")

# 3. skills / agents / commands frontmatter
for kind, glob, required in (
    ("skill", "skills/*/SKILL.md", ("name", "description")),
    ("agent", "agents/*.md", ("name", "description")),
    ("command", "commands/*.md", ("description",)),
):
    for path in sorted(ROOT.glob(glob)):
        checked += 1
        fm = frontmatter(path)
        rel = path.relative_to(ROOT)
        if fm is None:
            err(f"{kind} {rel}: missing frontmatter block")
            continue
        for field in required:
            if not fm.get(field):
                err(f"{kind} {rel}: missing frontmatter field '{field}'")

# 4. hooks.json (optional but must be valid if present)
if (ROOT / "hooks/hooks.json").exists():
    load_json("hooks/hooks.json")
    checked += 1

if errors:
    print(f"FAIL — {len(errors)} problem(s) across {checked} checked item(s):")
    for e in errors:
        print(f"  - {e}")
    sys.exit(1)

print(f"OK — {checked} item(s) validated, no problems.")
