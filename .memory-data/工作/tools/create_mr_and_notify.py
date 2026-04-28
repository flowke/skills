#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from pathlib import Path

DEFAULT_NOTIFY_WORK_CODE = "113166"
DEFAULT_NOTIFY_DISPLAY_NAME = "涔涔"
DEFAULT_TEMPLATE = "{name}, 帮合并下: {mr_url}"
FALLBACK_TEMPLATE = "帮合并下: {mr_url}"

MEMORY_ROOT = Path(__file__).resolve().parent.parent
MR_TOOL = MEMORY_ROOT / "tools/gitlab_create_mr.py"
DEFAULT_YACH_SKILL_ROOT = Path.home() / "Documents/AAA/skills/skills/yach-message"
YACH_SKILL_ROOT = Path(os.getenv("YACH_MESSAGE_SKILL_ROOT", str(DEFAULT_YACH_SKILL_ROOT))).expanduser()
YACH_SEND_SINGLE = YACH_SKILL_ROOT / "scripts/send_single_message.py"


class WorkflowError(Exception):
    pass



def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="创建 MR 并通知默认协作者")
    parser.add_argument("--repo", help="git 仓库目录；不传时默认使用当前工作目录")
    parser.add_argument("--title", help="MR 标题；不传时默认使用最近一条 commit message")
    parser.add_argument("--target", help="目标分支；不传时优先读取配置文件里的 default_target_branch，否则默认 master")
    parser.add_argument("--source", help="源分支；不传时默认使用当前分支")
    parser.add_argument("--description", help="MR 描述")
    parser.add_argument("--description-file", help="从文件读取 MR 描述内容，优先级高于 --description")
    parser.add_argument("--remove-source-branch", action="store_true", help="合并后删除源分支")
    parser.add_argument("--draft", action="store_true", help="以 Draft MR 形式创建")
    parser.add_argument("--open", action="store_true", help="创建成功后自动在浏览器打开 MR 链接")

    parser.add_argument("--notify-work-code", default=DEFAULT_NOTIFY_WORK_CODE, help="通知接收人工号；默认 113166")
    parser.add_argument("--notify-name", help="通知接收人称呼；默认在给 113166 时使用“涔涔”")
    parser.add_argument("--notify-content", help="完整消息内容模板；支持 {mr_url} / {mr_title} / {name} 占位符")
    parser.add_argument("--notify-dry-run", action="store_true", help="只预览消息请求，不真正发送")
    parser.add_argument("--skip-notify", action="store_true", help="只创建 MR，不发送消息")
    parser.add_argument("--json", action="store_true", help="以 JSON 输出两步结果")
    return parser



def run(cmd: list[str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(cmd, check=True, capture_output=True, text=True)



def create_mr(args: argparse.Namespace) -> dict:
    if not MR_TOOL.exists():
        raise WorkflowError(f"未找到 MR 工具: {MR_TOOL}")

    cmd = [sys.executable, str(MR_TOOL), "create", "--json"]
    for flag, value in (("--repo", args.repo), ("--title", args.title), ("--target", args.target), ("--source", args.source), ("--description", args.description), ("--description-file", args.description_file)):
        if value:
            cmd.extend([flag, value])
    if args.remove_source_branch:
        cmd.append("--remove-source-branch")
    if args.draft:
        cmd.append("--draft")
    if args.open:
        cmd.append("--open")

    try:
        result = run(cmd)
    except subprocess.CalledProcessError as exc:
        raise WorkflowError(exc.stderr.strip() or exc.stdout.strip() or "MR 创建失败") from exc

    try:
        return json.loads(result.stdout.strip())
    except json.JSONDecodeError as exc:
        raise WorkflowError(f"MR 工具返回了非 JSON 输出: {result.stdout}") from exc



def build_notify_content(args: argparse.Namespace, mr: dict) -> str:
    mr_url = mr.get("url") or ""
    mr_title = mr.get("title") or ""
    notify_work_code = args.notify_work_code

    if args.notify_content:
        return args.notify_content.format(mr_url=mr_url, mr_title=mr_title, name=args.notify_name or DEFAULT_NOTIFY_DISPLAY_NAME)

    if args.notify_name:
        return DEFAULT_TEMPLATE.format(name=args.notify_name, mr_url=mr_url)

    if notify_work_code == DEFAULT_NOTIFY_WORK_CODE:
        return DEFAULT_TEMPLATE.format(name=DEFAULT_NOTIFY_DISPLAY_NAME, mr_url=mr_url)

    return FALLBACK_TEMPLATE.format(mr_url=mr_url)



def notify(args: argparse.Namespace, mr: dict) -> dict:
    if args.skip_notify:
        return {"skipped": True}
    if not YACH_SEND_SINGLE.exists():
        raise WorkflowError(f"未找到知音楼发送脚本: {YACH_SEND_SINGLE}")

    content = build_notify_content(args, mr)
    cmd = [
        sys.executable,
        str(YACH_SEND_SINGLE),
        "--to-work-code", args.notify_work_code,
        "--msgtype", "text",
        "--content", content,
    ]
    if args.notify_dry_run:
        cmd.append("--dry-run")

    try:
        result = run(cmd)
    except subprocess.CalledProcessError as exc:
        raise WorkflowError(exc.stderr.strip() or exc.stdout.strip() or "知音楼消息发送失败") from exc

    return {
        "work_code": args.notify_work_code,
        "content": content,
        "dry_run": args.notify_dry_run,
        "raw_output": result.stdout.strip(),
    }



def main() -> int:
    args = build_parser().parse_args()
    try:
        mr = create_mr(args)
        notify_result = notify(args, mr)
    except WorkflowError as exc:
        print(f"[create_mr_and_notify] {exc}", file=sys.stderr)
        return 1

    payload = {"mr": mr, "notify": notify_result}
    if args.json:
        print(json.dumps(payload, ensure_ascii=False))
        return 0

    print("前两步执行完成")
    print(f"- mr_url: {mr.get('url')}")
    print(f"- mr_title: {mr.get('title')}")
    if notify_result.get("skipped"):
        print("- notify: skipped")
    else:
        print(f"- notify_to: {notify_result.get('work_code')}")
        print(f"- notify_content: {notify_result.get('content')}")
        print(f"- notify_dry_run: {notify_result.get('dry_run')}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
