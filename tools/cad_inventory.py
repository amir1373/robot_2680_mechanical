#!/usr/bin/env python3
"""Create a simple inventory of CAD and manufacturing files."""

from __future__ import annotations

import argparse
from collections import Counter
from pathlib import Path

CAD_EXTENSIONS = {
    ".sldprt", ".sldasm", ".slddrw", ".step", ".stp", ".igs", ".iges",
    ".stl", ".dxf", ".dwg", ".pdf", ".zip", ".rar",
}


def scan(root: Path) -> tuple[Counter[str], list[Path]]:
    counts: Counter[str] = Counter()
    files: list[Path] = []

    for path in root.rglob("*"):
        if path.is_file() and path.suffix.lower() in CAD_EXTENSIONS:
            counts[path.suffix.lower()] += 1
            files.append(path)

    return counts, files


def main() -> int:
    parser = argparse.ArgumentParser(description="Inventory CAD/manufacturing files.")
    parser.add_argument("root", nargs="?", type=Path, default=Path.cwd())
    parser.add_argument("--list", action="store_true", help="Print matching file paths.")
    args = parser.parse_args()

    counts, files = scan(args.root)
    if not files:
        print("No CAD/manufacturing files found.")
        return 1

    print("File type summary:")
    for suffix, count in sorted(counts.items()):
        print(f"  {suffix:8} {count}")

    if args.list:
        print("\nFiles:")
        for path in sorted(files):
            print(path.relative_to(args.root))

    return 0


if __name__ == "__main__":
    raise SystemExit(main())