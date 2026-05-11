#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any

SEMVER_RE = re.compile(r"^v(\d+)\.(\d+)\.(\d+)$")
DEFAULT_TARGET_REF = "origin/master"


class ReleaseTagError(Exception):
    pass


@dataclass
class TagPlan:
    repo: str
    ref: str
    latest_tag: str
    next_tag: str
    bump: str
    message: str
    ref_commit: str
    ref_subject: str



def run_git(args: list[str], cwd: str | None = None) -> str:
    try:
        result = subprocess.run(
            ["git", *args],
            cwd=cwd,
            check=True,
            capture_output=True,
            text=True,
        )
    except subprocess.CalledProcessError as exc:
        stderr = exc.stderr.strip()
        stdout = exc.stdout.strip()
        detail = stderr or stdout or str(exc)
        raise ReleaseTagError(f"git {' '.join(args)} 执行失败: {detail}") from exc
    return result.stdout.strip()



def normalize_repo(repo: str | None) -> str | None:
    if not repo:
        return None
    return os.path.abspath(os.path.expanduser(repo))



def ensure_git_repo(repo: str | None) -> str:
    cwd = repo or os.getcwd()
    git_dir = run_git(["rev-parse", "--git-dir"], cwd=cwd)
    if not git_dir:
        raise ReleaseTagError("当前目录不是 git 仓库，或无法定位 .git。")
    return cwd



def fetch_tags_and_refs(repo: str) -> None:
    run_git(["fetch", "origin", "--prune", "--tags"], cwd=repo)



def ensure_ref_exists(repo: str, ref: str) -> None:
    run_git(["rev-parse", "--verify", ref], cwd=repo)



def list_version_tags(repo: str) -> list[str]:
    output = run_git(["tag", "--list", "v*", "--sort=-version:refname"], cwd=repo)
    tags = [line.strip() for line in output.splitlines() if line.strip()]
    return [tag for tag in tags if SEMVER_RE.match(tag)]



def parse_semver(tag: str) -> tuple[int, int, int]:
    match = SEMVER_RE.match(tag)
    if not match:
        raise ReleaseTagError(f"tag 格式不是预期的 vX.Y.Z: {tag}")
    return tuple(int(x) for x in match.groups())



def bump_version(tag: str, bump: str) -> str:
    major, minor, patch = parse_semver(tag)
    if bump == "major":
        major += 1
        minor = 0
        patch = 0
    elif bump == "minor":
        minor += 1
        patch = 0
    elif bump == "patch":
        patch += 1
    else:
        raise ReleaseTagError(f"不支持的 bump 类型: {bump}")
    return f"v{major}.{minor}.{patch}"



def get_ref_subject(repo: str, ref: str) -> str:
    return run_git(["log", "-1", "--pretty=%s", ref], cwd=repo)



def get_ref_commit(repo: str, ref: str) -> str:
    return run_git(["rev-parse", ref], cwd=repo)



def build_message(message: str | None, mr_title: str | None, ref_subject: str) -> str:
    if message:
        return message
    if mr_title:
        return mr_title
    return ref_subject



def build_plan(repo: str, ref: str, bump: str, message: str | None, mr_title: str | None, do_fetch: bool) -> TagPlan:
    repo = ensure_git_repo(repo)
    if do_fetch:
        fetch_tags_and_refs(repo)
    ensure_ref_exists(repo, ref)
    tags = list_version_tags(repo)
    if not tags:
        raise ReleaseTagError("未读取到符合 vX.Y.Z 格式的历史 tag，无法自动升级。")
    latest_tag = tags[0]
    next_tag = bump_version(latest_tag, bump)
    ref_subject = get_ref_subject(repo, ref)
    ref_commit = get_ref_commit(repo, ref)
    final_message = build_message(message, mr_title, ref_subject)
    return TagPlan(
        repo=repo,
        ref=ref,
        latest_tag=latest_tag,
        next_tag=next_tag,
        bump=bump,
        message=final_message,
        ref_commit=ref_commit,
        ref_subject=ref_subject,
    )



def tag_exists(repo: str, tag: str) -> bool:
    output = run_git(["tag", "--list", tag], cwd=repo)
    return bool(output.strip())



def create_local_tag(plan: TagPlan) -> None:
    if tag_exists(plan.repo, plan.next_tag):
        raise ReleaseTagError(f"tag 已存在，无法重复创建: {plan.next_tag}")
    run_git(["tag", "-a", plan.next_tag, plan.ref, "-m", plan.message], cwd=plan.repo)



def push_tag(plan: TagPlan) -> None:
    run_git(["push", "origin", plan.next_tag], cwd=plan.repo)



def plan_to_dict(plan: TagPlan) -> dict[str, Any]:
    return {
        "repo": plan.repo,
        "ref": plan.ref,
        "latest_tag": plan.latest_tag,
        "next_tag": plan.next_tag,
        "bump": plan.bump,
        "message": plan.message,
        "ref_commit": plan.ref_commit,
        "ref_subject": plan.ref_subject,
    }



def add_common_args(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--repo", help="git 仓库目录；不传时默认使用当前工作目录")
    parser.add_argument("--ref", default=DEFAULT_TARGET_REF, help="打 tag 的基准 ref，默认 origin/master")
    parser.add_argument("--bump", choices=["major", "minor", "patch"], default="patch", help="版本升级级别，默认 patch")
    parser.add_argument("--message", help="tag 说明文案；优先级最高")
    parser.add_argument("--mr-title", help="若未显式给 --message，则优先用 MR 标题作为 tag 说明")
    parser.add_argument("--no-fetch", action="store_true", help="不执行 git fetch origin --prune --tags")
    parser.add_argument("--json", action="store_true", help="输出 JSON")



def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="规划或推送 git.100tal 项目的线上发布 tag")
    subparsers = parser.add_subparsers(dest="command", required=True)

    plan_parser = subparsers.add_parser("plan", help="只计算下一版 tag，不推送")
    add_common_args(plan_parser)

    push_parser = subparsers.add_parser("push", help="创建并推送下一版 tag")
    add_common_args(push_parser)

    return parser.parse_args()



def print_human(plan: TagPlan, pushed: bool = False) -> None:
    action = "Tag 已推送" if pushed else "Tag 方案已生成"
    print(action)
    print(f"- repo: {plan.repo}")
    print(f"- ref: {plan.ref}")
    print(f"- ref_commit: {plan.ref_commit}")
    print(f"- latest_tag: {plan.latest_tag}")
    print(f"- next_tag: {plan.next_tag}")
    print(f"- bump: {plan.bump}")
    print(f"- message: {plan.message}")
    print(f"- ref_subject: {plan.ref_subject}")



def main() -> int:
    args = parse_args()
    try:
        plan = build_plan(
            repo=normalize_repo(args.repo),
            ref=args.ref,
            bump=args.bump,
            message=args.message,
            mr_title=args.mr_title,
            do_fetch=not args.no_fetch,
        )
        if args.command == "push":
            create_local_tag(plan)
            push_tag(plan)
            payload = plan_to_dict(plan) | {"pushed": True}
            if args.json:
                print(json.dumps(payload, ensure_ascii=False))
            else:
                print_human(plan, pushed=True)
            return 0

        payload = plan_to_dict(plan) | {"pushed": False}
        if args.json:
            print(json.dumps(payload, ensure_ascii=False))
        else:
            print_human(plan, pushed=False)
        return 0
    except ReleaseTagError as exc:
        print(f"[gitlab_release_tag] {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
