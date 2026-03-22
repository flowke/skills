# Document Location

默认把 `discuss-and-distill` 产出的讨论文档放到固定目录：`docs-discuss-and-distill/`。

## Default Rules

- 固定目录：`docs-discuss-and-distill/`
- 默认单位：每个主题一个目录，而不是每个主题一个单文件
- 主题目录名：`YYYY-MM-DD-<中文主题>/`
- 日期含义：主题首次建立日期，而不是最后更新时间
- 主文件名：`current-truth.md`
- 阶段文件名：按需创建 `planning.md`、`regression.md`
- 同主题后续讨论：继续维护原目录与原 `current-truth.md`
- 明显切换新主题：新建主题目录

## File Set Rule

默认最小文件集合如下：

- 必有：`current-truth.md`
- 按需：`planning.md`
- 按需：`regression.md`

规则说明：
- 新主题默认创建主题目录与 `current-truth.md`。
- 只有在进入代码落地规划阶段后，才创建 `planning.md`。
- 只有在进入代码完成后的回归阶段后，才创建 `regression.md`。
- 不要为尚未进入的阶段预建空文件。

## Naming Guidance

### 主题目录名

目录名优先体现主题，而不是会话本身；**优先使用简洁明确的中文标题**。

推荐示例：
- `2026-03-19-内部工具范围收敛/`
- `2026-03-19-认证重构方向/`
- `2026-03-19-产品定位讨论/`

避免过于宽泛或无信息量的名字，例如：
- `notes/`
- `discussion/`
- `today/`
- `2026-03-19-聊聊这个/`

### 目录内文件名

目录内文件名默认固定，不重复主题名：
- `current-truth.md`
- `planning.md`
- `regression.md`

不要使用下面这类冗余命名：
- `2026-03-19-认证重构方向-current-truth.md`
- `当前真相.md`
- `回归记录.md`

## Fallback Rule

满足下面情况时，可以不用中文主题目录名，改用英文或 slug：
- 用户明确要求英文命名
- 当前项目已有稳定的英文命名约定
- 文件系统、工具链或协作环境对中文命名不友好

## Reuse Rule

满足下面条件时，优先复用已有主题目录，而不是新建：
- 讨论主题没有变化，只是在继续收敛
- 当前目录中的 `current-truth.md` 仍然是本轮讨论的主入口
- 用户明确表示“继续上次那个”

## New Directory Rule

满足下面条件时，优先新建主题目录：
- 讨论目标明显切换
- 原主题已经收敛完成，当前是在开新主题
- 用户明确要求新开一份

## Override Rule

如果用户明确指定了目标路径、目标目录名或项目内既有文档位置，优先遵循用户指定，不强制写入 `docs-discuss-and-distill/`。
