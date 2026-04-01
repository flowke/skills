# Memory Mode

## Goal

把 discussion / delivery 中已经稳定、可复用的内容，沉淀成长期记忆。

## Default trigger

默认由用户主动触发，尽量不自动触发，例如：
- 进入记忆
- 沉淀一下
- 把这轮值得记住的收一下

没有这个触发时，不主动进入 Memory。

## Memory filter

进入 `memory/` 的内容，默认必须同时满足：
1. 稳定
2. 可复用
3. 已验证或高置信
4. 脱离当前 discussion 仍有价值

## Suitable content

### decisions/
- 最终方案取舍
- 稳定命名约定
- 已定边界规则

### constraints/
- 技术限制
- 业务约束
- 不可突破规则

### patterns/
- 已验证做法
- 常见坑与对应处理方式
- 可复用工作模式

### facts/
- 已确认现状
- 已验证系统事实
- 稳定结构认知

## Unsuitable content

不要写入：
- 临时 TODO
- 一次性讨论过程
- 候选方案
- 未确认猜测
- 只属于某一轮 delivery 的细节
- 还在波动的结论

## Memory dedup and update

进入 Memory 前，先在对应类型目录中查找是否已有相近条目。

默认规则：
- 如果只是补充依据、适用范围、注意事项，或把已有结论表达得更清楚，优先更新原条目
- 只有当这是新的、稳定的、与已有条目不同的结论时，才新建条目
- 如果发现新信息与旧条目存在冲突，先不要写入 memory
- 这类冲突应先回到 discussion / delivery 中确认，确认后再更新已有条目或新增条目

## Reply example

示例：
- 已把这轮候选记忆筛了一遍，先不新建条目
- 其中 1 条更适合补充到已有 constraint，而不是单独新建
- 另 1 条仍有冲突，先留在 discussion，不进入 memory
- 下一步建议：先更新已有条目，再确认冲突项

## Core rule

不是“聊过就记”，而是“稳定且可复用才记”。
