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

## Naming

- discussion 目录：`docs-works/discussions/<discussion-name>/`
- topic 子页：`docs-works/discussions/<discussion-name>/topics/<topic-name>.md`
- 名称使用短、稳定、可读的 kebab-case

## Default discussion loop

采用**中强主持**，但保持自然对话感。

默认按下面顺序循环推进：
1. **先定焦**：判断当前最该聊的是哪个问题或哪个层次。
2. **再推进 1-3 个关键问题**：默认优先推进 1 个问题；当多个问题高度相关、一起推进更高效时，可在同一轮推进 2-3 个问题。
3. **做阶段总结**：在自然节点收一下当前理解、待确认问题和未决点。
4. **更新讨论文档**：把稳定内容写入当前 discussion / topic，把暂时未定的内容放入待确认问题。
5. **给出下一步聚焦**：指出下一轮最值得继续推进的问题，并附 1-3 条具体建议。

## How to work

默认按下面方式落结构：
1. 先用 `index.md` 承接当前 discussion
2. 新输入先落到总页，不急着拆 topic
3. 当某一部分已经能独立承接“目标 + 问题 + 后续推进”时，再创建 topic 页
4. topic 创建后，总页保留总览，topic 承接细节
5. 只有用户明确要求“拆成新的”时，才把 topic 升级成新的 discussion

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
