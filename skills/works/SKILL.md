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
- `Discuss`：接需求、接材料、整理讨论结构，并把未决点区分为关键待确认问题与非阻塞开放问题
- `Implement`：围绕某项代码实现持续推进，可承接 `Discuss`，也可直接承接外部需求文档、issue、设计稿或已有任务说明

## Mode routing

调用 `$works` 时，先判断当前最适合进入哪一种模式：
- 如果用户还在描述需求、补材料、补限制，或问题仍然偏发散，进入 `Discuss`
- 如果当前仍存在会影响下一步动作的**关键待确认问题**，或 discussion / topic 仍处于 `待确认`、`已暂停` 等未收口状态，默认继续停留在 `Discuss`
- 如果 `Discuss` 下已经存在多个 topic，默认先判断当前是否已经可进入 `Implement Lock`；如果还不能，就继续推进 `Discuss`，不必为了选 topic 额外建立复杂优先级机制
- 如果剩余问题已经被明确降级为**非阻塞假设、默认实现约定或后续版本项**，且本轮目标、范围边界和主要约束已经足够清晰，可以进入 `Implement` 先做 `Lock`
- 如果用户已经明确要开始实现、落地、修某一块，且需求来源足以支撑本轮 `Lock`，进入 `Implement`
- 如果信号不明确，默认先进入 `Discuss`

补充约束：
- `可进入 Implement Lock` 不等于可直接开始 `Build`
- 只要仍存在会阻止锁定 brief 或改变本轮范围 / 约束 / 验收标准的关键未决点，默认不要切到 `Build`
- 若当前已在 `Implement`，但新出现的关键未决点开始影响本轮范围、方案或验收标准，应优先回到 `Discuss` 收敛，或至少先停在 `待收口上下文 / 待锁定`

## Execution loop

进入 `$works` 后，默认按这个最小闭环执行：
1. 先判断当前所处模式（Discuss / Implement）
2. 在当前 workspace 根目录下定位或创建 `docs-works/` 相关结构
3. 只读取和本轮模式直接相关的文档；如果是模式切换，只补读切换所需的直接来源文档
4. 先按当前模式更新文档中的关键字段，再形成回复结论
5. 回复开头先用一句话说明本轮已落文档内容
6. 然后只给当前阶段 / 状态、当前结论或阻塞、以及下一步建议，不展开长过程；如果下一步已经可被合理缩成 1-3 个候选方案，应在同一轮直接列出推荐方案，而不是把方案延后到“下一条再说”

## Reply contract

使用 `$works` 回复时，默认遵循以下约束：
- 先以文档中的最新结果为准，再组织回复
- 不要在 `Discuss` 中越级写成直接开始 `Build`
- 不要在 `Implement` 仍未达到 `可构建` 时写成可直接进入 `Build`
- 如果当前仍有关键阻塞项，回复中的下一步建议应优先体现继续收敛、补确认、解除阻塞或缩小范围
- 如果下一步已经收敛到某个可直接拍板的关键问题，默认在同一条回复里直接给出 1 个推荐方案，必要时附 1-2 个备选，而不是只预告“如果你愿意，下一条我再给方案”
- 在 `Discuss` 中，若已能形成推荐方案，回复默认压缩成固定骨架：已落文档 + 当前阶段/状态 + 当前唯一关键结论或阻塞 + 下一步建议（推荐 / 备选 / 一句确认）
- 如果 discussion 下存在多个 topic，而本轮继续推进其中一个，默认只需说明它与“暂不能进入 `Implement Lock`”之间的关系；不必展开复杂排序理由
- 如果建议进入 `Implement Lock` 或 `Build`，应确保前置条件已在对应文档中成立
- 如果某项新确认的内容会影响多个 topic 或多个板块，默认只在同一个父 topic / 父板块范围内做同轮联动更新，并同步必要的总页字段；不要自动跨到其他父 topic，除非用户主动要求

## References

按模式读取对应文件：
- `references/discuss-mode.md`
- `references/implement-mode.md`
