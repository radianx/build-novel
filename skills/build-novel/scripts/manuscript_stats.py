#!/usr/bin/env python3
"""Report lightweight Markdown manuscript statistics without imposing targets."""

import argparse
import re
from pathlib import Path


CHAPTER = re.compile(r"chapter-(\d+)\.md$", re.IGNORECASE)
WORD = re.compile(r"[^\W_]+(?:[’'-][^\W_]+)*", re.UNICODE)


def count_words(text: str) -> int:
    text = re.sub(r"```.*?```", " ", text, flags=re.DOTALL)
    text = re.sub(r"<!--.*?-->", " ", text, flags=re.DOTALL)
    return len(WORD.findall(text))


def chapters(directory: Path) -> list[tuple[int, Path, int]]:
    found = []
    for path in directory.glob("chapter-*.md"):
        match = CHAPTER.match(path.name)
        if match:
            found.append((int(match.group(1)), path, count_words(path.read_text(encoding="utf-8"))))
    return sorted(found)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("manuscript", type=Path)
    args = parser.parse_args()
    found = chapters(args.manuscript)
    if not found:
        raise SystemExit("No chapter-NN.md files found")

    print("chapter\twords")
    for number, _, words in found:
        print(f"{number}\t{words}")
    total = sum(item[2] for item in found)
    print(f"total\t{total}")
    print(f"average\t{total / len(found):.1f}")
    expected = set(range(found[0][0], found[-1][0] + 1))
    missing = sorted(expected - {item[0] for item in found})
    if missing:
        print("missing\t" + ", ".join(map(str, missing)))


if __name__ == "__main__":
    main()
