#!/usr/bin/env python3
import argparse
import json
import os
import sys
from pathlib import Path

THIS_DIR = Path(__file__).resolve().parent
if str(THIS_DIR) not in sys.path:
    sys.path.insert(0, str(THIS_DIR))

from yapi_interface_lib import (  # noqa: E402
    YapiInterfaceError,
    build_config_diagnostic,
    extract_interface_id,
    fetch_interface_doc,
    pretty_text_summary,
    resolve_config,
    summarize_interface_doc,
)


def main():
    parser = argparse.ArgumentParser(description="Fetch and summarize a YAPI interface document by ID or page URL")
    parser.add_argument("--start-dir", default=os.getcwd(), help="Workspace directory to search first (default: cwd)")
    source = parser.add_mutually_exclusive_group(required=True)
    source.add_argument("--id", help="YAPI interface ID, e.g. 184595")
    source.add_argument("--url", help="YAPI page URL containing the interface ID")
    parser.add_argument("--raw", action="store_true", help="Print raw API response JSON")
    parser.add_argument("--json", action="store_true", help="Print machine-readable summary JSON")
    args = parser.parse_args()

    try:
        config_path, config = resolve_config(args.start_dir)
        interface_id = extract_interface_id(args.id or args.url)
        result = fetch_interface_doc(config, interface_id)
        summary = summarize_interface_doc(result["data"])
    except SystemExit:
        raise
    except YapiInterfaceError as e:
        diagnostic = {}
        try:
            config_path, config = resolve_config(args.start_dir)
            diagnostic = build_config_diagnostic(config_path, config)
        except BaseException:
            diagnostic = {}
        message = str(e)
        if diagnostic:
            message = message + "\nConfig diagnostic: " + json.dumps(diagnostic, ensure_ascii=False)
        raise SystemExit(f"ERROR: {message}")

    if args.raw:
        print(json.dumps(result["payload"], ensure_ascii=False, indent=2))
        return

    if args.json:
        print(json.dumps(summary, ensure_ascii=False, indent=2))
        return

    print(pretty_text_summary(summary))


if __name__ == "__main__":
    main()
