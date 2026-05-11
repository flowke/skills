# Layout and Templates

## Canonical directory layout

```text
/Users/flowkehurly/Documents/AAA/skills/.memory-data/
  general/
    index.md
    logs/
      2026/
        2026-04.md
    topics/
    sops/
    tools/
  <module>/
    index.md
    logs/
    topics/
    sops/
    tools/
```

## Index template

```md
# 模块索引：<module>

## 模块说明
记录属于“<module>”模块的长期记忆、日志、主题、SOP 和工具。

## Topics
- 暂无

## SOPs
- 暂无

## Tools
- 暂无

## Recent Updates
- 暂无
```

## Topic template

```md
---
title: <title>
module: <module>
type: topic
tags: [tag1, tag2]
updated_at: YYYY-MM-DD
---

# <title>

## 摘要
<1-3 句摘要>

## 细节
- ...
```

## SOP template

```md
---
title: <title>
module: <module>
type: sop
tags: [tag1, tag2]
updated_at: YYYY-MM-DD
related_tools:
  - tools/<tool-name>.py
---

# <title>

## 适用场景
<何时使用>

## 步骤
1. ...
2. ...
3. ...
```

## Log entry template

```md
# YYYY-MM

## YYYY-MM-DD HH:MM
- Record: <fact or event>
- Tags: tag1, tag2
```


## Collection pattern for recurring entities

When a category starts to repeat, create a collection directory instead of scattering flat files.

```text
topics/
  people/
    index.md
    杜涔涔.md
    张三.md
```

Use this for colleagues, clients, vendors, projects, or other durable entity sets.

## Attachment patterns

If a topic needs images or supporting files, keep them next to the topic in one of these shapes.

### File + assets folder

```text
topics/
  people/
    杜涔涔.md
    杜涔涔.assets/
      avatar.png
      org-chart.jpg
```

### Dedicated topic folder

```text
topics/
  people/
    杜涔涔/
      index.md
      avatar.png
      notes.md
```

Choose the simpler file form first. Promote to a folder when the topic accumulates assets or multiple related notes.


## Remodeling prompt patterns during capture

When new memory suggests a better structure, surface the suggestion immediately and briefly.

Examples:

- `topics/` 下连续出现多个同事姓名文件 → 建议升级为 `topics/同事/index.md` + 每人一个文档
- 单个 `客户.md` 内开始堆积多个客户条目 → 建议拆为 `topics/客户/<客户名>.md`
- 某个主题开始持续附带图片或附件 → 建议为该主题建立 `.assets/` 邻接目录，或升级为专题文件夹
- 某类流程重复出现并伴随脚本 → 建议拆成 `sops/` + `tools/` 配套结构

Use the proposal-first style for remodels that would move, rename, split, or merge existing files.


## Path wording in replies

When confirming memory writes, prefer concise relative references instead of absolute paths.

Examples:

- `已记录到 工作/topics/杜涔涔.md`
- `已追加到 工作/logs/2026/2026-04.md`
- `建议迁移到 topics/同事/index.md + 每位同事一个文档`

Use an absolute path only when the file location depends on this specific computer and the exact machine path matters. When doing so, say that explicitly.


## Shared vs repo-scoped memory

When memory is shared across workspaces, avoid unanchored wording like `当前仓库对应的项目是 ...`.

Prefer a two-step model:

1. Record repository identity in `topics/repos/<repo>.md`
2. Record project facts in `topics/projects/<project>.md`
3. Link them only when the binding is confirmed

Suggested repo note shape:

```md
# <repo-name>

- remote: <url>
- role: <what this repository is for>
- default branch: <branch>
- repo root clue: <directory or identifying clue>
- binding status: confirmed / inferred / unknown
```

Suggested project note wording:

- `以下内容描述项目“超级教研”的发布资料，不自动代表当前打开仓库就是该项目仓库。`
- `若要绑定到具体仓库，请补充 repo 名、remote URL、目录名或 README 证据。`


## General pattern: hidden-context assertions

This is the reusable pattern to detect during memory capture:

- The statement sounds durable.
- But its truth actually depends on some hidden `current` context.
- That context is not written down.
- If copied into shared memory, the statement becomes misleading.

Typical domains include repositories, browser pages, selected nodes, local files, accounts, permissions, environments, and temporary UI state.

Preferred handling:

1. name the scope
2. capture the anchor facts
3. downgrade certainty if needed
4. store the durable fact separately from the volatile context

Bad:

- `当前仓库就是超级教研`
- `这个页面就是发布页`
- `当前账号有线上权限`
- `本地已经装好 CLI 了`

Better:

- `项目“超级教研”的资料如下；当前仓库是否属于该项目仍待确认。`
- `当前浏览器页面疑似发布页；建议记录标题、URL、系统名后再沉淀。`
- `某次操作中使用的账号具备线上权限；若要共享复用，应补充账号身份与权限范围。`
- `某台电脑已安装 CLI；若要共享复用，应补充机器标识与验证方式。`
