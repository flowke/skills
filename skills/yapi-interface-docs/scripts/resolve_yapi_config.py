#!/usr/bin/env python3
import argparse
import json
import os
from pathlib import Path

CONFIG_NAME = ".yapi-config.json"
DEFAULT_BASE_URL = "https://yapi.xesv5.com"
DEFAULT_TIMEOUT_SEC = 20
REQUIRED_KEYS = ["base_url", "cookie"]
OPTIONAL_KEYS = ["headers", "timeout_sec"]
ALL_KEYS = REQUIRED_KEYS + OPTIONAL_KEYS


def mask(value: str) -> str:
    value = str(value or "")
    if not value:
        return ""
    if len(value) <= 8:
        return "***"
    return f"{value[:4]}***{value[-4:]}"


def candidate_paths(start_dir: Path):
    yield start_dir / CONFIG_NAME
    home = Path.home() / CONFIG_NAME
    if home != start_dir / CONFIG_NAME:
        yield home


def _normalize_headers(headers):
    if headers is None:
        return {}
    if not isinstance(headers, dict):
        raise SystemExit("ERROR: headers must be a JSON object if provided")
    normalized = {}
    for key, value in headers.items():
        if value is None:
            continue
        normalized[str(key)] = str(value)
    return normalized


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

    data = dict(data)
    data.setdefault("base_url", DEFAULT_BASE_URL)
    data.setdefault("timeout_sec", DEFAULT_TIMEOUT_SEC)
    data["headers"] = _normalize_headers(data.get("headers"))

    missing = [key for key in REQUIRED_KEYS if not str(data.get(key, "")).strip()]
    if missing:
        example = json.dumps(
            {
                "base_url": DEFAULT_BASE_URL,
                "cookie": "xesId=...; _yapi_token=...",
                "headers": {
                    "accept": "application/json, text/plain, */*",
                    "referer": f"{DEFAULT_BASE_URL}/",
                },
                "timeout_sec": DEFAULT_TIMEOUT_SEC,
            },
            ensure_ascii=False,
            indent=2,
        )
        raise SystemExit(
            f"ERROR: missing required keys in {path}: {', '.join(missing)}\n"
            f"Minimal example:\n{example}"
        )

    try:
        timeout_sec = int(data.get("timeout_sec", DEFAULT_TIMEOUT_SEC))
    except (TypeError, ValueError):
        raise SystemExit(f"ERROR: timeout_sec must be an integer in {path}")

    if timeout_sec <= 0:
        raise SystemExit(f"ERROR: timeout_sec must be > 0 in {path}")

    data["timeout_sec"] = timeout_sec
    data["base_url"] = str(data["base_url"]).rstrip("/")
    data["cookie"] = str(data["cookie"]).strip()
    return data


def resolve(start_dir: Path):
    tried = []
    for path in candidate_paths(start_dir):
        tried.append(str(path))
        if path.is_file():
            data = load_config(path)
            return path, data, tried
    tried_str = "\n  - ".join([""] + tried)
    raise SystemExit(
        "ERROR: no .yapi-config.json found. Search order:"
        + tried_str
        + "\nMinimal example:\n"
        + json.dumps(
            {
                "base_url": DEFAULT_BASE_URL,
                "cookie": "xesId=...; _yapi_token=...",
                "headers": {
                    "accept": "application/json, text/plain, */*",
                    "referer": f"{DEFAULT_BASE_URL}/",
                },
                "timeout_sec": DEFAULT_TIMEOUT_SEC,
            },
            ensure_ascii=False,
            indent=2,
        )
    )


def main():
    parser = argparse.ArgumentParser(
        description="Resolve yapi-interface-docs config. Search order: cwd/.yapi-config.json -> ~/.yapi-config.json"
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
        print(json.dumps(data, ensure_ascii=False, indent=2))
        return
    if args.field:
        value = data.get(args.field, "")
        if isinstance(value, (dict, list)):
            print(json.dumps(value, ensure_ascii=False))
        else:
            print(value)
        return
    if args.summary or not any([args.path, args.json, args.field, args.validate]):
        summary = {
            "path": str(path),
            "base_url": data.get("base_url", ""),
            "cookie": mask(data.get("cookie", "")),
            "headers": data.get("headers", {}),
            "timeout_sec": data.get("timeout_sec"),
            "source": "workspace" if path.parent == start_dir else "global",
        }
        print(json.dumps(summary, ensure_ascii=False, indent=2))
        return


if __name__ == "__main__":
    main()
