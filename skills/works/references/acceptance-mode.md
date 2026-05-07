# Acceptance Mode

## Goal

对 Implement 的结果进行逐项验收，确认 progress 中的原始需求和实施子项是否真正满足要求，并把问题回流到 progress 或 Discuss。

Acceptance 不是实施进度记录；它是独立检查记录。

## Core rule

验收必须对照 `implement/progress.md` 逐项执行：

```text
progress.md 中的原始需求
└── 实施子项 checklist
    └── acceptance.md 中逐项验收
```

progress 全部 `[x]` 不等于验收通过。

## Default trigger

进入 Acceptance 的典型信号：
- 用户明确要求验收、检查、逐项检查、让另一个 agent 检查
- progress 主要子项已经完成，需要独立确认
- 本轮风险较高，需要正式验收记录
- 需要把实现和验收分开维护

如果用户只要求自检，且风险不高，可以在 Implement 中做 Check，不一定创建 acceptance。

## File location

Acceptance 总是附着在对应 implement 下：

```text
implement/
├── progress.md
├── context.md
└── acceptance.md
```

## Acceptance state model

验收结论使用：

- `未开始`：尚未开始验收
- `验收中`：正在逐项检查
- `通过`：所有必验项通过，无阻塞问题
- `有条件通过`：核心项通过，但存在可接受遗留或后续项
- `不通过`：存在阻止收口的问题
- `已回流`：验收问题已回流到 progress 或 Discuss，等待下一轮实施或确认

## What to read before acceptance

执行 Acceptance 前，至少读取：
- `implement/progress.md`
- `implement/context.md`（如果存在）
- 对应 discussion / topic 的 `index.md`
- 相关 context（如果验收依赖接口、设计稿、项目资料）

验收以 progress 为主入口，但不能忽略当前实施口径和上下文约束。

## Acceptance item rule

每个验收项必须能追溯到：
- 原始需求编号 `R#`
- progress 中的实施子项
- 当前实施口径

每个实施子项的验收记录至少包含：
- progress 状态
- 验收状态
- 验收说明
- 证据 / 命令 / 截图 / 文件（如适用）

验收状态：
- `通过`
- `不通过`
- `未验证`
- `不适用`

## Evidence rule

验收证据可以包括：
- 测试命令和结果
- 截图
- 访问链接
- 文件路径
- 代码位置
- 手工检查说明
- 设计稿对照结论
- 接口响应示例

如果无法提供证据，应在验收说明里说明原因。

## Problem feedback rule

验收发现问题时：

1. **实现缺陷**
   - 回流到 `progress.md` 对应原始需求下
   - 将相关子项改回 `[~]` 或新增修复子项

2. **需求理解偏差**
   - 回到 Discuss，更新讨论细化、当前结论或待确认

3. **新增需求**
   - 不直接塞进当前实施完成项
   - 作为新原始需求、后续版本项或新的 Discuss 输入处理

4. **可接受遗留**
   - 记录在 acceptance 的遗留项中
   - 必要时同步到 progress 的下一步或 context

## Round workflow

### 1. Prepare

读取 progress 和相关上下文，确定验收范围。

### 2. Check items

按原始需求和子项逐项检查。

### 3. Record evidence

为每个已检查项记录验收说明和证据。

### 4. Summarize result

给出总体结论：通过 / 不通过 / 有条件通过。

### 5. Feedback

把问题项回流到 progress 或 Discuss。

## Round update contract

每轮 Acceptance 默认按下面顺序更新：

1. 更新 `验收对象` 和 `验收范围`
2. 按 progress 逐项更新 `逐项验收`
3. 汇总 `问题项`
4. 汇总 `遗留项 / 后续建议`
5. 更新 `验收结论`
6. 如有问题回流，同步更新 progress 或说明需要回到 Discuss

## Consistency rule

必须保持同步：
- acceptance 的逐项验收范围和 progress checklist
- acceptance 的问题项和 progress 中的阻塞 / 待确认 / 子项状态
- acceptance 的需求理解问题和 Discuss 的待确认 / 讨论细化

禁止出现：
- acceptance 写通过，但仍有必验项未验证且未说明
- acceptance 写通过，但问题项中存在阻塞问题
- progress 子项发生变化后，acceptance 仍按旧子项验收且没有说明
- 验收发现新增需求，却直接写成当前实现通过

## Minimal template

### `implement/acceptance.md`

```md
# <scope-title> / Acceptance

## 1. 验收对象
- 对应 discussion：
- 对应 topic：
- 对应 progress：`progress.md`
- 验收时间：
- 验收人 / agent：

## 2. 验收范围
- 本次覆盖：
- 本次不覆盖：

## 3. 验收结论
- 结论：未开始 / 验收中 / 通过 / 有条件通过 / 不通过 / 已回流
- 总结：

## 4. 逐项验收

### R1. <原始需求标题>
- 原始需求：
- 当前实施口径：

#### 子项 1：<progress 子项文本>
- progress 状态：[ ] / [~] / [x]
- 验收状态：通过 / 不通过 / 未验证 / 不适用
- 验收说明：
- 证据 / 命令 / 截图 / 文件：

#### 子项 2：<progress 子项文本>
- progress 状态：
- 验收状态：
- 验收说明：
- 证据：

## 5. 问题项
- 

## 6. 遗留项 / 后续建议
- 

## 7. 回流记录
- 已回流到 progress：
- 需要回到 Discuss：
```
