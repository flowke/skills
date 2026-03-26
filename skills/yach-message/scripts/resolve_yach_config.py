#!/usr/bin/env python3
import argparse
import json
import os
from pathlib import Path

REQUIRED_KEYS = ["appkey", "appsecret", "base_url"]
OPTIONAL_KEYS = ["agent_id", "app_id"]
ALL_KEYS = REQUIRED_KEYS + OPTIONAL_KEYS
DEFAULT_BASE_URL = "https://yach-oapi.zhiyinlou.com"


def mask(value: str) -> str:
    value = str(value or "")
    if not value:
        return ""
    if len(value) <= 6:
        return "***"
    return f"{value[:3]}***{value[-3:]}"


def candidate_paths(start_dir: Path):
    yield start_dir / ".yach-config.json"
    home = Path.home() / ".yach-config.json"
    if home != start_dir / ".yach-config.json":
        yield home


def load_config(path: Path):
    try:
        with path.open("r", encoding="utf-8") as f:
            data = json.load(f)
    except FileNotFoundError:
        raise
    except Exception as e:
        raise SystemExit(f"ERROR: failed to parse {path}: {e}")

    if not isinstance(data, dict):
        raise SystemExit(f"ERROR: config must be a JSON object: {path}")

    missing = [k for k in REQUIRED_KEYS if not data.get(k)]
    if missing:
        raise SystemExit(f"ERROR: missing required keys in {path}: {', '.join(missing)}")

    if data.get("base_url") != DEFAULT_BASE_URL:
        raise SystemExit(
            f"ERROR: unsupported base_url in {path}: {data.get('base_url')} (expected {DEFAULT_BASE_URL})"
        )
    return data


def resolve(start_dir: Path):
    tried = []
    for path in candidate_paths(start_dir):
        tried.append(str(path))
        if path.is_file():
            data = load_config(path)
            return path, data, tried
    tried_str = "\n  - ".join([""] + tried)
    raise SystemExit("ERROR: no .yach-config.json found. Search order:" + tried_str)


def main():
    parser = argparse.ArgumentParser(
        description="Resolve yach-message config. Search order: cwd/.yach-config.json -> ~/.yach-config.json"
    )
    parser.add_argument("--start-dir", default=os.getcwd(), help="Workspace directory to search first (default: cwd)")
    parser.add_argument("--path", action="store_true", help="Print resolved config path")
    parser.add_argument("--json", action="store_true", help="Print resolved config JSON")
    parser.add_argument("--field", choices=ALL_KEYS, help="Print one config field if present")
    parser.add_argument("--summary", action="store_true", help="Print masked summary")
    parser.add_argument("--validate", action="store_true", help="Exit 0 if config resolves and validates")
    args = parser.parse_args()

    start_dir = Path(args.start_dir).expanduser().resolve()
    path, data, _ = resolve(start_dir)

    if args.path:
        print(path)
        return
    if args.json:
        print(json.dumps(data, ensure_ascii=False))
        return
    if args.field:
        print(data.get(args.field, ""))
        return
    if args.summary or not any([args.path, args.json, args.field, args.validate]):
        summary = {
            "path": str(path),
            "appkey": mask(data.get("appkey", "")),
            "appsecret": mask(data.get("appsecret", "")),
            "agent_id": mask(data.get("agent_id", "")),
            "app_id": mask(data.get("app_id", "")),
            "base_url": data.get("base_url", ""),
            "source": "workspace" if path.parent == start_dir else "global",
        }
        print(json.dumps(summary, ensure_ascii=False))
        return


if __name__ == "__main__":
    main()
