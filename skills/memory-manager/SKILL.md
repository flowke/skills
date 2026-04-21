---
name: memory-manager
description: Structured memory capture, retrieval, update, and organization using the unified filesystem memory root at /Users/flowkehurly/Documents/AAA/skills/.memory-data. Use when Codex needs to record memory into a specific module, default unspecified memory to general, decide whether content belongs in logs, topics, sops, or tools, create module directories on demand, maintain per-module index.md files, retrieve existing memory, or write SOP documents and helper scripts such as Python tools into a module directory.
---

# Memory Manager

## Overview

Manage long-term memory under `/Users/flowkehurly/Documents/AAA/skills/.memory-data`.
Organize memory by module. Create new modules on demand. Route each item into `logs/`, `topics/`, `sops/`, or `tools/` instead of dumping everything into one file. When new information clearly belongs to an existing category, entity set, or durable structure, organize it immediately instead of creating another flat standalone note.

Use bundled scripts when they simplify filesystem setup or index maintenance:

- `scripts/bootstrap_memory_root.py` — initialize the memory root and one or more modules
- `scripts/ensure_module.py` — create or repair a single module structure
- `scripts/rebuild_index.py` — regenerate a module `index.md` from current files

Read `references/layout-and-templates.md` when you need the canonical directory layout or markdown templates.

## Apply the fixed filesystem contract

Use this fixed memory root:

- `/Users/flowkehurly/Documents/AAA/skills/.memory-data`

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

## Run a lightweight remodeling check during capture

Before writing new memory, quickly check whether the incoming information reveals a better organization model. Treat this as part of memory capture, not as a separate cleanup task.

Look for signals such as:

- several flat topic files that obviously belong to the same class
- one topic accumulating many distinct entities
- repeated attachments or images that need adjacency to the related note
- repeated updates that would be easier to manage as a collection plus per-entity files
- a topic that has outgrown a single markdown file and should become a folder

When a clearer structure is apparent, proactively say so in the reply. Keep the suggestion short and concrete. Example: "This looks like the start of a colleagues collection. I recommend moving from `topics/杜涔涔.md` to `topics/同事/index.md` + one file per colleague."

Prefer proposing remodeling before executing it when the change would move or rename existing files. You may silently apply no-regret structure fixes only when they do not change meaning and do not risk surprising the user.

## Route content to the correct location

Choose the destination by content type.


## Organize proactively when structure is obvious

Do not treat every new memory as an isolated file. When the new memory clearly belongs inside an existing structure, organize it during capture.

Use these rules:

1. If the memory belongs to an existing topic, update that topic instead of creating a sibling file.
2. If repeated items belong to the same entity class, create a collection directory and index for that class.
3. If one entity is likely to accumulate more facts over time, give that entity its own file.
4. If multiple entities are tiny and unlikely to grow, they may temporarily live in one collection note, but prefer splitting them once the category becomes important.
5. Prefer shallow, interpretable structure over many unrelated top-level markdown files.

### Use collection-plus-entity structure for recurring entities

For recurring entity types such as colleagues, people, clients, projects, or vendors, prefer this pattern under `topics/`:

```text
topics/
  people/
    index.md
    杜涔涔.md
    张三.md
```

Or use another clear category name such as `topics/同事/`, `topics/clients/`, or `topics/projects/`.

Use `index.md` in that collection directory to summarize and link the entity files.
Use one file per durable entity when that entity can reasonably accumulate profile, preferences, relationships, images, or history.

### Handle images and other attachments without breaking structure

If a memory includes images or other supporting files, keep them adjacent to the organized topic or collection instead of leaving them loose at the module root.

Prefer patterns like:

```text
topics/
  people/
    index.md
    杜涔涔.md
    杜涔涔.assets/
      profile.png
```

Or, when a topic becomes large enough to justify its own folder:

```text
topics/
  people/
    杜涔涔/
      index.md
      profile.png
      notes.md
```

Choose the simpler shape first. Promote a single markdown file into a dedicated folder only when attachments or scale make that worthwhile.


### Use `logs/` for time-based or transient capture

Write transient notes, meeting outcomes, short-lived context, or chronological event records to:

- `logs/YYYY/YYYY-MM.md`

Prefer appending a dated bullet or short subsection instead of creating many tiny files.

### Use `topics/` for durable knowledge

Write stable preferences, project background, client facts, reusable decisions, and other long-lived knowledge to:

- `topics/<topic>.md`
- `topics/<collection>/index.md` plus `topics/<collection>/<entity>.md` for recurring entity sets

Prefer updating an existing topic file when the new information clearly belongs there. When several memories belong to the same class of durable entities, prefer a collection directory with an index and one file per entity over many unrelated top-level files.

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


## Prefer portable path references in replies

When describing where memory was written or should be updated, do not default to absolute filesystem paths in the final reply.

Prefer path styles like:

- `工作/topics/杜涔涔.md`
- `topics/同事/杜涔涔.md`
- `sops/知音楼给同事发消息流程.md`

Use the smallest path that is still unambiguous in context.
Prefer paths relative to the memory root or relative to the current module.

Only use an absolute path when the location is meaningfully machine-specific and the exact host path matters. In that case, explicitly say that the path is machine-specific before giving it.

Examples:

- Preferred: `已记录到 工作/topics/同事/杜涔涔.md`
- Preferred: `建议把它整理到 topics/同事/index.md + 每位同事一个文档`
- Machine-specific exception: `这张图片位于这台电脑的本地目录，因此我用绝对路径说明：/Users/.../Screenshots/profile.png`

Do not clutter normal memory capture confirmations with absolute paths.

## Work efficiently with the bundled scripts

### Initialize the root

Run `scripts/bootstrap_memory_root.py` when the root is missing or when you want to create several starting modules.

Example:

```bash
python scripts/bootstrap_memory_root.py --root /Users/flowkehurly/Documents/AAA/skills/.memory-data --modules general,工作,生活
```

### Ensure a module exists

Run `scripts/ensure_module.py` before writing into a new module or when a module looks incomplete.

Example:

```bash
python scripts/ensure_module.py --root /Users/flowkehurly/Documents/AAA/skills/.memory-data --module 客户A
```

### Rebuild a module index

Run `scripts/rebuild_index.py` after multiple file changes, migrations, or manual edits.

Examples:

```bash
python scripts/rebuild_index.py --root /Users/flowkehurly/Documents/AAA/skills/.memory-data --module 工作
python scripts/rebuild_index.py --root /Users/flowkehurly/Documents/AAA/skills/.memory-data --all
```

## Handle common requests

### Record memory

- Determine the module.
- Ensure the module exists.
- Run a quick remodeling check and surface any strong organization suggestion.
- Check whether the content belongs in an existing topic or collection.
- Route the content to `logs/`, `topics/`, `sops/`, or `tools/`.
- Update the index when needed.
- In the final reply, prefer relative or module-scoped paths instead of absolute paths unless the location is machine-specific.

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
Do not keep adding top-level topic files when a clear collection such as `people/`, `clients/`, or `projects/` has emerged.
Do not miss obvious opportunities to tell the user that the knowledge model should be upgraded.
Do not silently move or rename large existing structures unless the user asked for that change or the change is trivially safe.
Do not use absolute paths in ordinary memory confirmations when a relative path would be clear enough.
Do not leave images or attachments loose when they can be grouped next to the relevant topic or entity.
Do not leave indexes stale after major topic, SOP, or tool changes.
