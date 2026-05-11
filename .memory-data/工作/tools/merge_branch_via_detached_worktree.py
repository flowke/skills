#!/usr/bin/env python3
"""Safely merge a source branch into a target branch using a detached temporary git worktree.

Default behavior is dry-run. Pass --execute to actually run commands.

Example:
  python merge_branch_via_detached_worktree.py \
    --repo /path/to/repo \
    --source 046 \
    --target dev \
    --execute
"""
from __future__ import annotations

import argparse
import os
import shlex
import shutil
import subprocess
import sys
import tempfile
from datetime import datetime
from pathlib import Path


def run(cmd: list[str], *, cwd: str | None = None, execute: bool = False) -> None:
    printable = " ".join(shlex.quote(part) for part in cmd)
    prefix = f"[cwd={cwd}] " if cwd else ""
    print(prefix + printable)
    if execute:
        subprocess.run(cmd, cwd=cwd, check=True)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", required=True, help="Path to the git repository")
    parser.add_argument("--source", required=True, help="Source branch to merge from")
    parser.add_argument("--target", required=True, help="Target branch to merge into, e.g. dev or gray")
    parser.add_argument("--remote", default="origin", help="Git remote name (default: origin)")
    parser.add_argument(
        "--worktree-base",
        default=None,
        help="Parent directory for temporary worktrees (default: system temp dir)",
    )
    parser.add_argument(
        "--execute",
        action="store_true",
        help="Actually run commands. Without this flag, only print the plan.",
    )
    parser.add_argument(
        "--keep-worktree",
        action="store_true",
        help="Keep the temporary worktree after execution for debugging.",
    )
    args = parser.parse_args()

    repo = Path(args.repo).expanduser().resolve()
    if not (repo / ".git").exists() and not (repo / ".git").is_file():
        print(f"[error] Not a git repository: {repo}", file=sys.stderr)
        return 2

    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    temp_root = Path(args.worktree_base).expanduser().resolve() if args.worktree_base else Path(tempfile.gettempdir())
    temp_dir = temp_root / f"git-merge-{args.target}-{timestamp}"
    temp_branch = f"tmp/merge-{args.source}-into-{args.target}-{timestamp}"

    print("[info] Strategy: use a detached temporary worktree based on remote target branch.")
    print("[info] This avoids switching the current working directory branch.")
    print("[info] It also avoids reusing an existing target worktree by default.")

    commands = [
        (["git", "fetch", args.remote], str(repo)),
        (["git", "worktree", "add", "--detach", str(temp_dir), f"{args.remote}/{args.target}"], str(repo)),
        (["git", "switch", "-c", temp_branch], str(temp_dir)),
        (["git", "merge", "--no-ff", "--no-edit", f"{args.remote}/{args.source}"], str(temp_dir)),
        (["git", "push", args.remote, f"HEAD:{args.target}"], str(temp_dir)),
    ]

    try:
        for cmd, cwd in commands:
            run(cmd, cwd=cwd, execute=args.execute)
    finally:
        if args.execute and not args.keep_worktree:
            try:
                subprocess.run(["git", "worktree", "remove", "--force", str(temp_dir)], cwd=str(repo), check=True)
            except subprocess.CalledProcessError as exc:
                print(f"[warn] Failed to remove temporary worktree: {exc}", file=sys.stderr)
            if temp_dir.exists():
                shutil.rmtree(temp_dir, ignore_errors=True)
        elif not args.execute:
            print(f"[dry-run] Temporary worktree would be created at: {temp_dir}")
        elif args.keep_worktree:
            print(f"[info] Temporary worktree kept at: {temp_dir}")

    print("[done]" if args.execute else "[planned]")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
