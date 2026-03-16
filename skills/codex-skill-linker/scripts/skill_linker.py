#!/usr/bin/env python3
"""
Manage an external directory of Codex skills by creating/removing symlinks in a
target skills directory (default: ~/.codex/skills).

This script is intentionally conservative:
- It creates symlinks for skill folders (directories containing SKILL.md)
- It removes only symlinks by default (refuses to delete real dirs/files unless --force)

Config:
- Stored at ~/.codex/skill-linker.json by default
"""

from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import sys
from typing import Any, Dict, Iterable, List, Optional, Tuple


DEFAULT_CONFIG_PATH = Path("~/.codex/skill-linker.json").expanduser()
DEFAULT_TARGET_DIR = Path("~/.codex/skills").expanduser()


def eprint(*args: object) -> None:
    print(*args, file=sys.stderr)


def load_config(path: Path) -> Dict[str, Any]:
    if not path.exists():
        return {}
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        raise SystemExit(f"Failed to read config {path}: {exc}") from exc


def save_config(path: Path, data: Dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def resolve_default_source(cfg: Dict[str, Any]) -> Optional[Path]:
    src = cfg.get("default_source")
    if not src:
        return None
    return Path(str(src)).expanduser()


def resolve_default_target(cfg: Dict[str, Any]) -> Path:
    tgt = cfg.get("default_target")
    if tgt:
        return Path(str(tgt)).expanduser()
    return DEFAULT_TARGET_DIR


def is_skill_dir(p: Path) -> bool:
    return p.is_dir() and (p / "SKILL.md").is_file()


def iter_skills_in_source(source: Path) -> List[Path]:
    if not source.exists():
        raise SystemExit(f"Source directory does not exist: {source}")
    if not source.is_dir():
        raise SystemExit(f"Source is not a directory: {source}")

    skills: List[Path] = []
    for child in sorted(source.iterdir(), key=lambda x: x.name.lower()):
        if is_skill_dir(child):
            skills.append(child)
    return skills


def readlink_real(p: Path) -> Optional[Path]:
    if not p.is_symlink():
        return None
    try:
        target = os.readlink(p)
    except OSError:
        return None
    # Preserve relative symlink targets by resolving from parent
    return (p.parent / target).resolve()


def ensure_target_dir(target: Path) -> None:
    if target.exists() and not target.is_dir():
        raise SystemExit(f"Target exists but is not a directory: {target}")
    target.mkdir(parents=True, exist_ok=True)


def link_one(source_skill: Path, target_dir: Path, force: bool) -> Tuple[str, bool]:
    """
    Returns (message, changed)
    """
    dest = target_dir / source_skill.name
    src_real = source_skill.resolve()

    if dest.exists() or dest.is_symlink():
        if dest.is_symlink():
            cur = readlink_real(dest)
            if cur and cur == src_real:
                return f"[SKIP] {source_skill.name} already enabled", False
            if force:
                dest.unlink()
            else:
                return f"[ERROR] {dest} is a symlink but points elsewhere ({cur}); use --force", False
        else:
            return f"[ERROR] {dest} already exists and is not a symlink; refusing", False

    # Use an absolute link target for clarity and robustness
    dest.symlink_to(src_real)
    return f"[OK] Enabled {source_skill.name} -> {src_real}", True


def unlink_one(source_skill_name: str, source_dir: Path, target_dir: Path, force: bool) -> Tuple[str, bool]:
    """
    Returns (message, changed)
    """
    dest = target_dir / source_skill_name
    if not (dest.exists() or dest.is_symlink()):
        return f"[SKIP] {source_skill_name} not present in target", False

    if dest.is_symlink():
        cur = readlink_real(dest)
        if cur is None:
            if force:
                dest.unlink(missing_ok=True)  # type: ignore[arg-type]
                return f"[OK] Disabled {source_skill_name} (broken symlink removed)", True
            return f"[ERROR] {dest} is a broken symlink; use --force to remove", False

        # If source_dir doesn't match, we still allow removing if --force is used.
        try:
            cur.relative_to(source_dir.resolve())
            dest.unlink()
            return f"[OK] Disabled {source_skill_name}", True
        except ValueError:
            if force:
                dest.unlink()
                return f"[OK] Disabled {source_skill_name} (forced; pointed to {cur})", True
            return f"[ERROR] {dest} points outside source dir ({cur}); use --force", False

    # Not a symlink (real directory/file)
    if force:
        # Extremely conservative: do not rm -rf. Only allow removing files (not directories).
        if dest.is_dir():
            return f"[ERROR] {dest} is a real directory; refusing to delete even with --force", False
        dest.unlink()
        return f"[OK] Removed file {dest} (forced)", True
    return f"[ERROR] {dest} is not a symlink; refusing (use --force for files only)", False


def status(source_dir: Path, target_dir: Path) -> List[Tuple[str, str]]:
    """
    Returns list of (skill_name, status_string)
    """
    ensure_target_dir(target_dir)
    src_real = source_dir.resolve()
    out: List[Tuple[str, str]] = []
    for entry in sorted(target_dir.iterdir(), key=lambda x: x.name.lower()):
        if not entry.is_symlink():
            continue
        cur = readlink_real(entry)
        if cur is None:
            continue
        try:
            cur.relative_to(src_real)
            out.append((entry.name, str(cur)))
        except ValueError:
            continue
    return out


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="skill_linker.py")
    p.add_argument("--config", default=str(DEFAULT_CONFIG_PATH), help="Config file path")
    p.add_argument("--source", help="External skills directory (overrides config default_source)")
    p.add_argument("--target", help="Target skills directory (overrides config default_target)")
    p.add_argument("--force", action="store_true", help="Override safety checks (still conservative)")

    sub = p.add_subparsers(dest="cmd", required=True)

    sp = sub.add_parser("set-source", help="Persist default source directory in config")
    sp.add_argument("path", help="Directory containing external skills (each is a folder with SKILL.md)")

    sp = sub.add_parser("set-target", help="Persist default target skills directory in config")
    sp.add_argument("path", help="Target directory to place symlinks (default: ~/.codex/skills)")

    sub.add_parser("show-config", help="Print resolved config + defaults")

    sub.add_parser("list", help="List skills found in the source directory")

    sp = sub.add_parser("enable", help="Enable one or more skills by name")
    sp.add_argument("names", nargs="+", help="Skill folder name(s) under source directory")

    sp = sub.add_parser("disable", help="Disable one or more skills by name (removes symlinks)")
    sp.add_argument("names", nargs="+", help="Skill folder name(s) in target directory")

    sub.add_parser("enable-all", help="Enable all skills in source directory")
    sub.add_parser("disable-all", help="Disable all skills in target that point into source directory")

    sub.add_parser("status", help="List active symlinks in target that point into source directory")

    return p


def resolve_source_target(args: argparse.Namespace, cfg: Dict[str, Any]) -> Tuple[Path, Path]:
    source = Path(args.source).expanduser() if args.source else resolve_default_source(cfg)
    if not source:
        raise SystemExit(
            "No source directory configured. Provide --source or run: set-source /path/to/external/skills"
        )
    target = Path(args.target).expanduser() if args.target else resolve_default_target(cfg)
    return source, target


def cmd_set_source(args: argparse.Namespace, cfg_path: Path) -> int:
    cfg = load_config(cfg_path)
    cfg["default_source"] = str(Path(args.path).expanduser())
    save_config(cfg_path, cfg)
    print(f"[OK] default_source set to: {cfg['default_source']}")
    return 0


def cmd_set_target(args: argparse.Namespace, cfg_path: Path) -> int:
    cfg = load_config(cfg_path)
    cfg["default_target"] = str(Path(args.path).expanduser())
    save_config(cfg_path, cfg)
    print(f"[OK] default_target set to: {cfg['default_target']}")
    return 0


def main(argv: Optional[List[str]] = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    cfg_path = Path(args.config).expanduser()

    if args.cmd == "set-source":
        return cmd_set_source(args, cfg_path)
    if args.cmd == "set-target":
        return cmd_set_target(args, cfg_path)

    cfg = load_config(cfg_path)

    if args.cmd == "show-config":
        source = resolve_default_source(cfg)
        target = resolve_default_target(cfg)
        print(json.dumps({"config_path": str(cfg_path), "default_source": str(source) if source else None, "default_target": str(target)}, indent=2))
        return 0

    source, target = resolve_source_target(args, cfg)
    ensure_target_dir(target)

    if args.cmd == "list":
        skills = iter_skills_in_source(source)
        if not skills:
            print(f"[OK] No skills found in {source} (expected folders containing SKILL.md)")
            return 0
        print(f"[OK] Skills in {source}:")
        for s in skills:
            print(f"- {s.name}")
        return 0

    if args.cmd == "status":
        items = status(source, target)
        if not items:
            print(f"[OK] No active symlinks found in {target} pointing into {source}")
            return 0
        print(f"[OK] Active skills from {source} (linked into {target}):")
        for name, cur in items:
            print(f"- {name} -> {cur}")
        return 0

    if args.cmd == "enable":
        skills_map = {p.name: p for p in iter_skills_in_source(source)}
        rc = 0
        for name in args.names:
            src = skills_map.get(name)
            if not src:
                eprint(f"[ERROR] Skill not found in source: {name}")
                rc = 2
                continue
            msg, changed = link_one(src, target, force=bool(args.force))
            print(msg)
            if msg.startswith("[ERROR]"):
                rc = 2
        return rc

    if args.cmd == "enable-all":
        rc = 0
        skills = iter_skills_in_source(source)
        if not skills:
            print(f"[OK] No skills found in {source}")
            return 0
        for src in skills:
            msg, _changed = link_one(src, target, force=bool(args.force))
            print(msg)
            if msg.startswith("[ERROR]"):
                rc = 2
        return rc

    if args.cmd == "disable":
        rc = 0
        for name in args.names:
            msg, _changed = unlink_one(name, source_dir=source, target_dir=target, force=bool(args.force))
            print(msg)
            if msg.startswith("[ERROR]"):
                rc = 2
        return rc

    if args.cmd == "disable-all":
        rc = 0
        items = status(source, target)
        if not items:
            print(f"[OK] No active symlinks found in {target} pointing into {source}")
            return 0
        for name, _cur in items:
            msg, _changed = unlink_one(name, source_dir=source, target_dir=target, force=bool(args.force))
            print(msg)
            if msg.startswith("[ERROR]"):
                rc = 2
        return rc

    parser.error(f"Unhandled cmd: {args.cmd}")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())

