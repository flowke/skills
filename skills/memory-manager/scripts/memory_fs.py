#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Iterable

SUBDIRS = ("logs", "topics", "sops", "tools")


@dataclass(frozen=True)
class ModulePaths:
    root: Path
    module: str

    @property
    def base(self) -> Path:
        return self.root / self.module

    @property
    def index(self) -> Path:
        return self.base / "index.md"


def ensure_module(root: Path, module: str) -> ModulePaths:
    module = module.strip() or "general"
    paths = ModulePaths(root=root.expanduser(), module=module)
    paths.base.mkdir(parents=True, exist_ok=True)
    for subdir in SUBDIRS:
        (paths.base / subdir).mkdir(exist_ok=True)
    if not paths.index.exists():
        paths.index.write_text(index_stub(module), encoding="utf-8")
    return paths


def index_stub(module: str) -> str:
    return f"""# 模块索引：{module}

## 模块说明
记录属于“{module}”模块的长期记忆、日志、主题、SOP 和工具。

## Topics
- 暂无

## SOPs
- 暂无

## Tools
- 暂无

## Recent Updates
- 暂无
"""


def iter_relative_files(root: Path, parent: Path) -> Iterable[Path]:
    if not parent.exists():
        return []
    return sorted(
        (path.relative_to(root) for path in parent.rglob("*") if path.is_file()),
        key=lambda p: p.as_posix().lower(),
    )


def rebuild_index(root: Path, module: str, recent_limit: int = 12) -> Path:
    paths = ensure_module(root, module)
    topic_files = list(iter_relative_files(paths.base, paths.base / "topics"))
    sop_files = list(iter_relative_files(paths.base, paths.base / "sops"))
    tool_files = list(iter_relative_files(paths.base, paths.base / "tools"))

    recent_files = [
        path
        for path in paths.base.rglob("*")
        if path.is_file() and path.name != "index.md"
    ]
    recent_files.sort(key=lambda p: p.stat().st_mtime, reverse=True)

    def bullets(items: list[Path], empty: str = "- 暂无") -> str:
        if not items:
            return empty
        return "\n".join(f"- {item.as_posix()}" for item in items)

    recent_lines = []
    for file_path in recent_files[:recent_limit]:
        stamp = datetime.fromtimestamp(file_path.stat().st_mtime).strftime("%Y-%m-%d %H:%M")
        recent_lines.append(f"- {stamp} {file_path.relative_to(paths.base).as_posix()}")
    recent_section = "\n".join(recent_lines) if recent_lines else "- 暂无"

    content = f"""# 模块索引：{module}

## 模块说明
记录属于“{module}”模块的长期记忆、日志、主题、SOP 和工具。

## Topics
{bullets(topic_files)}

## SOPs
{bullets(sop_files)}

## Tools
{bullets(tool_files)}

## Recent Updates
{recent_section}
"""
    paths.index.write_text(content, encoding="utf-8")
    return paths.index
