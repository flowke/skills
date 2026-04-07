---
name: works
description: Orchestrate project work from discussion through implementation. Prefer explicit invocation. Use when Codex needs to accept ambiguous or concrete requirements, organize user-provided materials into one evolving discussion document, restructure discussion by topic or object when boundaries become clear, and progressively turn project conversation into actionable implementation context.
---

# works

进入一种面向项目工作的编排模式。

当前优先完善两件事：**Discuss** 和 **Implement**。

## Overview

`$works` 负责把一项工作按阶段组织起来，而不是把内容按聊天顺序堆积；其中 `Discuss` 用来收敛需求，`Implement` 用来维护实现推进，二者可以衔接，也可以独立存在。

默认优先显式触发，不主动自动进入。

## Current Scope

当前版本覆盖两种工作模式，但默认仍以 `Discuss` 为主入口：
- `Discuss`：接需求、接材料、整理讨论结构
- `Implement`：围绕某项代码实现持续推进，可承接 `Discuss`，也可直接承接外部需求文档、issue、设计稿或已有任务说明

## Mode routing

调用 `$works` 时，先判断当前最适合进入哪一种模式：
- 如果用户还在描述需求、补材料、补限制，或问题仍然偏发散，进入 `Discuss`
- 如果用户已经明确要开始实现、落地、修某一块，或已经有现成需求材料并要进入代码推进，进入 `Implement`
- 如果信号不明确，默认先进入 `Discuss`

## Execution loop

进入 `$works` 后，默认按这个最小闭环执行：
1. 先判断当前所处模式（Discuss / Implement）
2. 在当前 workspace 根目录下定位或创建 `docs-works/` 相关结构
3. 只读取和本轮模式直接相关的文档
4. 回复开头先用一句话说明本轮已落文档内容
5. 然后只给当前结论和下一步建议，不展开长过程

## References

按模式读取对应文件：
- `references/discuss-mode.md`
- `references/implement-mode.md`
