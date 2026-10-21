#!/usr/bin/env python3
"""Create a non-destructive novel project scaffold from the bundled template."""

import argparse
import datetime as dt
import shutil
from pathlib import Path


def initialize(target: Path, title: str, language: str) -> list[Path]:
    template = Path(__file__).resolve().parent.parent / "assets" / "project-template"
    if not template.is_dir():
        raise SystemExit(f"Template not found: {template}")

    target.mkdir(parents=True, exist_ok=True)
    created: list[Path] = []
    substitutions = {
        "{{TITLE}}": title,
        "{{LANGUAGE}}": language,
        "{{DATE}}": dt.date.today().isoformat(),
    }

    for source in sorted(template.rglob("*")):
        relative = source.relative_to(template)
        destination = target / relative
        if source.is_dir():
            destination.mkdir(parents=True, exist_ok=True)
            continue
        if destination.exists():
            continue
        destination.parent.mkdir(parents=True, exist_ok=True)
        content = source.read_text(encoding="utf-8")
        for old, new in substitutions.items():
            content = content.replace(old, new)
        destination.write_text(content, encoding="utf-8")
        created.append(destination)

    for name in ("research", "feedback", "production", "archive"):
        (target / name).mkdir(exist_ok=True)
    return created


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("target", type=Path)
    parser.add_argument("--title", default="Untitled novel")
    parser.add_argument("--language", default="Use the author's language")
    args = parser.parse_args()
    created = initialize(args.target.resolve(), args.title, args.language)
    print(f"Created {len(created)} files in {args.target.resolve()}")
    if not created:
        print("Existing files were preserved; nothing was overwritten.")


if __name__ == "__main__":
    main()
