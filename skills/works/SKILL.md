---
name: works
description: Orchestrate project work from discussion through delivery and memory backfill. Prefer explicit invocation. Use when Codex needs to accept ambiguous or concrete requirements, organize user-provided materials into one evolving discussion document, restructure discussion by topic or object when boundaries become clear, and progressively turn project conversation into actionable delivery context.
---

# works

进入一种面向项目工作的编排模式。

当前优先完善三件事：**Discuss**、**Delivery** 和 **Memory**。

## Overview

用这个 skill 承接项目需求讨论，不把内容按聊天时间顺序堆积，而是整理成一个可持续演化的讨论文档。

默认优先显式触发，不主动自动进入。

默认先维护一个统一讨论页；当用户明确要求分主题，或内容已经自然形成边界时，再把已有内容重组为主题化结构，而不是从头重写。

## Current Scope

当前版本已经覆盖 `Discuss`、`Delivery` 和 `Memory` 三种工作模式，但默认仍以 `Discuss` 为主入口：
- `Discuss`：接需求、接材料、整理讨论结构、支持后续按主题重组
- `Delivery`：先查相关 memory，再锁定本轮交付范围，推进代码落地，并为验收提供基线
- `Memory`：把 discussion / delivery 中稳定、可复用的内容沉淀到 `docs-works/memory/`

## Mode routing

调用 `$works` 时，先判断当前最适合进入哪一种模式：
- 如果用户还在描述需求、补材料、补限制，或问题仍然偏发散，进入 `Discuss`
- 如果用户已经明确要开始实现、落地、修某一块，进入 `Delivery`
- 如果用户明确要沉淀规则、约束、做法、事实，进入 `Memory`
- 如果信号不明确，默认先进入 `Discuss`，不要抢跑到 `Delivery` 或 `Memory`

## Execution loop

进入 `$works` 后，默认按这个最小闭环执行：
1. 先判断当前所处模式（Discuss / Delivery / Memory）
2. 在当前 workspace 根目录下定位或创建 `docs-works/` 相关结构
3. 只读取和本轮模式直接相关的文档，而不是全量扫所有 reference
4. 只更新本轮最必要的 1-2 个文件，避免一次建太多页
5. 回复开头先用一句话说明本轮已落文档内容
6. 然后只给当前结论和下一步建议，不展开长过程

## References

按模式读取 reference，避免一次加载全部材料：

### Discuss
优先读取：
- `references/discuss-mode.md`
- `references/document-organization.md`
- `references/unified-discussion-template.md`
- `references/topic-template.md`
- `references/migration-rules.md`

### Delivery
优先读取：
- `references/delivery-mode.md`
- `references/document-organization.md`
- `references/delivery-brief-template.md`
- `references/delivery-progress-template.md`
- `references/delivery-acceptance-template.md`
- `references/memory-mode.md`（仅用于筛选相关 memory）

### Memory
优先读取：
- `references/memory-mode.md`
- `references/memory-entry-template.md`
- `references/document-organization.md`
