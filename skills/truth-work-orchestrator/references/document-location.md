# Document Location

默认把 `truth-work-orchestrator` 的产出放到固定目录：`docs-TWO/`。

## Default Rules

- 固定目录：`docs-TWO/`
- 顶层结构：`intake/`、`modules/`、`topics/`、`tasks/`、`knowledge/`
- `tasks/` 内部分为：`active/`、`archive/`
- 默认按**对象性质**落点，而不是按对话轮次落点
- 默认先判断当前内容属于：待处理资料、稳定对象、执行对象，还是共享知识
- 用户明确指定路径时，优先遵循用户指定

## Top-Level Placement Rule

### 1. `intake/`

位置：`docs-TWO/intake/`

适用场景：
- 用户只是把资料交给 agent，尚未正式开始处理
- 当前内容主要是原始文字描述、文件、URL、截图、表格等待处理输入
- 用户表达的是“先收一下 / 先放进去 / 之后再处理”

默认形态：
- 每个 intake 项是目录级对象
- 最小包含：`note.md`、`attachments/`

命名建议：
- 目录名采用：`YYMMDD-<中文待处理项名>/`
- 名称优先描述资料主题，而不是“待办 1”“稍后处理”这类弱语义名字

### 2. `modules/`

位置：`docs-TWO/modules/`

适用场景：
- 当前讨论对象是稳定的软件模块
- 后续会持续承接 truth、模块内知识或围绕该对象的 task
- 该对象更像系统中的结构单元，而不是一次性话题

默认形态：
- 模块目录最小包含：`current-truth.md`、`knowledge/`
- 按需可继续包含 `submodule-*.md` 或 `submodule-*/`
- 模块目录中的主入口固定为 `current-truth.md`

子模块选型建议：
- **默认子模块 = 轻量子模块** → 使用 `submodule-*.md`
- 只有在当前上下文被显式说明为 **目录子模块** 时，才使用 `submodule-*/` 目录
- 目录子模块目录的主入口固定为 `current-truth.md`

命名建议：
- 模块目录名优先使用简洁明确的中文标题
- 目录名优先体现模块本体，而不是本次会话的动作
- 如果已有稳定英文命名约定，可改用英文或 slug

### 3. `topics/`

位置：`docs-TWO/topics/`

适用场景：
- 当前讨论对象不明确属于某个软件模块
- 它是一个稳定话题，但不需要模块式的内部结构
- 后续可能从该主题派生 task，或接收 task 的沉淀结果

默认形态：
- 每个主题目录最小包含：`current-truth.md`

命名建议：
- 目录名采用：`YYMMDD-<中文主题>/`
- 日期表示该主题首次建立日期，而不是最后更新时间

### 4. `tasks/`

位置：`docs-TWO/tasks/`

内部结构：
- `docs-TWO/tasks/active/`：当前仍在推进、挂起或待回写的 task
- `docs-TWO/tasks/archive/`：已经完成并退出 active 工作区的 task

适用场景：
- 当前需要承接一次执行活动，而不是继续只停留在稳定对象 truth
- 任务可能来自 intake，也可能直接独立创建
- 任务可能挂接模块、主题或子模块，也可能暂时不挂接任何对象

默认形态：
- 新 task 默认创建在 `docs-TWO/tasks/active/` 下
- 每个 task 是目录级对象
- 目录至少包含：`task.md`
- 子任务不单独建目录，统一以 `subtask-*.md` 形式放在父 task 目录内
- 已完成 task 立即从 `active/` 移到 `archive/`，不继续留在 active 原位置

命名建议：
- task 目录名采用：`YYMMDD-<中文任务名>/`
- 不把任务类型或挂接方式编码进目录名
- 任务类型、挂接对象、当前状态写入 `task.md`

### 5. `knowledge/`

位置：`docs-TWO/knowledge/`

适用场景：
- 当前内容可被多个模块或主题直接引用
- 内容更像协议说明、技术机制、系统约束、长期约定等共享知识
- 该内容不适合混入单个模块 / 主题的 `current-truth.md`

默认形态：
- 当前只固定目录位置与角色
- 正文格式默认开放；如需轻量建议结构，可参考 `references/object-templates.md`

## Stable Object vs Execution Object

优先用下面的判断来区分应该落到哪里：

- 如果是在描述“这个对象目前成立的结论、边界、判断与未决” → 优先落到 `modules/` 或 `topics/`
- 如果是在承接“围绕某对象发起的一次执行活动” → 优先落到 `tasks/active/`
- 如果只是“先接收资料，稍后再决定是否处理” → 优先落到 `intake/`
- 如果是在记录“可跨对象复用的依据型知识” → 优先落到 `knowledge/`

## Reuse Rule

满足下面条件时，优先复用已有对象，而不是新建：
- 讨论对象没有变化，只是在继续收敛
- 现有 `current-truth.md` 仍然是本轮讨论的主入口
- 当前只是为已有模块 / 主题补知识、补边界、补未决项
- 当前只是继续推进已有 task，而不是发起新的一次执行活动

## New Object Rule

满足下面条件时，优先新建对象：
- 讨论对象明显切换，已不属于原模块 / 主题
- 需要承接一次新的执行活动，且不应混入旧 task
- 用户明确要求新开一份
- 当前输入只是待处理资料，还不适合直接转入已有 task
- 当前输入属于“值得记住，但还未确定最终归属”的待归类记忆

## Naming Guidance

### 目录命名

默认优先使用简洁明确的中文标题，避免下面这类弱语义命名：
- `notes/`
- `discussion/`
- `today/`
- `temp/`
- `misc/`
- `先这样/`

### 固定文件名

默认固定文件名如下：
- 稳定对象入口：`current-truth.md`
- task 入口：`task.md`
- 子任务：`subtask-*.md`
- 轻量子模块 truth：`submodule-*.md`
- 复杂子模块目录入口：`submodule-*/current-truth.md`
- intake 说明：`note.md`

不要重复把主题名或模块名塞进固定文件名里。

## Fallback Rule

满足下面情况时，可以不用中文目录名，改用英文或 slug：
- 用户明确要求英文命名
- 当前项目已有稳定的英文命名约定
- 文件系统、工具链或协作环境对中文命名不友好

## Override Rule

如果用户明确指定了目标路径、目标目录名或项目内既有文档位置，优先遵循用户指定，不强制写入 `docs-TWO/`。
