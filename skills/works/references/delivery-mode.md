# Delivery Mode

## Goal

把某一轮代码落地控制在明确边界内，持续推进，并在结束时具备可验收状态。

## Default trigger

默认由用户主动触发，尽量不自动触发，例如：
- 对某个 topic / 子 topic 进行代码落地
- 开始做这一块
- 进入交付 / 实现

## Delivery directory

代码落地不直接散落在 discussion 根目录下，而是进入独立的 `deliveries/` 目录。

每一轮交付默认对应：
- `deliveries/<delivery-name>/brief.md`
- `deliveries/<delivery-name>/progress.md`（可选）
- `deliveries/<delivery-name>/acceptance.md`（可选）

这样可以把 discussion 和交付执行分开。

## Memory check

进入 Delivery 时，默认先做一次相关 memory 检索，再开始 Lock / Build。

检索范围只限与当前功能相关的 memory 条目，优先看：
- `docs-works/memory/decisions/`
- `docs-works/memory/constraints/`
- `docs-works/memory/patterns/`
- `docs-works/memory/facts/`

不要全量扫 memory，只提取和当前交付直接相关的内容。

回复时简短说明：
- 已查到哪些相关 memory
- 本轮会遵守哪些约束 / 复用哪些模式

如果没查到相关 memory，就直接进入本轮 Delivery，不必强行补充。

## Round workflow

每轮 Delivery 默认按下面节奏推进：

### 0. Memory Check
先查与当前交付直接相关的 memory。

### 1. Lock
先锁定本轮交付范围。

优先创建或更新：
- `deliveries/<delivery-name>/brief.md`

这一步至少明确：
- 本轮目标
- In Scope
- Out of Scope
- 实现约束
- 验收标准

没有锁住范围时，不进入大规模实现。

### 2. Build
开始代码实现。

这一阶段的要求：
- 只做本轮 In Scope 内的内容
- 发现新问题时，先判断是否纳入本轮
- 不顺手扩做 Out of Scope 的内容
- 需要时回写进度状态

### 3. Check
实现完成后先做自检。

至少检查：
- 是否满足本轮目标
- 是否仍在范围内
- 是否引入明显回归
- 是否达到约定的验收标准

### 4. Accept
当用户要求，或本轮风险较高时，再进入独立验收。

独立验收可以由单独 agent 承担。

## Independent acceptance agent

### Trigger
独立验收 agent 默认在以下情况触发：
- 用户明确要求单独验收
- 本轮改动范围较大
- 本轮风险较高
- 需要把“实现”和“验收”分开

如果用户没有要求，且风险不高，可以只做自检。

### Responsibility
独立验收 agent 负责：
- 按 `deliveries/<delivery-name>/brief.md` 验收本轮范围
- 检查是否有实现漂移
- 检查是否满足验收标准
- 标记通过项、问题项、遗留项

独立验收 agent 不负责：
- 擅自扩大验收范围
- 顺手继续实现新需求
- 把新的讨论问题直接混入本轮交付

### Output
独立验收输出应尽量简洁，至少包含：
- 验收结论
- 发现的问题
- 是否通过
- 是否需要回到 Build 或 Discuss

## Output rhythm

每轮 Delivery 回复默认包含：
1. 本轮已落文档内容
2. 当前处于 Lock / Build / Check / Accept 哪一阶段
3. 当前进展或结论
4. 下一步建议

保持简洁，不展开长解释。

## Anti-drift rule

Delivery 的核心不是“持续加做”，而是“持续贴着本轮范围推进”。

出现新需求、新问题或新想法时，默认先做分类：
- 纳入本轮
- 记录但暂不处理
- 回退到 Discuss 再收敛

## Scope change rule

如果本轮 `In Scope` / `Out of Scope` / 验收标准发生实质变化，先更新 `deliveries/<delivery-name>/brief.md`，再继续 Build。

说明：
- 小的实现细节调整，不必回写 brief
- 只要影响本轮范围边界或完成标准，就必须先回锁范围
- 如果是否纳入本轮还不明确，先暂停扩做，必要时回到 Discuss 收敛

## Reply example

示例：
1. 已把本轮范围锁到 `deliveries/<delivery-name>/brief.md`
2. 当前处于 Build 阶段，先完成 In Scope 的最小闭环
3. 新发现 1 个相关问题，但先不纳入本轮
4. 下一步建议：先完成主路径，然后做一次自检

## End condition

当满足以下条件时，本轮 Delivery 可以结束：
- In Scope 内容已完成
- 已经过自检
- 需要独立验收的，已完成验收或明确遗留项


## Checkbox rule

checkbox 主要用于执行和验收，不默认用于讨论和范围锁定。

推荐使用 checkbox 的文档：
- `deliveries/<delivery-name>/progress.md`
- `deliveries/<delivery-name>/acceptance.md`

不推荐默认使用 checkbox 的文档：
- `deliveries/<delivery-name>/brief.md`
- `discussion/index.md`
- `topics/*.md`
