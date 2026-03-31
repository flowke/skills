# Document Organization

## 推荐结构

```text
docs-works/
└── discussions/
    ├── <discussion-a>/
    │   ├── index.md
    │   ├── topics/
    │   │   ├── topic-a.md
    │   │   └── ...
    │   ├── shared.md      # 可选
    │   └── materials.md   # 可选
    └── <discussion-b>/
        └── ...
```

## 1. discussions/

所有 discussion 统一放在 `docs-works/discussions/` 下。

这样后续即使 `docs-works/` 里增加别的分类，也不会和 discussion 混在一起。

## 2. 总页 `index.md`

总入口，默认始终存在。

负责：
- 当前讨论主题
- 当前目标
- 当前理解
- 主题导航
- 跨主题问题摘要
- 待确认问题摘要
- 下一步建议

## 3. 主题子页 `topics/*.md`

按主题或对象展开详细讨论。

每个主题子页负责：
- 主题目标
- 当前结论
- 待确认问题
- 相关材料
- 下一步

## 4. `shared.md`（可选）

只在跨主题内容较多时创建。

负责：
- 主题依赖
- 共用约束
- 全局规则
- 全局待确认问题

如果跨主题内容不多，也可以先留在总页。

## 5. `materials.md`（可选）

只在材料较多时创建。

负责：
- 链接清单
- 截图说明索引
- 参考资料索引
- 外部文档入口

如果材料不多，也可以先写在总页或主题子页里。

## 6. 默认生长顺序

默认按下面顺序生长：
1. 先有 `index.md`
2. 总页里先长出主题摘要子块
3. 某主题内容明显变大，再创建对应主题子页
4. 跨主题内容变多，再补 `shared.md`
5. 材料较多，再补 `materials.md`

## 7. 命名建议

### discussion 目录
- `docs-works/discussions/<discussion-name>/`
- 使用短、稳定、可读的 kebab-case
- 优先体现这次讨论的核心对象或核心问题
- 不要带时间戳当主体
- 不要用过泛的名字，如 `misc`、`temp`、`new-discussion`

推荐：
- `teacher-dashboard-redesign`
- `comment-permission-model`
- `course-detail-experience`

不推荐：
- `discussion-1`
- `temp`
- `misc-notes`

### 总页
- `index.md`

### 主题子页
- `topics/<topic-name>.md`
- 名称使用稳定、短、可复用的 kebab-case

### 可选页
- `shared.md`
- `materials.md`

### delivery 目录
- `deliveries/<delivery-name>/`
- 使用短、稳定、可读的 kebab-case
- 优先体现“这轮交付的对象 + 动作”
- 不要只写技术动作，不要丢掉对象语义
- 不要用过泛名字，如 `fixes`、`update`、`iteration-1`

推荐：
- `comment-permission-phase-1`
- `teacher-dashboard-layout`
- `course-detail-loading-optimization`

不推荐：
- `fix`
- `update`
- `delivery-1`

## 8. 最小可用版本

如果只做最小结构，默认只需要：

```text
docs-works/
└── discussions/
    └── <discussion-name>/
        ├── index.md
        └── topics/
            └── <topic-name>.md
```

## 9. 使用原则

- 先有总页，再长子页
- 不要一开始就建很多页
- 子页只承接明显长大的主题
- 总页始终保留导航和总览职责

## 10. 升级为新的 <discussion-root>

当某个主题非常复杂时，可以把它拆成一个新的 `<discussion-root>`。

默认规则：
- 只有当用户主动明确说“拆成新的”时才执行
- 这不是在原 root 下面多建一页，而是新建一棵讨论树
- 原 root 删除与该主题相关的所有内容
- 新 root 承接该主题后续的详细讨论
- 默认不在原 root 保留摘要、入口或关系说明
- 新 root 的 `index.md` 也使用统一 discussion 模板

推荐结构：

```text
docs-works/
└── discussions/
    ├── <old-discussion-root>/
    │   ├── index.md
    │   ├── topics/
    │   └── ...
    └── <new-discussion-root>/
        ├── index.md
        ├── topics/
        ├── shared.md
        └── materials.md
```


## 11. Delivery brief

当用户主动要求对某个 topic / 子 topic 进行代码落地时，先创建或更新一份 `delivery-brief.md` 来锁定本轮范围。

模板：
- `references/delivery-brief-template.md`

## 12. Delivery 文档结构

当某个 discussion 进入 Delivery 后，代码落地默认使用独立目录组织，类似 work-items：

```text
<discussion-root>/
├── index.md
├── topics/
├── shared.md
├── materials.md
└── deliveries/
    ├── <delivery-name>/
    │   ├── brief.md
    │   ├── progress.md      # 可选
    │   └── acceptance.md    # 可选
    └── ...
```

### 说明
- `deliveries/<delivery-name>/brief.md`：必需，用来锁定本轮范围
- `deliveries/<delivery-name>/progress.md`：当本轮实现跨度较大、持续时间较长时再建
- `deliveries/<delivery-name>/acceptance.md`：需要正式验收记录时再建

默认原则：
- 每一轮代码落地对应一个独立的 delivery 目录
- 先有 `brief.md`
- 需要持续跟踪时，再补 `progress.md`
- 需要正式验收记录时，再补 `acceptance.md`
- `discussion/index.md` 负责总览，具体交付状态下沉到 `deliveries/`

## 13. Delivery progress

当某一轮 delivery 跨度较大、会持续多轮推进时，再创建：
- `deliveries/<delivery-name>/progress.md`

模板：
- `references/delivery-progress-template.md`

## 14. Delivery acceptance

当某一轮 delivery 需要正式验收记录时，再创建：
- `deliveries/<delivery-name>/acceptance.md`

模板：
- `references/delivery-acceptance-template.md`

## 15. Memory 目录结构

长期记忆不放在 `discussions/` 里，而是单独放在 `docs-works/memory/` 下。

推荐结构：

```text
docs-works/
├── discussions/
│   └── ...
└── memory/
    ├── decisions/
    ├── constraints/
    ├── patterns/
    └── facts/
```

说明：
- `decisions/`：稳定决策
- `constraints/`：可复用约束
- `patterns/`：可复用做法与经验
- `facts/`：已确认事实

原则：
- discussion 产出记忆候选
- memory 承接最终沉淀
- 不把讨论过程直接写入 memory

## 16. Memory 规则

进入 memory 前，先按下面规则筛选：
- `references/memory-mode.md`

## 17. Memory 条目模板

当某条内容通过 memory 筛选后，默认使用：
- `references/memory-entry-template.md`

适用位置：
- `docs-works/memory/decisions/*.md`
- `docs-works/memory/constraints/*.md`
- `docs-works/memory/patterns/*.md`
- `docs-works/memory/facts/*.md`
