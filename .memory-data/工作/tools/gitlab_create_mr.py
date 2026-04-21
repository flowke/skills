#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any
from urllib import error, parse, request

DEFAULT_CONFIG_PATH = Path.home() / ".gitlab-mr-config.json"


class GitLabMrError(Exception):
    pass


@dataclass
class RepoInfo:
    host: str
    project_path: str
    remote_url: str


@dataclass
class CreateMrOptions:
    title: str
    target_branch: str
    source_branch: str
    description: str | None
    remove_source_branch: bool
    draft: bool
    open_in_browser: bool



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
        raise GitLabMrError(f"git {' '.join(args)} 执行失败: {detail}") from exc

    return result.stdout.strip()



def get_origin_url(repo_cwd: str | None) -> str:
    url = run_git(["remote", "get-url", "origin"], cwd=repo_cwd)
    if not url:
        raise GitLabMrError("未读取到 origin remote，请确认当前目录是 git 仓库。")
    return url



def parse_remote_url(remote_url: str) -> RepoInfo:
    remote_url = remote_url.strip()

    if remote_url.startswith(("http://", "https://")):
        parsed = parse.urlparse(remote_url)
        if not parsed.hostname:
            raise GitLabMrError(f"无法解析 remote URL: {remote_url}")
        project_path = parsed.path.lstrip("/")
        if project_path.endswith(".git"):
            project_path = project_path[:-4]
        return RepoInfo(host=parsed.hostname, project_path=project_path, remote_url=remote_url)

    if remote_url.startswith("git@"):
        try:
            host_part, path_part = remote_url.split(":", 1)
            host = host_part.split("@", 1)[1]
        except (IndexError, ValueError) as exc:
            raise GitLabMrError(f"无法解析 SSH remote URL: {remote_url}") from exc
        project_path = path_part
        if project_path.endswith(".git"):
            project_path = project_path[:-4]
        return RepoInfo(host=host, project_path=project_path, remote_url=remote_url)

    raise GitLabMrError(f"暂不支持这种 remote URL 格式: {remote_url}")



def get_current_branch(repo_cwd: str | None) -> str:
    branch = run_git(["branch", "--show-current"], cwd=repo_cwd)
    if not branch:
        raise GitLabMrError("当前 HEAD 不在本地分支上，无法自动创建 MR。")
    return branch



def ensure_remote_branch_exists(repo_cwd: str | None, branch: str) -> None:
    output = run_git(["ls-remote", "--heads", "origin", branch], cwd=repo_cwd)
    if not output:
        raise GitLabMrError(
            f"远端不存在分支 {branch!r}。请先 push，例如：git push -u origin {branch}"
        )



def get_latest_commit_subject(repo_cwd: str | None) -> str:
    subject = run_git(["log", "-1", "--pretty=%s"], cwd=repo_cwd)
    if not subject:
        raise GitLabMrError("未读取到最近一条 commit message，请显式传入 --title。")
    return subject



def load_config() -> dict[str, Any]:
    config_path_raw = os.getenv("GITLAB_MR_CONFIG")
    config_path = Path(config_path_raw).expanduser() if config_path_raw else DEFAULT_CONFIG_PATH
    if not config_path.exists():
        return {}
    try:
        data = json.loads(config_path.read_text(encoding="utf-8"))
    except OSError as exc:
        raise GitLabMrError(f"读取配置文件失败: {config_path}: {exc}") from exc
    except json.JSONDecodeError as exc:
        raise GitLabMrError(f"配置文件不是合法 JSON: {config_path}: {exc}") from exc

    if not isinstance(data, dict):
        raise GitLabMrError(f"配置文件根节点必须是对象: {config_path}")
    return data



def get_token(config: dict[str, Any]) -> str:
    token = config.get("gitlab_token") or os.getenv("GITLAB_TOKEN") or os.getenv("PRIVATE_TOKEN")
    if token == "请把你的PAT填在这里":
        token = None
    if not token:
        raise GitLabMrError(
            "未读取到 GitLab token。\n"
            f"请优先填写配置文件：{DEFAULT_CONFIG_PATH}\n"
            "或在当前 shell 中设置：export GITLAB_TOKEN='你的PAT'"
        )
    return token



def build_api_base(host: str) -> str:
    return f"https://{host}/api/v4"



def create_merge_request(repo: RepoInfo, options: CreateMrOptions, token: str) -> dict[str, Any]:
    encoded_project = parse.quote(repo.project_path, safe="")
    api_url = f"{build_api_base(repo.host)}/projects/{encoded_project}/merge_requests"

    title = options.title
    if options.draft and not title.lower().startswith(("draft:", "wip:")):
        title = f"Draft: {title}"

    payload: dict[str, Any] = {
        "source_branch": options.source_branch,
        "target_branch": options.target_branch,
        "title": title,
        "remove_source_branch": options.remove_source_branch,
    }
    if options.description:
        payload["description"] = options.description

    body = parse.urlencode(payload).encode("utf-8")
    req = request.Request(
        api_url,
        data=body,
        method="POST",
        headers={
            "PRIVATE-TOKEN": token,
            "Content-Type": "application/x-www-form-urlencoded",
        },
    )

    try:
        with request.urlopen(req) as resp:
            data = resp.read().decode("utf-8")
    except error.HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace")
        raise GitLabMrError(f"GitLab API 创建 MR 失败（HTTP {exc.code}）：{detail}") from exc
    except error.URLError as exc:
        raise GitLabMrError(f"请求 GitLab API 失败：{exc.reason}") from exc

    try:
        return json.loads(data)
    except json.JSONDecodeError as exc:
        raise GitLabMrError(f"GitLab API 返回了非 JSON 数据：{data}") from exc



def open_in_browser(url: str) -> None:
    try:
        subprocess.run(["open", url], check=True)
    except subprocess.CalledProcessError as exc:
        raise GitLabMrError(f"已创建 MR，但自动打开浏览器失败：{exc}") from exc



def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="通过 GitLab API 创建 Merge Request")
    subparsers = parser.add_subparsers(dest="command", required=True)

    create_parser = subparsers.add_parser("create", help="创建 MR")
    create_parser.add_argument("--repo", help="git 仓库目录；不传时默认使用当前工作目录")
    create_parser.add_argument("--title", help="MR 标题；不传时默认使用最近一条 commit message")
    create_parser.add_argument("--target", help="目标分支；不传时优先读取配置文件里的 default_target_branch，否则默认 master")
    create_parser.add_argument("--source", help="源分支；不传时默认使用当前分支")
    create_parser.add_argument("--description", help="MR 描述")
    create_parser.add_argument("--description-file", help="从文件读取 MR 描述内容，优先级高于 --description")
    create_parser.add_argument("--remove-source-branch", action="store_true", help="合并后删除源分支")
    create_parser.add_argument("--draft", action="store_true", help="以 Draft MR 形式创建")
    create_parser.add_argument("--open", action="store_true", help="创建成功后自动在浏览器打开 MR 链接")
    create_parser.add_argument("--json", action="store_true", help="以 JSON 输出结果，便于其他工具串联")

    return parser.parse_args()



def load_description(args: argparse.Namespace) -> str | None:
    if args.description_file:
        try:
            with open(args.description_file, "r", encoding="utf-8") as f:
                return f.read()
        except OSError as exc:
            raise GitLabMrError(f"读取 description 文件失败: {exc}") from exc
    return args.description



def handle_create(args: argparse.Namespace) -> int:
    repo_cwd = os.path.abspath(os.path.expanduser(args.repo)) if args.repo else None
    config = load_config()
    token = get_token(config)
    repo = parse_remote_url(get_origin_url(repo_cwd))
    if config.get("gitlab_host"):
        repo.host = str(config["gitlab_host"])
    source_branch = args.source or get_current_branch(repo_cwd)
    ensure_remote_branch_exists(repo_cwd, source_branch)

    target_branch = args.target or str(config.get("default_target_branch") or "master")
    if source_branch == target_branch:
        raise GitLabMrError(
            f"source branch 和 target branch 都是 {source_branch!r}，这通常不是你想要的。"
        )

    title = args.title or get_latest_commit_subject(repo_cwd)
    description = load_description(args)
    should_open = args.open or bool(config.get("open_after_create"))

    result = create_merge_request(
        repo,
        CreateMrOptions(
            title=title,
            target_branch=target_branch,
            source_branch=source_branch,
            description=description,
            remove_source_branch=args.remove_source_branch,
            draft=args.draft,
            open_in_browser=should_open,
        ),
        token,
    )

    web_url = result.get("web_url") or result.get("url")
    iid = result.get("iid")
    payload = {
        "project": repo.project_path,
        "remote": repo.remote_url,
        "source": source_branch,
        "target": target_branch,
        "iid": iid,
        "title": result.get("title"),
        "url": web_url,
    }

    if args.json:
        print(json.dumps(payload, ensure_ascii=False))
        if web_url and should_open:
            open_in_browser(web_url)
        return 0

    print("MR 创建成功")
    print(f"- project: {repo.project_path}")
    print(f"- remote: {repo.remote_url}")
    print(f"- source: {source_branch}")
    print(f"- target: {target_branch}")
    print(f"- iid: {iid}")
    print(f"- title: {result.get('title')}")
    if web_url:
        print(f"- url: {web_url}")
        if should_open:
            open_in_browser(web_url)

    return 0



def main() -> int:
    args = parse_args()
    try:
        if args.command == "create":
            return handle_create(args)
        raise GitLabMrError(f"不支持的命令: {args.command}")
    except GitLabMrError as exc:
        print(f"[gitlab_create_mr] {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
