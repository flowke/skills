# Implement Mode

## Goal

把某项实现工作组织成可持续推进的交付单元：先接住需求来源，再按轮次锁定范围、推进实现、自检，并在需要时验收。

## Default trigger

默认由用户主动触发，例如：
- 开始做这一块
- 对某个 topic 进行代码落地
- 已经有 PRD / issue / 设计稿，直接进入实现
- 进入交付 / 实现

## Minimal structure

```text
docs-works/
└── implements/
    └── <implement-name>/
        ├── brief.md
        ├── progress.md      # 可选
        └── acceptance.md    # 可选
```

说明：
- `Implement` 默认可独立创建，不要求先存在 `Discuss`
- 如果它来自某个 discussion / topic，只在文档里记录关联来源，不强依赖目录层级
- `brief.md`：必需，用来锁定当前阶段范围，并记录需求来源
- `progress.md`：本轮跨度较大或持续多轮时再建
- `acceptance.md`：需要正式验收记录时再建

## Context check

进入 Implement 时，默认先查当前最直接的需求来源，再开始 Lock / Build。

需求来源可以是：
- 当前 discussion / topic
- 外部需求文档 / PRD
- issue / ticket
- 设计稿 / 代码评审意见 / 现有缺陷描述

如果没有成型上下文，就直接根据用户当前指令建立一个 Implement。

## Round workflow

### 0. Context Check
先查本轮实现最直接相关的需求来源，并整理成可执行上下文。

### 1. Lock
先锁定当前推进阶段的范围，优先创建或更新 `implements/<implement-name>/brief.md`。

至少明确：
- 本轮目标
- In Scope
- Out of Scope
- 实现约束
- 验收标准

### 2. Build
开始实现，只做本轮 In Scope 内的内容。

### 3. Check
实现完成后先做自检，确认：
- 是否满足本轮目标
- 是否仍在范围内
- 是否引入明显回归
- 是否达到约定的验收标准

### 4. Accept
当用户要求，或本轮风险较高时，再进入独立验收。

## Scope change rule

如果当前推进阶段的 `In Scope` / `Out of Scope` / 验收标准发生实质变化，先更新 `implements/<implement-name>/brief.md`，再继续 Build。

说明：
- 小的实现细节调整，不必回写 brief
- 只要影响本轮范围边界或完成标准，就必须先回锁范围
- 如果是否纳入本轮还不明确，先暂停扩做，必要时回到 Discuss 收敛

## Acceptance rule

独立验收默认在以下情况触发：
- 用户明确要求单独验收
- 本轮改动范围较大
- 本轮风险较高
- 需要把“实现”和“验收”分开

如果用户没有要求，且风险不高，可以只做自检。

## Reply shape

每轮 Implement 回复默认包含：
1. 本轮已落文档内容
2. 当前处于 Context Check / Lock / Build / Check / Accept 哪一阶段
3. 当前进展或结论
4. 下一步建议

## Reply example

示例：
1. 已把当前阶段范围锁到 `implements/<implement-name>/brief.md`
2. 当前处于 Build 阶段，先完成 In Scope 的最小闭环
3. 新发现 1 个相关问题，但先不纳入当前阶段
4. 下一步建议：先完成主路径，然后做一次自检

## Minimal templates

### `brief.md`

```md
# <implement-title>

## 1. 本轮目标
- 

## 2. 需求来源
- 可填写 discussion / topic、外部 PRD、issue、设计稿、口头需求等


## 3. In Scope
- 

## 4. Out of Scope
- 

## 5. 实现约束
- 

## 6. 验收标准
- 
```

### `progress.md`

```md
# <implement-title>

## 1. 当前状态
- 未开始 / 进行中 / 待验收 / 已完成

## 2. 本轮摘要
- 

## 3. 已完成
- 

## 4. 进行中
- 

## 5. 阻塞项
- 

## 6. 下一步
- 
```

### `acceptance.md`

```md
# <implement-title>

## 1. 验收结论
- 通过 / 有条件通过 / 不通过

## 2. 验收范围
- 

## 3. 通过项
- 

## 4. 问题项
- 

## 5. 遗留项
- 

## 6. 建议动作
- 
```

## End condition

当满足以下条件时，当前阶段 Implement 可以结束：
- 当前阶段 In Scope 内容已完成
- 已经过自检
- 需要独立验收的，已完成验收或明确遗留项

说明：
- 一个 Implement 可以包含多轮推进
- 是否结束 Implement，取决于该实现目标是否已经整体收口，而不是只看单次编码动作是否结束
