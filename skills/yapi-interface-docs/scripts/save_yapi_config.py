#!/usr/bin/env python3
import argparse
import json
import os
from pathlib import Path

CONFIG_NAME = ".yapi-config.json"
DEFAULT_BASE_URL = "https://yapi.xesv5.com"
DEFAULT_TIMEOUT_SEC = 20
DEFAULT_ACCEPT = "application/json, text/plain, */*"


def mask(value: str) -> str:
    value = str(value or "")
    if not value:
        return ""
    if len(value) <= 8:
        return "***"
    return f"{value[:4]}***{value[-4:]}"


def load_existing(path: Path):
    if not path.is_file():
        return {}
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except Exception as e:
        raise SystemExit(f"ERROR: failed to parse existing config {path}: {e}")
    if not isinstance(data, dict):
        raise SystemExit(f"ERROR: existing config must be a JSON object: {path}")
    return data


def target_path(start_dir: Path, use_workspace: bool) -> Path:
    return (start_dir / CONFIG_NAME) if use_workspace else (Path.home() / CONFIG_NAME)


def main():
    parser = argparse.ArgumentParser(description="Save or update .yapi-config.json in workspace or home directory")
    parser.add_argument("--start-dir", default=os.getcwd(), help="Workspace directory used when --workspace is set")
    parser.add_argument("--workspace", action="store_true", help="Write config to cwd/.yapi-config.json instead of ~/.yapi-config.json")
    parser.add_argument("--cookie", help="Cookie string used to access YAPI")
    parser.add_argument("--base-url", default=DEFAULT_BASE_URL, help=f"YAPI base URL (default: {DEFAULT_BASE_URL})")
    parser.add_argument("--accept", default=DEFAULT_ACCEPT, help="Default Accept header")
    parser.add_argument("--referer", help="Referer header (default: <base_url>/)")
    parser.add_argument("--timeout-sec", type=int, default=DEFAULT_TIMEOUT_SEC, help=f"HTTP timeout in seconds (default: {DEFAULT_TIMEOUT_SEC})")
    args = parser.parse_args()

    if not args.cookie or not args.cookie.strip():
        raise SystemExit("ERROR: --cookie is required. If the request failed due to permission, provide the latest YAPI cookie.")
    if args.timeout_sec <= 0:
        raise SystemExit("ERROR: --timeout-sec must be > 0")

    start_dir = Path(args.start_dir).expanduser().resolve()
    path = target_path(start_dir, args.workspace)
    existing = load_existing(path)

    base_url = str(args.base_url or existing.get("base_url") or DEFAULT_BASE_URL).rstrip("/")
    headers = dict(existing.get("headers") or {})
    headers["accept"] = args.accept
    headers["referer"] = args.referer or f"{base_url}/"

    payload = {
        "base_url": base_url,
        "cookie": args.cookie.strip(),
        "headers": headers,
        "timeout_sec": args.timeout_sec,
    }

    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    try:
        os.chmod(path, 0o600)
    except PermissionError:
        pass

    summary = {
        "path": str(path),
        "source": "workspace" if args.workspace else "global",
        "base_url": payload["base_url"],
        "cookie": mask(payload["cookie"]),
        "headers": payload["headers"],
        "timeout_sec": payload["timeout_sec"],
    }
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
