---
name: codex-skill-linker
description: Manage an external directory of Codex skills by creating/removing symlinks (软连接) in the Codex skills folder (usually ~/.codex/skills). Use when you want to enable/disable (link/unlink) specific skills from a given directory, batch enable/disable all skills in that directory, or check which skills from that directory are currently active.
---

# Codex Skill Linker

Linking a skill makes it immediately available in the target skills folder without copying files.

This skill ships a script that can:
- Set a default "source skills directory"
- List which skills exist in that directory
- Enable/disable one skill or all skills (symlink create/delete)
- Show which skills from that directory are currently active (symlink status)

## Quick Start

1) Set the external skills directory (once):

```bash
python3 ~/.codex/skills/codex-skill-linker/scripts/skill_linker.py set-source /path/to/external/skills
```

2) List available skills in that directory:

```bash
python3 ~/.codex/skills/codex-skill-linker/scripts/skill_linker.py list
```

3) Enable a specific skill:

```bash
python3 ~/.codex/skills/codex-skill-linker/scripts/skill_linker.py enable my-skill
```

4) Disable a skill:

```bash
python3 ~/.codex/skills/codex-skill-linker/scripts/skill_linker.py disable my-skill
```

5) Check which skills from the source directory are currently active:

```bash
python3 ~/.codex/skills/codex-skill-linker/scripts/skill_linker.py status
```

## Notes / Safety

- The tool only removes symlinks by default; it refuses to delete real directories/files unless `--force` is passed.
- A "skill folder" is detected as a directory containing a `SKILL.md` file.
- Default target is `~/.codex/skills`. Override with `--target` if you want to link into a repo-local `.codex/skills`.
- If Codex doesn't pick up newly linked skills immediately, restart the Codex app/session.

### scripts/
`scripts/skill_linker.py` implements the symlink management commands. Run it via
`python3 ~/.codex/skills/codex-skill-linker/scripts/skill_linker.py ...`.
