# Works Core Model

## Goal

`$works` 用来把一项工作从需求讨论推进到实施和验收，并让需求来源、细化过程、实施进度、上下文资料和验收结果可以被连续承接。

它不是聊天纪要工具，而是一个面向项目工作的结构化工作系统：

```text
需求来源 / 产品文档 / 设计稿 / 接口文档 / 项目资料
        ↓
Discuss：需求整理、讨论细化、上下文管理、实现思路预对齐
        ↓
Implement：实施进度跟踪、跨机器继续工作、上下文承接
        ↓
Acceptance：逐项验收、问题回流
```

## Core principles

1. **原始需求不可被覆盖**
   - 产品文档、用户输入、issue 或口头需求中的原始诉求必须保留原始语义
   - 后续讨论得出的理解、边界、默认方案和实现口径只能进入讨论细化、当前结论或实施字段，不能反向改写原始需求

2. **需求最多三层**
   - 默认两层：`原始需求 → 讨论细化`
   - 复杂需求包可选三层：`topic → 原始需求 → 讨论细化`
   - 不做无限层级的 topic / subtopic / sub-subtopic

3. **topic 是页面 / 模块 / 业务域，不默认等于原始需求**
   - 一个 topic 可以包含多个原始需求
   - 当需求包覆盖多个页面、模块、业务域或版本内功能区时，才拆 topic
   - 简单需求包不强行拆 topic

4. **上下文资料必须可追踪**
   - 接口文档、Figma、项目资料、外部链接、截图、现有代码说明等都属于 context
   - context 要记录来源、类型、关联需求、消化状态和影响，不只是堆链接

5. **Discuss 阶段允许管理实现思路**
   - 在需求讨论时，可以预先讨论实现方案、技术路径、约束和取舍
   - 这些内容不等于已经开始实施，但进入 Implement 时必须能被承接

6. **Implement 必须支持 handoff**
   - `progress.md` 是实施主控文档，也是默认 handoff 文档
   - 中途暂停、换机器、换 agent 时，应能只看 progress 和必要 context 继续工作

7. **验收和实施分离**
   - `progress.md` 记录实施方进度
   - `acceptance.md` 记录验收方逐项检查结果
   - progress 全部勾选不等于验收通过

## Domain objects

### Discussion

一个 discussion 是一组相关需求的讨论空间，通常来自一个产品文档、一次需求沟通、一个版本需求包或一个较大的工作目标。

职责：
- 承接需求来源
- 判断是否需要 topic
- 管理全局上下文资料
- 记录全局关键待确认
- 决定是否可以进入 Implement

### Topic

topic 是 discussion 下的可选第三层，用于表示页面、模块、业务域、版本内功能区或其他自然分组。

职责：
- 承接该页面 / 模块 / 业务域内的多个原始需求
- 管理 topic 级上下文资料
- 管理该 topic 内的关键待确认和下一步
- 可作为独立实施对象

默认不要把 topic 当成单个原始需求。只有当用户明确要求，或某个原始需求天然就是一个页面 / 模块 / 业务域时，topic 才可能只包含一个原始需求。

### Original Requirement（原始需求 / 原始描述）

原始需求是从产品文档、用户输入、issue、设计稿说明或其他需求来源中直接接收到的原始诉求与原始描述。

规则：
- 判断依据是**来源**，不是内容粗细
- 产品文档里已经写出的详细字段、交互、文案、状态、流程，都仍属于 `原始需求 / 原始描述`
- 保留原始语义，可轻微整理措辞，但不要混入后续讨论推导
- 使用稳定编号，例如 `R1`、`R2`、`R3`
- 后续实施和验收都应能追溯到原始需求编号

### Requirement Refinement（讨论细化）

讨论细化是围绕某个原始需求，在**后续讨论循环**中新增确认、澄清或补充出来的内容。

规则：
- 只有讨论循环中新确认的边界、规则、例子、默认行为、例外场景、优先级、不做什么和依赖条件，才进入 `讨论细化`
- 初始导入产品文档时，`讨论细化` 通常应为 `暂无`
- 不要把产品文档原文中已经存在的详细需求误放进 `讨论细化`
- 已确认并稳定下来的讨论细化，可以进一步影响 `当前结论` 和 Implement 的 `当前实施口径`

### Context（上下文资料）

context 是帮助理解需求或实现需求的外部或补充资料。

常见类型：
- 产品文档
- 接口文档
- Figma / 设计稿
- 项目资料
- 代码结构说明
- 数据结构说明
- 外部链接
- 截图 / 文件
- 用户补充说明

context 可以存在于三个层级：
- `discussion/context.md`：全局需求理解资料
- `topics/<topic-name>/context.md`：topic 级需求理解资料
- `implement/context.md`：实施阶段上下文、方案讨论和技术资料

### Implementation Idea（实现思路 / 方案预对齐）

Discuss 阶段也可以记录与实现相关的思路。

语义：
- 它是讨论阶段的实现预对齐
- 不等于已经进入 Build
- 不一定是最终方案
- 进入 Implement 时，应转写或承接到 `implement/context.md` 或 `progress.md` 的 `当前实施口径`

### Implement

Implement 是对某个 discussion 或 topic 的实施空间。

规则：
- 默认附着在被实施对象下面
- `progress.md` 必需
- `context.md` 按需
- `acceptance.md` 在验收时必需
- 新结构不再默认使用独立平行目录 `docs-works/implements/`

### Progress

`progress.md` 是实施主控文档和 handoff 文档。

它必须按原始需求组织实施子项：

```text
原始需求 R1
└── 实施子项 checklist

原始需求 R2
└── 实施子项 checklist
```

规则：
- 每个实施子项必须挂在某个原始需求下面
- checklist 是进度单一事实来源
- 使用 `[ ] / [~] / [x]` 表示未开始 / 进行中或部分完成 / 已完成
- 不维护脱离原始需求的杂项 todo 池

### Acceptance

Acceptance 是实施后的逐项验收空间。

规则：
- 验收应对照 `progress.md` 的原始需求和实施子项逐项检查
- 可由另一个 agent 执行
- 结论可以是：`通过 / 不通过 / 有条件通过`
- 问题项需要回流到 progress 或下一轮 implement

## Default directory structure

### Simple discussion（默认两层，无 topic）

```text
docs-works/
└── discussions/
    └── <discussion-name>/
        ├── index.md
        ├── context.md              # 可选：全局需求上下文
        └── implement/              # 对整个 discussion 实施时创建
            ├── progress.md         # 必需
            ├── context.md          # 按需
            └── acceptance.md       # 验收时必需
```

### Topic-based discussion（可选三层）

```text
docs-works/
└── discussions/
    └── <discussion-name>/
        ├── index.md
        ├── context.md                      # 可选：全局需求上下文
        ├── implement/                      # 可选：跨 topic 实施
        │   ├── progress.md                 # 必需
        │   ├── context.md                  # 按需
        │   └── acceptance.md               # 验收时必需
        └── topics/
            └── <topic-name>/
                ├── index.md
                ├── context.md              # 可选：topic 级上下文
                └── implement/
                    ├── progress.md         # 必需
                    ├── context.md          # 按需
                    └── acceptance.md       # 验收时必需
```

## Naming

- discussion 目录：`docs-works/discussions/<discussion-name>/`
- topic 目录：`docs-works/discussions/<discussion-name>/topics/<topic-name>/`
- discussion 级 implement：`docs-works/discussions/<discussion-name>/implement/`
- topic 级 implement：`docs-works/discussions/<discussion-name>/topics/<topic-name>/implement/`
- 名称使用短、稳定、可读的 kebab-case

## Mode relation

### Discuss → Implement

当需求已经对齐到足以开始实施时，进入 Implement。

进入时应承接：
- 原始需求编号和原始语义
- 当前结论
- 讨论细化中的关键边界
- Discuss 阶段的实现思路 / 方案预对齐
- 已消化且影响实现的 context
- 仍阻塞实施的待确认项

### Implement → Acceptance

当实施子项已完成、用户要求验收，或需要独立 agent 检查时，进入 Acceptance。

进入时应承接：
- progress 中的原始需求和实施子项
- 当前实施口径
- 已知阻塞 / 遗留 / 风险
- 验收所需 context 和证据

### Acceptance → Implement / Discuss

如果验收发现问题：
- 实现缺陷：回流到 progress，作为未完成或修复子项
- 需求理解偏差：回到 Discuss 更新讨论细化 / 当前结论
- 新增需求：作为新的原始需求或后续版本项处理
