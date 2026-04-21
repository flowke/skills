#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path

from memory_fs import ensure_module, rebuild_index


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Initialize a structured memory root.")
    parser.add_argument("--root", required=True, help="Memory root directory.")
    parser.add_argument(
        "--modules",
        default="general",
        help="Comma-separated module names to create. Defaults to general.",
    )
    parser.add_argument(
        "--rebuild-index",
        action="store_true",
        help="Rebuild each module index after creation.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    root = Path(args.root).expanduser()
    root.mkdir(parents=True, exist_ok=True)
    modules = [item.strip() for item in args.modules.split(",") if item.strip()] or ["general"]

    for module in modules:
        paths = ensure_module(root, module)
        if args.rebuild_index:
            rebuild_index(root, module)
        print(f"[ok] {paths.base}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
