#!/usr/bin/env python3
import argparse
import json
import os
import sys
from pathlib import Path

THIS_DIR = Path(__file__).resolve().parent
if str(THIS_DIR) not in sys.path:
    sys.path.insert(0, str(THIS_DIR))

from yach_message_lib import YachMessageError, get_access_token, resolve_config  # noqa: E402


def mask(value: str) -> str:
    value = str(value or "")
    if len(value) <= 6:
        return "***"
    return f"{value[:3]}***{value[-3:]}"


def main():
    parser = argparse.ArgumentParser(description="Get Yach access_token using local/global .yach-config.json")
    parser.add_argument("--start-dir", default=os.getcwd(), help="Workspace directory to search first (default: cwd)")
    parser.add_argument("--json", action="store_true", help="Print JSON instead of plain token")
    parser.add_argument("--masked", action="store_true", help="Mask token in output")
    args = parser.parse_args()

    try:
        path, config = resolve_config(args.start_dir)
        token = get_access_token(config)
    except YachMessageError as e:
        raise SystemExit(f"ERROR: {e}")

    if args.json:
        payload = {
            "config_path": str(path),
            "token": mask(token) if args.masked else token,
        }
        print(json.dumps(payload, ensure_ascii=False))
        return

    print(mask(token) if args.masked else token)


if __name__ == "__main__":
    main()
