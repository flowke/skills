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

