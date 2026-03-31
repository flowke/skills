---
name: works
description: Orchestrate project work from discussion through delivery and memory backfill. Use when Codex needs to accept ambiguous or concrete requirements, organize user-provided materials into one evolving discussion document, restructure discussion by topic or object when boundaries become clear, and progressively turn project conversation into actionable delivery context.
---

# works

进入一种面向项目工作的编排模式。

当前优先完善三件事：**Discuss**、**Delivery** 和 **Memory**。

## Overview

用这个 skill 承接项目需求讨论，不把内容按聊天时间顺序堆积，而是整理成一个可持续演化的讨论文档。

默认先维护一个统一讨论页；当用户明确要求分主题，或内容已经自然形成边界时，再把已有内容重组为主题化结构，而不是从头重写。

## Current Scope

当前版本先聚焦 `Discuss`，其余模式后续再补：
- `Discuss`：接需求、接材料、整理讨论结构、支持后续按主题重组
- `Delivery`：锁定本轮交付范围，推进代码落地，并为验收提供基线
- `Memory`：把 discussion / delivery 中稳定、可复用的内容沉淀到 `docs-works/memory/`

## Discuss

### Goal

把零散需求、补充说明和相关材料，整理成可继续推进的讨论结构。

### Default behavior

1. 先维护一个统一讨论页。
2. 不按时间顺序记录聊天，而是按讨论对象组织内容。
3. 当对象边界还不清楚时，先按较粗粒度整理。
4. 当用户要求分主题，或主题边界自然出现时，再重组为主题化结构。
5. 保留跨主题问题，不要把它们硬塞进某个主题。
6. 在讨论中承担轻度主持职责：帮助聚焦、分流、补洞、推进下一步。
7. 回复保持简洁；没有特别必要时，不展开解释原因。
8. 一次优先给 2-3 个可选项或建议，不给过长清单。
9. 边讨论边落文档；每轮回复开头先用一句话说明本轮哪些内容已经落入文档，只让用户知道已落文档即可。

### Output checklist

每轮 Discuss 至少产出：
- 当前讨论目标或背景
- 已有材料与补充输入
- 当前理解或阶段性结论
- 待确认问题
- 下一步建议

### Transition rule

当满足以下任一条件时，可以结束当前 Discuss：
- 已经形成清晰讨论结构
- 已经可以进入后续交付规划
- 当前主要缺少新材料或用户确认

## References

需要执行 `Discuss` 时，优先读取：
- `references/discuss-mode.md`
- `references/document-organization.md`
- `references/unified-discussion-template.md`
- `references/delivery-brief-template.md`
- `references/delivery-mode.md`
- `references/delivery-progress-template.md`
- `references/delivery-acceptance-template.md`
- `references/memory-mode.md`
- `references/memory-entry-template.md`
