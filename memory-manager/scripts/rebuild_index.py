#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path

from memory_fs import rebuild_index


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Rebuild memory module indexes.")
    parser.add_argument("--root", required=True, help="Memory root directory.")
    parser.add_argument("--module", action="append", default=[], help="Module name. Repeatable.")
    parser.add_argument("--all", action="store_true", help="Rebuild every module under the root.")
    parser.add_argument(
        "--recent-limit",
        type=int,
        default=12,
        help="Maximum number of recent files to show in the index.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    root = Path(args.root).expanduser()
    if not root.exists():
        raise SystemExit(f"Memory root does not exist: {root}")

    modules = list(dict.fromkeys(args.module))
    if args.all:
        modules.extend(
            child.name for child in sorted(root.iterdir()) if child.is_dir() and not child.name.startswith(".")
        )
        modules = list(dict.fromkeys(modules))

    if not modules:
        raise SystemExit("Specify --module <name> or use --all")

    for module in modules:
        index_path = rebuild_index(root, module, recent_limit=max(args.recent_limit, 1))
        print(f"[ok] {index_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
