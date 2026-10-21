#!/usr/bin/env python3
"""Check that both plugin marketplaces resolve to the same packaged skill."""

import json
import re
from pathlib import Path


root = Path(__file__).resolve().parents[1]
codex = json.loads((root / ".codex-plugin/plugin.json").read_text())
claude = json.loads((root / ".claude-plugin/plugin.json").read_text())
for field in ("name", "version", "description", "author", "repository", "license"):
    assert codex[field] == claude[field], f"Plugin manifests disagree: {field}"
assert codex["name"] == "build-novel"
assert re.fullmatch(r"\d+\.\d+\.\d+", codex["version"])

skill = root / codex["skills"] / codex["name"]
entrypoint = skill / "SKILL.md"
assert entrypoint.is_file(), "Codex skills path does not resolve"
frontmatter = entrypoint.read_text().split("---", 2)[1]
assert "name: build-novel\n" in frontmatter
assert re.search(r"^description: .+", frontmatter, re.MULTILINE)
assert (root / "skills/build-novel").resolve() == skill.resolve()

for filename in (".agents/plugins/marketplace.json", ".claude-plugin/marketplace.json"):
    market = json.loads((root / filename).read_text())
    assert market["name"] == "build-novel"
    assert len(market["plugins"]) == 1
    plugin = market["plugins"][0]
    assert plugin["name"] == codex["name"]
    source = plugin["source"]
    path = source["path"] if isinstance(source, dict) else source
    assert path.startswith("./") and (root / path).resolve() == root

for document in [entrypoint, *sorted((skill / "references").glob("*.md"))]:
    for target in re.findall(r"\[[^\]]+\]\(([^)]+)\)", document.read_text()):
        if "://" in target or target.startswith("#"):
            continue
        resolved = (document.parent / target.split("#")[0]).resolve()
        assert resolved.is_relative_to(skill), f"Reference escapes skill: {document}: {target}"
        assert resolved.exists(), f"Missing reference: {document}: {target}"

assert (root / "LICENSE").is_file()
print(f"Distribution check passed: {codex['name']} {codex['version']}")
