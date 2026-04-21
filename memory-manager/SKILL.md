---
name: memory-manager
description: Structured memory capture, retrieval, update, and organization using the unified filesystem memory root at /Users/flowkehurly/.memory-data. Use when Codex needs to record memory into a specific module, default unspecified memory to general, decide whether content belongs in logs, topics, sops, or tools, create module directories on demand, maintain per-module index.md files, retrieve existing memory, or write SOP documents and helper scripts such as Python tools into a module directory.
---

# Memory Manager

## Overview

Manage long-term memory under `/Users/flowkehurly/.memory-data`.
Organize memory by module. Create new modules on demand. Route each item into `logs/`, `topics/`, `sops/`, or `tools/` instead of dumping everything into one file.

Use bundled scripts when they simplify filesystem setup or index maintenance:

- `scripts/bootstrap_memory_root.py` — initialize the memory root and one or more modules
- `scripts/ensure_module.py` — create or repair a single module structure
- `scripts/rebuild_index.py` — regenerate a module `index.md` from current files

Read `references/layout-and-templates.md` when you need the canonical directory layout or markdown templates.

## Apply the fixed filesystem contract

Use this fixed memory root:

- `/Users/flowkehurly/.memory-data`

Use this standard module layout for every module:

```text
<root>/<module>/
  index.md
  logs/
  topics/
  sops/
  tools/
```

Use `general` when the user does not specify a module.

Preserve the module name the user gives unless the user explicitly asks to rename or normalize it. Create the module directory immediately if it does not exist.

## Determine the target module

Follow this priority order:

1. Use the module explicitly named by the user.
2. Infer a module only when the context is unusually clear and low-risk.
3. Otherwise default to `general`.

If you default or infer, say so briefly in the reply.

## Route content to the correct location

Choose the destination by content type.

### Use `logs/` for time-based or transient capture

Write transient notes, meeting outcomes, short-lived context, or chronological event records to:

- `logs/YYYY/YYYY-MM.md`

Prefer appending a dated bullet or short subsection instead of creating many tiny files.

### Use `topics/` for durable knowledge

Write stable preferences, project background, client facts, reusable decisions, and other long-lived knowledge to:

- `topics/<topic>.md`

Prefer updating an existing topic file when the new information clearly belongs there.

### Use `sops/` for repeatable procedures

Write reusable workflows, checklists, operating procedures, or playbooks to:

- `sops/<name>.md`

Prefer linking any related scripts from the SOP.

### Use `tools/` for executable helpers

Write Python, shell, or other helper programs to:

- `tools/<name>.<ext>`

Use `tools/` only for executable artifacts. Put explanatory prose in `sops/` or `topics/`.

## Keep module indexes usable

Maintain `<module>/index.md` as the landing page for the module.

When you create, rename, or substantially revise a file in `topics/`, `sops/`, or `tools/`, update or rebuild the module index.

For pure log appends, index updates are optional. Prefer updating the recent activity section only when it materially improves navigation.

If the index is stale or inconsistent, run `scripts/rebuild_index.py` instead of hand-editing large sections.

## Write canonical markdown shapes

Use frontmatter for durable documents when it adds structure.

### Topic template

Use frontmatter like:

```yaml
---
title: <title>
module: <module>
type: topic
tags: [tag1, tag2]
updated_at: YYYY-MM-DD
---
```

### SOP template

Use frontmatter like:

```yaml
---
title: <title>
module: <module>
type: sop
tags: [tag1, tag2]
updated_at: YYYY-MM-DD
related_tools:
  - tools/<tool-name>.py
---
```

### Log format

Keep logs light. Prefer entries like:

```md
## YYYY-MM-DD HH:MM
- Record: <fact or event>
- Tags: tag1, tag2
```

Do not force heavy metadata into every log entry.

## Work efficiently with the bundled scripts

### Initialize the root

Run `scripts/bootstrap_memory_root.py` when the root is missing or when you want to create several starting modules.

Example:

```bash
python scripts/bootstrap_memory_root.py --root /Users/flowkehurly/.memory-data --modules general,工作,生活
```

### Ensure a module exists

Run `scripts/ensure_module.py` before writing into a new module or when a module looks incomplete.

Example:

```bash
python scripts/ensure_module.py --root /Users/flowkehurly/.memory-data --module 客户A
```

### Rebuild a module index

Run `scripts/rebuild_index.py` after multiple file changes, migrations, or manual edits.

Examples:

```bash
python scripts/rebuild_index.py --root /Users/flowkehurly/.memory-data --module 工作
python scripts/rebuild_index.py --root /Users/flowkehurly/.memory-data --all
```

## Handle common requests

### Record memory

- Determine the module.
- Ensure the module exists.
- Route the content to `logs/`, `topics/`, `sops/`, or `tools/`.
- Update the index when needed.

### Retrieve memory

- Start from the user-specified module when one is given.
- Check `index.md` first for navigation clues.
- Search `topics/`, `sops/`, and recent logs before assuming the memory is absent.

### Update memory

- Prefer modifying the existing topic or SOP file instead of creating duplicates.
- Merge overlapping notes when they describe the same durable fact.
- Rebuild the index after large reorganizations.

### Promote repeated work into reusable assets

When a repeated workflow appears, split it into:

1. a human-readable SOP in `sops/`
2. an executable helper in `tools/` when code would save time or reduce mistakes

## Avoid common failures

Do not put everything into `general` when the user explicitly named a module.
Do not create one-off markdown files at the module root except `index.md`.
Do not store executable code in `sops/`.
Do not create a new topic when an existing durable topic should be updated.
Do not leave indexes stale after major topic, SOP, or tool changes.
