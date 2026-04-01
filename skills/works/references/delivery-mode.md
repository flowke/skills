# Delivery Mode

## Goal

把某一轮实现控制在明确边界内，持续推进，并在结束时具备可验收状态。

## Default trigger

默认由用户主动触发，例如：
- 开始做这一块
- 对某个 topic 进行代码落地
- 进入交付 / 实现

## Minimal structure

```text
docs-works/
└── discussions/
    └── <discussion-name>/
        └── deliveries/
            └── <delivery-name>/
                ├── brief.md
                ├── progress.md      # 可选
                └── acceptance.md    # 可选
```

说明：
- `brief.md`：必需，用来锁定本轮范围
- `progress.md`：本轮跨度较大或持续多轮时再建
- `acceptance.md`：需要正式验收记录时再建

## Memory check

进入 Delivery 时，默认先做一次相关 memory 检索，再开始 Lock / Build。

只提取和当前交付直接相关的内容；如果没查到，就直接进入本轮 Delivery。

## Round workflow

### 0. Memory Check
先查与当前交付直接相关的 memory。

### 1. Lock
先锁定本轮交付范围，优先创建或更新 `deliveries/<delivery-name>/brief.md`。

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

如果本轮 `In Scope` / `Out of Scope` / 验收标准发生实质变化，先更新 `deliveries/<delivery-name>/brief.md`，再继续 Build。

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

每轮 Delivery 回复默认包含：
1. 本轮已落文档内容
2. 当前处于 Lock / Build / Check / Accept 哪一阶段
3. 当前进展或结论
4. 下一步建议

## Reply example

示例：
1. 已把本轮范围锁到 `deliveries/<delivery-name>/brief.md`
2. 当前处于 Build 阶段，先完成 In Scope 的最小闭环
3. 新发现 1 个相关问题，但先不纳入本轮
4. 下一步建议：先完成主路径，然后做一次自检

## Minimal templates

### `brief.md`

```md
# <delivery-title>

## 1. 本轮目标
- 

## 2. 对应 discussion / topic
- 

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
# <delivery-title>

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
# <delivery-title>

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

当满足以下条件时，本轮 Delivery 可以结束：
- In Scope 内容已完成
- 已经过自检
- 需要独立验收的，已完成验收或明确遗留项
