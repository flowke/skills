---
name: memory-manager
description: Dual-mode memory skill for structured capture and retrieval/application using the unified filesystem memory root at /Users/flowkehurly/Documents/AAA/skills/.memory-data. Use when Codex needs to record memory into a specific module, or retrieve existing memory/SOPs/tools as working context for the current task without writing new memory by default.
---

# Memory Manager

## Overview

Manage long-term memory under `/Users/flowkehurly/Documents/AAA/skills/.memory-data`.
This skill has **two equal operating modes**:

1. **Capture mode**: record, organize, update, and remodel memory
2. **Recall/apply mode**: retrieve memory, SOPs, and tools as context for the current task, and optionally execute the workflow the user asked for

Do **not** assume that enabling this skill means the user wants to write memory.
When the user asks to solve a task, answer a question, follow an existing SOP, or provide remembered context, prefer **recall/apply mode** unless the user clearly asked to store or update memory.

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

## Choose the operating mode before acting

Always classify the user's intent **before** doing any filesystem write.
The first job of this skill is not "store memory". The first job is "decide whether this turn is about capture or about recall/application."

### Mode A — Capture / store / update memory

Use capture mode only when the user clearly wants to persist or reshape memory. Typical cues:

- `记一下` / `记住` / `存一下` / `帮我沉淀`
- `写入 memory` / `更新记忆` / `补充到模块`
- `把这个流程整理成 SOP`
- `把这个脚本沉淀到 tools`
- `把这条信息长期保存`

In this mode, writing files is expected.

### Mode B — Recall / use / execute from memory

Use recall/apply mode when the user wants existing memory, SOPs, or tools to help with the current task. Typical cues:

- `查一下之前记过没有`
- `把相关背景给我` / `给 agent 提供上下文`
- `按之前的流程做` / `调用之前的 SOP`
- `看看这个模块里有没有现成工具`
- `根据已有记忆继续执行`
- `把能用的工作流提出来`

In this mode, **do not create or update memory by default**.
The goal is to fetch context, summarize it, link it to the current task, and if requested, execute the remembered workflow or tool.

### Default disambiguation rule

If the user intent is ambiguous, prefer **recall/apply mode** over capture mode.
Only write memory when the user explicitly asks to persist, update, organize, or promote information into long-term memory.

### Conversation heuristic: memory verbs vs direct task commands

In normal conversation, treat wording like `加下...`、`记一下...`、`沉淀一下...`、`补充到...` as a strong signal for **capture mode**.
These phrases usually mean the user wants the information written into memory.

By contrast, when the user gives a **direct task command**, treat it as **recall/apply mode** by default, not as a memory-write request.
Typical examples:

- `发线上`
- `按之前流程走`
- `继续做这个`
- `给我相关背景`
- `查下有没有现成 SOP`

These are usually execution or retrieval instructions.
They mean: use remembered context, workflow, or tools **for the live task**.
They do **not** mean: save a new memory entry.

### Imperative execution rule

If the user gives a short imperative instruction and it does not contain explicit memory-writing verbs, interpret it as a request to **execute** using existing memory when relevant.
For example, `发线上` should be understood as: retrieve the relevant SOP/context if needed, then carry out the release-related workflow — not `write that the user wants to发线上` into memory.

### Few-shot examples for Chinese conversational intent

Use these examples as the default interpretation pattern in normal Chinese conversation.

#### Example 1 — explicit memory write

- User: `加下这个客户偏好：他们更喜欢周三下午开会。`
- Interpret as: **record memory**
- Why: `加下` is a memory-writing cue
- Action: write or update the relevant topic/log in the correct module
- Not this: do not merely summarize it for the live task and stop

#### Example 2 — explicit memory write with “沉淀”

- User: `把这次发版流程沉淀一下，后面复用。`
- Interpret as: **record memory** or **promote into SOP**
- Why: `沉淀一下` signals durable storage, often into `sops/` and possibly `tools/`
- Action: organize the workflow into reusable assets

#### Example 3 — direct execution command

- User: `发线上`
- Interpret as: **execute a remembered workflow/tool**
- Why: this is a direct imperative command, not a memory-writing request
- Action: retrieve release-related SOP/context if needed, then continue execution
- Not this: do not create a memory entry like `用户要发线上`

#### Example 4 — direct execution with implied history

- User: `按之前流程走`
- Interpret as: **execute a remembered workflow/tool**
- Why: the user is referring to an existing remembered workflow
- Action: find the relevant SOP/process and apply it to the live task

#### Example 5 — context retrieval

- User: `把这个项目相关背景给我，我要给 agent 上下文。`
- Interpret as: **retrieve memory for context**
- Why: the request is to fetch and summarize existing memory for current use
- Action: gather relevant topics/SOPs/logs and present actionable context
- Not this: do not write a new note unless separately asked

#### Example 6 — retrieval plus execution

- User: `查一下之前怎么发的，然后照着做。`
- Interpret as: **retrieve first, then execute**
- Why: the first half asks for recall, the second half asks for action
- Action: locate the prior workflow, summarize the essential constraints, then proceed

#### Example 7 — update existing memory

- User: `把刚才那个 SOP 再补两条注意事项。`
- Interpret as: **update memory**
- Why: the user explicitly asks to modify an existing remembered asset
- Action: update the SOP rather than creating a duplicate

#### Example 8 — ambiguous short request

- User: `这个也加进去`
- Interpret as: usually **record memory**, but verify the target if unclear
- Why: `加进去` is usually a storage/update cue, but the destination may be ambiguous
- Action: if the target memory object is obvious, update it; otherwise ask a short clarification question

### Hard rule

**Using this skill is not itself permission to write memory.**
Skill activation only means memory may be relevant. The user's instruction still determines whether the task is capture or recall/application.

### Fast decision tree

Use this compact decision tree before acting:

1. Does the user explicitly ask to `记`, `加`, `沉淀`, `补充`, `更新记忆`, or `写入`?
   - Yes → **capture/update memory**
   - No → continue
2. Does the user ask for background, prior notes, remembered constraints, SOPs, or existing tools?
   - Yes → **retrieve memory for context**
   - If they also ask to act, then **retrieve first, then execute**
3. Is the message a direct imperative task command like `发线上`, `继续做`, `按流程来`, `处理一下`?
   - Yes → **execute using remembered context if relevant**
4. If still ambiguous:
   - prefer **recall/apply**
   - avoid writing memory unless the user explicitly asks for persistence

## What recall/apply mode should do

When operating in recall/apply mode, follow this order:

1. identify the likely module or default to `general` only for search scope
2. check `index.md` for navigation clues
3. inspect relevant `topics/`, `sops/`, `tools/`, and recent logs
4. extract only the memory relevant to the current task
5. present it as actionable context, not as a dump of notes
6. if the user asked to perform the workflow, follow the SOP or use the tool
7. do not write back new memory unless the user separately asks to record the outcome

### Response shape in recall/apply mode

Prefer outputs like:

- `我找到了 2 条相关记忆，核心结论如下...`
- `相关 SOP 在 sops/...，我将按这个流程继续执行`
- `现有 tools/... 可以直接用于这个任务，我先调用它`

Avoid outputs that imply storage when the user only asked for retrieval or execution.

### Output contract by mode

Match the reply style to the chosen mode.
The assistant should sound different in each mode.

#### If mode = record/update memory

Prefer replies like:

- `已记录到 topics/...`
- `已更新现有 SOP：sops/...`
- `我顺手整理成了 SOP + tool，位置如下...`

#### If mode = retrieve memory for context

Prefer replies like:

- `我找到了相关背景，核心有 3 点...`
- `之前记过，关键约束如下...`
- `有一份相关 SOP / topic，可以作为这次任务上下文...`

Do not end with a storage confirmation in this mode.

#### If mode = execute a remembered workflow/tool

Prefer replies like:

- `我先按之前的 SOP 检查一遍，然后继续执行。`
- `我找到了可复用的流程，先照这个做。`
- `现有工具可直接处理这个任务，我现在开始执行。`

Do not respond as if the main result were memory retrieval only when the user asked for action.

### Anti-patterns to avoid in replies

Bad patterns:

- User: `发线上` → Assistant: `已为你记录一条关于发线上的记忆`
- User: `给我这个项目背景` → Assistant: `已保存项目背景到 general/logs/...`
- User: `按之前 SOP 做` → Assistant: `我帮你沉淀了一份新的 SOP`

Preferred patterns:

- User: `发线上` → Assistant: `我先找相关发版 SOP / 约束，然后继续执行。`
- User: `给我这个项目背景` → Assistant: `我找到了相关背景，关键信息如下...`
- User: `按之前 SOP 做` → Assistant: `我定位到对应 SOP 了，接下来按它执行。`

## Detect context-dependent assertions before storing shared memory

Treat this as a general pattern, not a repo-only special case. Before saving memory, check whether the statement depends on a hidden `current ...` context that would become ambiguous when reused in another workspace, machine, app state, or conversation.

Common risky patterns include claims about:

- the current repository, workspace, project, or branch
- the current page, selected node, open file, or focused app
- the current account, tenant, environment, or permission context
- the local machine, local downloads, local screenshots, or local tool installation
- the current conversation state or temporary user intent

### Recognize the bad pattern

Watch for wording such as:

- `当前仓库是 ...`
- `当前项目是 ...`
- `这里就是 ...`
- `这个页面对应 ...`
- `当前账号有权限 ...`
- `本地已经安装了 ...`
- `当前选择的是 ...`

The problem is not the domain. The problem is that the claim relies on hidden context and would be misleading once copied into shared memory.

### Repair the pattern

When you detect this pattern, do one of these before storing the memory:

1. **Anchor the claim** with explicit context facts.
2. **Downgrade the claim** into a tentative or scoped statement.
3. **Split the memory** into durable facts plus context-specific evidence.
4. **Ask for or gather missing anchors** when the distinction matters.

Examples:

- Instead of `当前仓库对应的项目是 超级教研` → `项目“超级教研”的资料如下；是否对应当前仓库，需根据 repo 名、remote、README 或目录线索确认。`
- Instead of `这个页面就是发布页` → `当前浏览器页面疑似发布页；建议补充页面标题、URL 或系统名称后再固化为共享记忆。`
- Instead of `当前账号可以发线上` → `已知在某次会话中使用的账号具备发线上能力；若要沉淀为共享记忆，应补充账号身份、系统范围和权限证据。`
- Instead of `本地已经装了某工具` → `在某台电脑上已安装某工具；若要复用，应记录机器标识、安装位置或安装验证方式。`

### Use the right storage shape

When a claim mixes durable knowledge with volatile context, separate them:

- durable fact → store in `topics/` or `sops/`
- context anchor or evidence → store alongside it as scoped notes, links, or explicit caveats
- machine-specific detail → keep clearly marked as machine-scoped

Do not promote a context-bound observation into a global shared fact unless the necessary anchors are present.


## Model shared memory with explicit scope

Treat shared memory as portable context, not as an implicit snapshot of the currently opened workspace. Before writing repo-related, machine-related, or environment-related facts, identify the scope of the memory.

Use these scope buckets:

- **shared durable facts**: people, SOPs, domain knowledge, project facts that remain meaningful outside one repo
- **repo-scoped facts**: repository identity, remote URL, default branch, repo-specific scripts, release rules tied to one concrete repo
- **machine-scoped facts**: local absolute paths, downloaded files, desktop screenshots, host-specific tool locations

Do not mix these scopes casually in one sentence.

### Never use deictic repo wording without an anchor

Avoid phrases like:

- `当前仓库对应的项目是 ...`
- `这个仓库就是 ...`
- `这里的项目是 ...`

unless the memory also names the concrete repository identity that justifies the claim.

Prefer anchored wording such as:

- `仓库 \`skills\`（remote: \`https://github.com/flowke/skills.git\`）是一个 skills 管理仓库。`
- `项目“超级教研”的发布资料记录如下；是否为当前打开仓库，需根据 repo root、remote、目录名或 README 再确认。`

### Build repo context before writing repo conclusions

When a memory mentions a repository, collect and record the repo context first whenever possible:

1. repo name or directory name
2. remote URL
3. default branch or current branch when relevant
4. repo root or other identifying clues
5. whether the conclusion is confirmed, inferred, or still unknown

Prefer storing repo identity in a dedicated collection such as `topics/repos/`. Then let project or SOP notes refer to that repo context instead of claiming that the current workspace automatically matches the project.

When the repo binding is not known, say so explicitly.


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

### First: classify the request

Before taking action, classify the turn into one of these buckets:

1. **record memory**
2. **retrieve memory for context**
3. **execute a remembered workflow/tool**
4. **update or remodel existing memory**

Do not skip this classification step. It prevents accidental writes.

Quick interpretation rule:

- wording like `加下` / `记一下` / `沉淀` / `补充到记忆` → usually **record memory**
- direct task imperatives like `发线上` / `继续做` / `按之前流程走` → usually **execute a remembered workflow/tool**
- requests like `给我背景` / `查一下之前怎么做` → usually **retrieve memory for context**

If one request mixes retrieval and execution, handle it in that order: **retrieve first, then execute**.
Do not append a storage step unless the user explicitly asks for it.

### Record memory

- Determine the module.
- Ensure the module exists.
- Determine the scope: shared, repo-scoped, machine-scoped, account-scoped, app-scoped, or other context-scoped.
- Run a context-dependency check: does this statement rely on hidden `current` context?
- If yes, anchor it, downgrade it, split it, or gather the missing context before storing it as shared memory.
- Run a quick remodeling check and surface any strong organization suggestion.
- Check whether the content belongs in an existing topic or collection.
- Route the content to `logs/`, `topics/`, `sops/`, or `tools/`.
- Update the index when needed.
- In the final reply, prefer relative or module-scoped paths instead of absolute paths unless the location is machine-specific.

### Retrieve memory for context

- Start from the user-specified module when one is given.
- Check `index.md` first for navigation clues.
- Search `topics/`, `sops/`, `tools/`, and recent logs before assuming the memory is absent.
- Summarize only the parts that are relevant to the live task.
- Present the result as working context, recommended next steps, or candidate assets to use.
- Do not write any new memory unless the user explicitly asks for persistence.

### Execute a remembered workflow or tool

- Retrieve the relevant SOP and/or tool first.
- Tell the user briefly what remembered asset you are using.
- Apply the SOP steps or run the tool for the current task.
- Treat the memory as operational context, not as something to rewrite.
- Only write back outcomes when the user explicitly asks to record the result, or when updating the memory asset itself is the requested task.

### Update memory

- Prefer modifying the existing topic or SOP file instead of creating duplicates.
- Merge overlapping notes when they describe the same durable fact.
- Rebuild the index after large reorganizations.

### Promote repeated work into reusable assets

When a repeated workflow appears, split it into:

1. a human-readable SOP in `sops/`
2. an executable helper in `tools/` when code would save time or reduce mistakes

## Avoid common failures

Do not treat every invocation of this skill as a memory-write request.
Do not assume `use $memory-manager` means `store this`.
Do not write memory in recall/apply mode unless the user explicitly asks to persist the result.
Do not answer a retrieval or execution request with a storage confirmation.
Do not reinterpret a direct command like `发线上` or `继续做` as `record this intent into memory`.
Do not miss the distinction between **memory verbs** (`记一下`, `沉淀一下`) and **execution verbs** (`发线上`, `处理一下`, `按流程做`).
Do not put everything into `general` when the user explicitly named a module.
Do not create one-off markdown files at the module root except `index.md`.
Do not store executable code in `sops/`.
Do not create a new topic when an existing durable topic should be updated.
Do not keep adding top-level topic files when a clear collection such as `people/`, `clients/`, or `projects/` has emerged.
Do not miss obvious opportunities to tell the user that the knowledge model should be upgraded.
Do not silently move or rename large existing structures unless the user asked for that change or the change is trivially safe.
Do not use absolute paths in ordinary memory confirmations when a relative path would be clear enough.
Do not write context-scoped conclusions as if they were globally true when the needed anchors have not been captured.
Do not use phrases like `当前仓库就是...`, `当前项目是...`, `这个页面就是...`, or `当前账号可以...` in shared memory unless the underlying context is explicitly identified and the claim is justified.
Do not leave images or attachments loose when they can be grouped next to the relevant topic or entity.
Do not leave indexes stale after major topic, SOP, or tool changes.
