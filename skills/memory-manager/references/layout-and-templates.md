# Layout and Templates

## Canonical directory layout

```text
/Users/flowkehurly/.memory-data/
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
