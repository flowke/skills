# Migration Rules

## 1. 从 `index.md` 拆到 `topics/<topic-name>.md`

适用场景：
- 某个 topic 已经不适合只留在总页摘要里
- 需要单独承接该 topic 的持续讨论

### 迁移内容
从 `index.md` 迁到 `topics/<topic-name>.md` 时，优先迁：
- 该 topic 的目标
- 该 topic 的当前输入
- 该 topic 的当前结论
- 该 topic 的待确认问题
- 该 topic 的相关材料
- 该 topic 的下一步建议

### 原页保留
迁出后，`index.md` 只保留：
- topic 名称
- 一句话状态摘要
- 必要的主题导航

不要在 `index.md` 里继续保留大段 topic 细节。

---

## 2. 从 `topics/<topic-name>.md` 拆成新的 `<discussion-root>`

适用场景：
- 用户主动明确要求“拆成新的”

### 迁移内容
拆成新的 `<discussion-root>` 时，整体迁走：
- topic 目标
- 当前状态
- 当前输入
- 当前结论
- 待确认问题
- 相关材料
- Delivery 准备度
- 下一步建议
- 与该 topic 强绑定的子 topic 内容

### 原页处理
拆出后，原 discussion 中：
- 删除与该 topic 相关的全部内容
- 不保留摘要
- 不保留入口
- 不保留关系说明

### 新 root 处理
新 `<discussion-root>` 使用统一 discussion 模板，必要时再继续长出自己的：
- `topics/`
- `shared.md`
- `materials.md`
- `deliveries/`

---

## 3. 迁移原则

- 迁移是重组，不是复制一份后两边同时保留
- 总页只保留总览，不承接大段细节
- 只有用户主动说“拆成新的”时，才拆成新的 `<discussion-root>`
- 迁移后结构要更清楚，而不是增加重复内容
