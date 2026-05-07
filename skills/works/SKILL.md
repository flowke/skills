---
name: works
description: Orchestrate project work from requirements discussion through implementation and acceptance. Prefer explicit invocation. Use when Codex needs to organize original requirements, requirement refinement, contextual materials, implementation ideas, progress tracking, handoff-ready implementation docs, or acceptance checks.
---

# works

进入一种面向项目工作的编排模式。

`$works` 负责把工作从需求讨论推进到实施和验收，而不是把内容按聊天顺序堆积。

## Overview

核心链路：

```text
Discuss → Implement → Acceptance
```

- `Discuss`：整理需求来源、原始需求、需求细化、上下文资料、实现思路和关键待确认
- `Implement`：对某个 discussion 或 topic 进行实施，维护 handoff-ready 的 `progress.md`
- `Acceptance`：对照 progress 逐项验收，并把问题回流到 progress 或 Discuss

默认优先显式触发，不主动自动进入。

## Core model

`$works` 使用最多三层需求结构：

```text
topic（可选：页面 / 模块 / 业务域）
└── 原始需求
    └── 需求细化 / 上下文 / 实现思路 / 待确认 / 当前结论
```

默认两层：`原始需求 → 需求细化`。

只有当需求包覆盖多个页面、模块、业务域或版本内功能区时，才拆出 topic。

## Mode routing

调用 `$works` 时，先判断当前最适合进入哪一种模式。

### Discuss

如果用户还在描述需求、补材料、补限制、提供产品文档 / 接口文档 / Figma / 项目资料，或问题仍偏发散，进入 `Discuss`。

如果当前仍存在会影响实施范围、核心方案、主要约束或验收标准的关键待确认，默认继续停留在 `Discuss`。

如果用户在需求讨论中聊实现方案，但还没有开始实施，也仍属于 `Discuss`，并记录为 `实现思路 / 方案预对齐`。

### Implement

如果用户明确要开始实现、落地、开发、修改代码，且需求对象和关键上下文足以拆出实施子项，进入 `Implement`。

`Implement` 必须附着在某个 discussion 或 topic 下，并创建 / 更新 `implement/progress.md`。

如果进入 Implement 后发现关键需求或上下文仍不足，应停在 `待收口上下文` / `已阻塞`，必要时回到 `Discuss`。

### Acceptance

如果用户要求验收、逐项检查、让另一个 agent 检查，或 progress 已完成但需要正式确认，进入 `Acceptance`。

`Acceptance` 对照 `implement/progress.md` 逐项检查，并维护 `implement/acceptance.md`。

## Execution loop

进入 `$works` 后，默认按这个最小闭环执行：

1. 判断当前模式：Discuss / Implement / Acceptance
2. 在当前 workspace 根目录下定位或创建 `docs-works/` 结构
3. 只读取本轮模式直接相关的文档；模式切换时只补读切换所需来源文档
4. 先按当前模式更新文档中的关键字段，再形成回复结论
5. 回复开头先用一句话说明本轮已落文档内容
6. 然后只给当前阶段 / 状态、当前结论或阻塞、下一步建议

## Reply contract

使用 `$works` 回复时，默认遵循：

- 先以文档中的最新结果为准，再组织回复
- 不要在 `Discuss` 中越级写成已经开始 Build
- 不要在 `Implement` 需求或 checklist 未稳定时写成可直接完成
- progress 全部勾选不等于 Acceptance 通过
- 如果当前仍有关键阻塞项，下一步建议应优先解除阻塞、补确认、补资料或缩小范围
- 如果下一步已经收敛到可拍板问题，默认同轮给出推荐方案和必要备选
- 如果建议进入 Implement 或 Acceptance，应确保对应前置条件已在文档中成立

## References

按任务读取对应文件：

- `references/model.md`：核心领域模型和目录结构
- `references/discuss-mode.md`：需求讨论、需求细化、上下文和实现思路管理
- `references/implement-mode.md`：实施进度、progress、handoff 和 implement context
- `references/acceptance-mode.md`：逐项验收、验收记录和问题回流
