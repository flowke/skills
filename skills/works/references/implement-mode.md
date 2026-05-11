# Implement Mode

## Goal

把某个 discussion 或 topic 的需求实施组织成可持续推进、可中断恢复、可被独立验收的交付空间。

Implement 的核心不是写交付说明，而是维护 `progress.md`：
- 按原始需求组织实施子项
- 用 checklist 跟踪进度
- 承接 Discuss 阶段的讨论细化、上下文和实现思路
- 作为跨机器 / 跨 agent 继续工作的 handoff 文档

## Core rule

Implement 永远附着在被实施对象下面：

- discussion 级实施：`docs-works/discussions/<discussion-name>/implement/`
- topic 级实施：`docs-works/discussions/<discussion-name>/topics/<topic-name>/implement/`

新规则不再默认使用平行目录 `docs-works/implements/<implement-name>/`。

## Default trigger

进入 Implement 的典型信号：
- 用户明确说开始实现、落地、开发、改代码、推进实施
- Discuss 已达到 `可进入 Implement`
- 某个 topic 或整个 discussion 的需求已足够明确，需要开始维护实施进度
- 用户要求从某个产品文档 / topic / discussion 直接开始做
- 用户要求继续之前的实施进度

如果仍存在会影响实施范围、关键方案、主要约束或验收方式的未决点，优先回到 Discuss 或先在 Implement 中标为 `已阻塞`，不要直接 Build。

## Minimal structure

```text
implement/
├── progress.md       # 必需：实施主控 + handoff
├── context.md        # 按需：实施上下文 / 技术资料 / 方案讨论
└── acceptance.md     # 验收时必需：逐项检查结果
```

说明：
- `progress.md` 必须创建
- `context.md` 只在有实施相关资料、方案讨论或技术上下文需要管理时创建
- `acceptance.md` 在用户要求验收、使用另一个 agent 检查、风险较高或需要正式验收记录时创建
- `brief.md` 不再是默认必需文件；原 brief 的范围、约束、假设等信息，收敛到 `progress.md` 的当前实施口径和 `context.md`

## Implement state model

Implement 默认使用下面这组状态：

- `待收口上下文`：实施对象已确定，但需求、上下文或实现口径仍不足以拆出可执行子项
- `待拆子项`：需求基本明确，但 progress 还没有形成可执行 checklist
- `进行中`：正在按 progress 子项实施
- `已阻塞`：存在阻止继续实施的关键问题
- `待验证`：progress 子项已基本完成，等待自检或验收
- `待验收`：需要独立 Acceptance 检查
- `已完成`：实施完成且无需进一步验收，或已完成验收问题回收

说明：
- `当前状态` 表达实施空间状态，不等于聊天语气
- progress 全部 `[x]` 后，通常进入 `待验证` 或 `待验收`，不自动等于 `已完成`

## State decision priority

当多个状态同时成立时，按下面优先级判断：

1. 如果关键依赖、需求确认、技术方案或验收标准阻止继续实施，标为 `已阻塞`
2. 如果用户要求验收或需要独立检查，标为 `待验收`
3. 如果全部或主要子项完成但尚未检查，标为 `待验证`
4. 如果正在实施 checklist 子项，标为 `进行中`
5. 如果需求明确但还没有拆出可执行子项，标为 `待拆子项`
6. 如果实施对象已确定但上下文仍不足，标为 `待收口上下文`
7. 否则按当前 progress 判断

## Source handoff rule

从 Discuss 进入 Implement 时，必须承接以下内容：

- 原始需求编号和原始语义
- 讨论细化中的关键边界、规则、默认行为和例外
- 当前结论
- Discuss 阶段的 `实现思路 / 方案预对齐`
- 已消化且影响实现的 context
- 仍可能阻塞实施的待确认项

承接位置：
- 进入 `progress.md`：原始需求、当前实施口径、实施子项、阻塞 / 待确认
- 进入 `implement/context.md`：详细实现方案讨论、技术资料、接口说明、已吸收上下文

## Progress as handoff

`progress.md` 必须足以支持另一台机器或另一个 agent 继续工作。

最低要求：
- 能看出实施对象
- 能看出对应哪些原始需求
- 每个原始需求下面有实施子项 checklist
- 能看出每个子项是否未开始 / 进行中 / 已完成
- 能看出当前实施口径
- 能看出阻塞 / 待确认和下一步
- 不依赖额外 handoff 文档才能继续

## Checklist rule

实施子项必须挂在某个原始需求下面。

状态约定：
- `[ ]`：未开始
- `[~]`：进行中 / 部分完成 / 有待处理
- `[x]`：已完成

子项要求：
- 可执行
- 可判断是否完成
- 尽量不要混多个完成标准
- 不要写成泛化目标，例如“优化整体逻辑”
- 不维护脱离原始需求的杂项 todo 池

如果有跨多个原始需求的共用实施项：
- 优先挂到最相关的原始需求下，并说明影响范围
- 或在 progress 中创建 `共用实施项` 小节，但必须说明关联的原始需求编号

## Implement context rule

当实施阶段出现以下内容时，应创建或更新 `implement/context.md`：
- 技术方案讨论
- 接口调用方式
- 代码结构说明
- 实施阶段新增资料
- 从 Discuss 继承的关键上下文
- 已确认或暂不采用的方案取舍

context 条目建议结构：

```md
### IC1. <上下文标题>
- 类型：实现方案 / 接口说明 / 代码结构 / 技术约束 / 资料链接 / 其他
- 来源：Discuss / Implement 新增 / 外部资料
- 关联需求：R1 / R2 / Topic / 全局
- 当前状态：未消化 / 已消化 / 已吸收进 progress / 暂不采用
- 摘要：
- 对实现的影响：
```

`progress.md` 中的 `全局实施上下文摘要` 只保留关键结论和链接，不复制大量资料。

## Build gate rule

只有同时满足以下条件，才建议开始 Build：

- 实施对象明确：discussion 或 topic
- progress 已创建
- 原始需求已进入 progress
- 每个纳入本轮的原始需求都有当前实施口径
- 已拆出可执行子项 checklist
- 不存在会改变实施范围、核心方案或验收标准的关键未决点
- 关键上下文已消化，或未消化部分已标为不阻塞

如果不满足，应先补 progress、补 context、回到 Discuss 或标记阻塞。

## Round workflow

### 1. Context Check

读取实施对象：
- discussion / topic 的 index
- 相关 context
- Discuss 阶段的实现思路 / 方案预对齐
- 已有 implement/progress.md 和 implement/context.md

判断是否足以继续实施。

### 2. Progress Setup / Update

创建或更新 `progress.md`：
- 实施对象
- 当前状态
- 需求实施进度
- 全局实施上下文摘要
- 阻塞 / 待确认
- 下一步

### 3. Build

只实施 progress 中当前纳入的子项。

实施过程中：
- 完成子项后更新 `[x]`
- 进行中或部分完成用 `[~]` 并补一句说明
- 新发现的工作如果属于已有原始需求，补到该需求子项下
- 新发现的需求如果超出原始需求，回到 Discuss 或标为后续需求，不直接混入

### 4. Check

自检当前实现：
- 是否满足 progress 中的子项
- 是否仍符合当前实施口径
- 是否引入明显回归
- 是否需要进入 Acceptance

### 5. Acceptance handoff

如果用户要求验收，或需要另一个 agent 逐项检查：
- 创建 / 更新 `acceptance.md`
- 将状态置为 `待验收`
- 按 Acceptance Mode 执行

## Round update contract

每轮 Implement 默认按下面顺序更新：

1. 如果新增或变化了实施资料，先更新 `implement/context.md`
2. 如果实施口径变化，更新 progress 对应原始需求的 `当前实施口径`
3. 如果新增 / 完成 / 部分完成 / 阻塞子项，更新 checklist
4. 更新 `阻塞 / 待确认`
5. 更新 `当前状态`
6. 更新 `下一步`
7. 如果进入验收，创建或更新 `acceptance.md`

禁止实现完成后不更新 progress。

## Consistency rule

必须保持同步：
- progress 中的原始需求和 Discuss 中的原始需求编号 / 语义
- progress 中的当前实施口径和 implement context 中已采用方案
- progress checklist 和实际实施状态
- progress 阻塞 / 待确认和下一步
- acceptance 中的验收项和 progress checklist

禁止出现以下不一致：
- progress 全部 `[x]`，但仍有阻塞项未处理且没有说明
- 实施新增了范围外需求，却直接塞进 checklist 且没有回到 Discuss
- context 已标为已吸收，但 progress 没有体现其影响
- 用户要求验收，但没有创建或更新 acceptance
- 当前状态是 `已完成`，但 acceptance 仍有不通过问题项

## Next-step suggestion rule

根据当前状态给下一步：
- `待收口上下文`：补需求 / 补资料 / 回到 Discuss
- `待拆子项`：先把原始需求拆成 checklist
- `进行中`：继续完成当前最小闭环子项，不随意扩范围
- `已阻塞`：解除阻塞、缩小范围或回到 Discuss
- `待验证`：自检或准备 Acceptance
- `待验收`：执行 Acceptance
- `已完成`：总结结果，记录遗留，必要时开启下一轮

## Minimal templates

### Topic 级 `implement/progress.md`

```md
# <topic-title> / Implement Progress

## 1. 实施对象
- 对应 discussion：
- 对应 topic：
- 当前状态：待收口上下文 / 待拆子项 / 进行中 / 已阻塞 / 待验证 / 待验收 / 已完成

## 2. 需求实施进度

### R1. <原始需求标题>
- 原始需求：
- 当前实施口径：
- 子项：
  - [ ] 
  - [~] 
  - [x] 

### R2. <原始需求标题>
- 原始需求：
- 当前实施口径：
- 子项：
  - [ ] 

## 3. 全局实施上下文摘要
- 关键约束：
- 已吸收上下文：
- 详细资料：见 `context.md` / 暂无

## 4. 阻塞 / 待确认
- 

## 5. 下一步
- 
```

### Discussion 级 `implement/progress.md`

```md
# <discussion-title> / Implement Progress

## 1. 实施对象
- 对应 discussion：
- 当前状态：待收口上下文 / 待拆子项 / 进行中 / 已阻塞 / 待验证 / 待验收 / 已完成

## 2. 需求实施进度

### Topic A：<页面 / 模块 / 业务域>

#### R1. <原始需求标题>
- 原始需求：
- 当前实施口径：
- 子项：
  - [ ] 
  - [x] 

#### R2. <原始需求标题>
- 原始需求：
- 当前实施口径：
- 子项：
  - [~] 

### 未分 topic 的需求

#### R3. <原始需求标题>
- 原始需求：
- 当前实施口径：
- 子项：
  - [ ] 

## 3. 全局实施上下文摘要
- 关键约束：
- 已吸收上下文：
- 详细资料：见 `context.md` / 暂无

## 4. 阻塞 / 待确认
- 

## 5. 下一步
- 
```

### `implement/context.md`

```md
# <scope-title> / Implement Context

## 1. 实施上下文列表

### IC1. <上下文标题>
- 类型：实现方案 / 接口说明 / 代码结构 / 技术约束 / 资料链接 / 其他
- 来源：Discuss / Implement 新增 / 外部资料
- 关联需求：R1 / R2 / Topic / 全局
- 当前状态：未消化 / 已消化 / 已吸收进 progress / 暂不采用
- 摘要：
- 对实现的影响：

## 2. 方案取舍
- 当前采用：
- 暂不采用：
- 待确认：
```
