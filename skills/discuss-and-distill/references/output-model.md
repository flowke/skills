# Output Model

`discuss-and-distill` 管理的产出分为四层。

## 1. 主题工作层

位置：`docs-discuss-and-distill/<YYYY-MM-DD-主题>/`

用途：
- 承接该主题的主工作文档
- 记录该主题下已经确认的结论、边界、判断与待决状态
- 作为该主题后续 planning / regression 的主入口

默认文件：
- `current-truth.md`
- `planning.md`（按需）
- `regression.md`（按需）

## 2. 主题内知识层

位置：`docs-discuss-and-distill/<YYYY-MM-DD-主题>/knowledge/`

用途：
- 承接只服务当前主题或主要服务当前主题的知识资料
- 放置支撑当前主题判断的资料、协议说明、机制说明、上下文材料
- 避免把这些内容直接塞进 `current-truth.md` 导致主文档过厚

说明：
- 当前只定义位置与职责，不预设固定正文格式

## 3. 所有主题共享知识层

位置：`docs-discuss-and-distill/knowledge/`

用途：
- 承接可被多个主题直接引用的共享知识
- 放置 API 协议、技术工作机制、系统约束、长期约定等内容

说明：
- 当前只定义位置与职责，不预设固定正文格式

## 4. Skill 固有 Reference 层

位置：`skills/discuss-and-distill/references/`

用途：
- 承接 skill 自身的操作规则、文档结构、主持模式与阶段模板
- 用于指导 skill 如何工作，而不是承接主题知识或共享知识

## 边界规则

- `current-truth.md` 记录当前主题下已经确认的结论、边界、判断与待决状态。
- 主题内知识与共享知识承接支撑这些判断的资料、协议说明、机制说明、上下文材料等可被引用的知识内容。
- 不要把“结论”与“依据”长期混写在同一主文档中。
- 当前只定义知识产物的**位置、职责与边界**，**不预设固定正文格式**。

## 使用建议

- 当某条知识只服务当前主题，优先放在该主题的 `knowledge/` 下。
- 当某条知识会被多个主题直接引用，优先放在 `docs-discuss-and-distill/knowledge/` 下。
- 当讨论的是 skill 自身如何运作、文档怎么组织、阶段模板如何定义，放在 `skills/discuss-and-distill/references/`。

## 流转规则

- 当主题内知识被确认可跨主题复用时，允许将其**晋升 / 复制**到 `docs-discuss-and-distill/knowledge/`。
- 当前只确认“允许流转”这条规则，不强制规定固定流程。
- 是否保留原主题下的知识副本，按实际使用需要决定；当前不强制要求迁移后删除原文。
