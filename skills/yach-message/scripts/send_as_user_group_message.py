#!/usr/bin/env python3
import argparse
import json
import os
import sys
from pathlib import Path

THIS_DIR = Path(__file__).resolve().parent
if str(THIS_DIR) not in sys.path:
    sys.path.insert(0, str(THIS_DIR))

from yach_message_lib import (  # noqa: E402
    YachMessageError,
    build_markdown_message,
    build_text_message,
    get_access_token,
    load_message_from_args,
    read_text_content,
    resolve_config,
    send_user_group_message,
)


def main():
    parser = argparse.ArgumentParser(description="Experimental: send a Yach/知音楼 group message as a specific user")
    parser.add_argument("--start-dir", default=os.getcwd(), help="Workspace directory to search first (default: cwd)")
    parser.add_argument("--from-user-id", required=True, help="Sender Yach user ID, e.g. yach131763")
    parser.add_argument("--group-id", required=True, help="Group ID, e.g. 2740956956")
    parser.add_argument("--msgtype", choices=["text", "markdown"], default="text")
    parser.add_argument("--content", help="Message content/text; for markdown this is the markdown body")
    parser.add_argument("--content-file", help="Read content from a UTF-8 text file")
    parser.add_argument("--title", help="Markdown title; if omitted, derived from the first non-empty line")
    parser.add_argument("--image", help="Optional markdown cover image URL")
    parser.add_argument("--at-work-codes", help="Work codes to @, separated by | or ,")
    parser.add_argument("--at-mobiles", help="Mobile numbers to @, separated by | or ,")
    parser.add_argument("--at-all", action="store_true", help="Whether to @all")
    parser.add_argument("--message-json", help="Raw message JSON string; bypasses --msgtype/--content")
    parser.add_argument("--message-file", help="Path to raw message JSON file; bypasses --msgtype/--content")
    parser.add_argument("--message-id", help="Business message unique ID for de-duplication")
    parser.add_argument("--dry-run", action="store_true", help="Print request preview without sending")
    args = parser.parse_args()

    try:
        _, config = resolve_config(args.start_dir)
        token = get_access_token(config)

        message = load_message_from_args(args.message_json, args.message_file)
        if message is None:
            content = read_text_content(args.content, args.content_file)
            if args.msgtype == "text":
                message = build_text_message(
                    content=content or "",
                    at_work_codes=args.at_work_codes,
                    at_mobiles=args.at_mobiles,
                    at_all=args.at_all,
                )
            else:
                message = build_markdown_message(
                    text=content or "",
                    title=args.title,
                    image=args.image,
                    at_work_codes=args.at_work_codes,
                    at_mobiles=args.at_mobiles,
                    at_all=args.at_all,
                )

        result = send_user_group_message(
            config=config,
            token=token,
            message=message,
            from_user_id=args.from_user_id,
            group_id=args.group_id,
            message_id=args.message_id,
            dry_run=args.dry_run,
        )
        print(json.dumps(result, ensure_ascii=False, indent=2))
    except YachMessageError as e:
        raise SystemExit(f"ERROR: {e}")


if __name__ == "__main__":
    main()
