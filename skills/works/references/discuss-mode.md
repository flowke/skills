# Discuss Mode

## Goal

把讨论中的需求、材料和问题整理成一个持续演化的讨论结构，并在必要时拆出 topic 子页。

## Core rule

先维护总页，必要时再长出 topic。

## Default trigger

默认由用户主动触发，或在当前 discussion 语境内顺势延续。

## Minimal structure

默认只使用下面这套最小结构：

```text
docs-works/
└── discussions/
    └── <discussion-name>/
        ├── index.md
        └── topics/
            └── <topic-name>.md
```

说明：
- `index.md`：总页，负责承接全局背景、当前理解、待确认问题和下一步
- `topics/*.md`：子页，只在某个部分已经足够独立时才创建

默认不额外创建 `shared.md`、`materials.md` 等文件。

## Naming

- discussion 目录：`docs-works/discussions/<discussion-name>/`
- topic 子页：`docs-works/discussions/<discussion-name>/topics/<topic-name>.md`
- 名称使用短、稳定、可读的 kebab-case

## How to work

默认按下面方式推进：
1. 先更新当前 discussion 的 `index.md`
2. 不按聊天时间顺序堆积内容，而是按讨论对象组织
3. 当对象边界还不清楚时，先按较粗粒度整理
4. 当某一部分已经能独立承接“目标 + 问题 + 后续推进”时，再创建 topic 页
5. 保留跨主题问题，不要把它们硬塞进某个 topic

## What goes in index.md

`index.md` 默认至少包含：
- 讨论目标
- 当前输入
- 当前理解
- 当前板块
- 待确认问题
- 下一步建议

## Topic creation threshold

默认先只更新 `index.md`，不要急着创建 `topics/*.md`。

只有当某一部分已经能独立承接下面三件事时，才创建 topic 页：
- 独立目标
- 独立问题 / 结论 / 材料
- 后续独立推进

如果一个部分还不能独立承接“目标 + 问题 + 后续推进”，就先留在 `index.md`。

## Promote to a new discussion

只有当用户主动明确要求“拆成新的”时，才把某个 topic 拆成新的 discussion。

拆出去后：
- 原 discussion 删除与该 topic 相关的内容
- 默认不保留摘要、入口或关系说明
- 新 discussion 继续使用同样的最小结构

## Documentation rhythm

- 边讨论边落文档
- 每轮默认优先更新 `index.md`
- 每轮回复开头先简短说明本轮哪些内容已经落入文档
- 只说明已落文档的内容，不展开过程

## Reply shape

每轮 Discuss 回复默认包含：
1. 本轮已落文档内容
2. 当前理解或阶段性结论
3. 待确认问题
4. 下一步建议

## Reply example

示例：
- 已把本轮新增需求和待确认问题落到 discussion 的 `index.md`
- 当前先聚焦范围和边界，不急着讨论实现细节
- 现在还差 1-2 个关键确认点
- 下一步建议：
  - 选项 1：先确认边界（推荐）
  - 选项 2：先补现状材料

## Minimal templates

### `index.md`

```md
# <discussion-title>

## 1. 讨论目标
- 

## 2. 当前输入
- 

## 3. 当前理解
- 

## 4. 当前板块
### 板块 A：
- 当前结论：
- 待确认：
- 下一步：

## 5. 待确认问题
- 

## 6. 下一步建议
- 选项 1：
- 选项 2：
```

### `topics/<topic-name>.md`

```md
# <topic-title>

## 1. topic 目标
- 

## 2. 当前状态
- 讨论中 / 可进入 Delivery / 已完成

## 3. 当前输入
- 

## 4. 当前结论
- 

## 5. 待确认问题
- 

## 6. 下一步建议
- 选项 1：
- 选项 2：
```

## End condition

当满足以下任一条件时，可以结束当前 Discuss：
- 已经形成较清晰的讨论结构
- 已经可以进入后续交付规划
- 当前主要缺少新材料或用户确认
