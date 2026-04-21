#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path

from memory_fs import ensure_module, rebuild_index


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Create or repair a single memory module.")
    parser.add_argument("--root", required=True, help="Memory root directory.")
    parser.add_argument("--module", required=True, help="Module name.")
    parser.add_argument(
        "--rebuild-index",
        action="store_true",
        help="Rebuild the module index after ensuring the structure.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    root = Path(args.root).expanduser()
    paths = ensure_module(root, args.module)
    if args.rebuild_index:
        rebuild_index(root, args.module)
    print(f"[ok] {paths.base}")
    print(f"[ok] {paths.index}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
