# Output Model

`truth-work-orchestrator` 当前管理的产出采用“模块 + 主题 + work-item + 知识”模型。

## 顶层结构

位置：`docs-TWO/`

当前顶层包含六类主要产物：
- `intake/`：待处理队列
- `modules/`：模块树
- `topics/`：主题树
- `work-items/`：当前仍在推进、挂起或待回补的工作项
- `knowledge/`：共享知识层
- `archive/`：归档层（当前主要承接已完成工作项）

## 0. 待处理队列

位置：`docs-TWO/intake/`

用途：
- 承接尚未正式进入 work-item 的原始资料
- 接收文字描述、文件、URL 等待处理输入
- 作为 work-item 之前的独立承接层

说明：
- `加入待处理` 与 `正式创建 work-item` 是两个不同动作。
- 待处理队列是独立顶层产物，不属于 work-item 生命周期内部的隐藏阶段。
- 顶层目录名已确定为 `intake/`。
- 每个 intake 项是目录级对象。
- 每个 intake 项当前最小包含：`note.md` 与 `attachments/`。
- `note.md` 用于简短说明；`attachments/` 用于承接原始资料。

## 1. 模块树

位置：`docs-TWO/modules/`

用途：
- 承接稳定的软件模块对象
- 记录模块本身的结论、边界、判断与待决状态
- 作为后续知识沉淀与 work-item 引用的对象层

### 模块目录的最小形态

每个模块目录当前最小包含：
- `current-truth.md`
- `knowledge/`
- 按需包含 `submodule-*`（可以是 `submodule-*.md` 文件，也可以是 `submodule-*/` 目录）

说明：
- `current-truth.md` 记录模块本身当前已经确认的结论、边界、判断与待决状态。
- `knowledge/` 承接只服务当前模块或主要服务当前模块的知识资料。
- 子模块支持轻量文件形态与复杂目录形态，两者都统一使用 `submodule-` 前缀命名。

## 2. 子模块 Truth

位置：模块目录内部，例如：
- `docs-TWO/modules/<module>/submodule-xxx.md`
- `docs-TWO/modules/<module>/submodule-xxx/current-truth.md`

规则：
- 子模块支持两种形态：
  - **轻量子模块**：`submodule-xxx.md`
  - **目录子模块**：`submodule-xxx/` 目录
- **默认子模块一律按轻量子模块处理。**
- 只有在当前上下文中被显式说明为 **“目录子模块”** 时，才创建目录结构子模块。
- 轻量子模块适合局部 truth 较少、暂时不需要独立知识层或下一层拆分的场景。
- 目录子模块适合已经需要独立 `knowledge/`、需要继续拆下一层子模块，或需要长期演化的场景。
- 目录子模块最小包含 `current-truth.md`；按需可继续包含 `knowledge/` 与下一层 `submodule-*`。
- 目录子模块支持分形展开：目录子模块内部可以继续出现轻量子模块或目录子模块。
- 子模块 truth 统一使用 `submodule-` 前缀命名，无论是文件还是目录。

## 3. 主题树

位置：`docs-TWO/topics/`

用途：
- 承接不明确属于某个软件模块的讨论对象
- 作为与模块并列的另一类稳定对象
- 可作为 work-item 的派生源或沉淀宿主

### 主题目录的最小形态

每个主题目录当前最小包含：
- `current-truth.md`

说明：
- 主题当前只承接一个 truth 文件。
- 主题不引入模块式的 `knowledge/` 与 `submodule-*` 分形结构。

## 4. 共享知识层

位置：`docs-TWO/knowledge/`

用途：
- 承接可被多个模块或主题直接引用的共享知识
- 放置 API 协议、技术工作机制、系统约束、长期约定等内容

说明：
- 共享知识层继续保留为顶层目录。
- 当前只定义位置与职责，不预设固定正文格式；如需轻量建议结构，可参考 `references/object-templates.md`。
- 共享知识默认推荐补充轻量元信息：`来源`、`更新时间`、`适用范围`、`相关对象`，但这些字段不是必填项。

## 5. Work-item 树

> 注：这里的 `work-item` 当前已采用新命名；这里的 **work-item / 工作承接对象** 不应被理解为狭义执行动作。

位置：`docs-TWO/work-items/`

默认理解：
- `docs-TWO/work-items/` 只承接当前仍在推进、挂起或待回补的工作项
- 已完成 work-item 转入 `docs-TWO/archive/work-items/`

用途：
- 承接围绕模块、主题或子模块发起的一次完整工作推进
- 也允许 work-item 从待处理队列中的资料正式启动后创建
- 允许 work-item 先独立创建，后续再挂接对象并沉淀结果

核心模型：
- work-item 可以先独立创建
- work-item 后续可以挂接到模块或主题
- work-item 完成后可以把结果沉淀到模块 / 主题 / 知识层
- work-item 可以从模块需求进入实施开始承接，而不应只在“开始执行代码”时才被理解为存在
- 对挂接对象的 work-item 而言，只有在回补对象完成后，才可视为真正完成
- 已完成 work-item 不继续留在 `work-items/`，而应转入 `archive/work-items/`
- 不是所有执行活动都必须先创建 work-item；当工作适合在当前会话内直接完成时，可直接走陪伴开发模式，并在完成后回填到模块 / 主题 / 知识层

说明：
- work-item 当前采用新名，语义上即 **工作承接对象（work-item）**，不是狭义执行动作，也不是稳定对象本体。
- 当前先定义 work-item 的位置与角色，不预设固定内部模板；如需轻量建议结构，可参考 `references/object-templates.md`。
- work-item 采用“类型 + 挂接方式”双维度模型。
- 第一版工作项类型当前先收为：`delivery`、`regression`。
- 第一版挂接方式至少包含：`独立创建`、`挂模块`、`挂主题`、`挂子模块`。
- `直接创建任务` 不再作为工作项类型，而归入挂接方式。
- 父工作项 / 子工作项首先是逻辑上的任务编排关系。
- 父 work-item 仍然是目录级对象；子 work-item 不单独起目录，而在父 work-item 目录内以 `subwork-*.md` 文件表达。
- 子工作项使用 `subwork-` 前缀命名，以保持可读性与轻量性。
- `subwork-*.md` 沿用与 `work.md` 相同的最小字段集合：`工作项类型`、`挂接对象`、`当前状态`。
- work-item 目录命名规则采用：`YYMMDD-<中文任务名>/`。
- 新创建 work-item 默认放在 `docs-TWO/work-items/`。
- 任务完成并收口后，目录移动到 `docs-TWO/archive/work-items/`。
- `工作项类型` 与 `挂接方式` 不编码进目录名，而放入 work-item 内容字段中。
- 每个 work-item 目录至少包含一个入口文件：`work.md`。
- `work.md` 的最小字段包括：`工作项类型`、`挂接对象`、`当前状态`。
- `挂接方式` 当前不作为最小必选字段；多数场景下可由 `挂接对象` 推导。
- `来源 intake 项` 不作为必选字段，但正式作为可选字段保留，用于承接从 intake 到 work-item 的追溯链。
- work-item 的更具体内容字段与内部结构，按类型继续细化；delivery work-item 的流程与推荐文档集合，见 `references/delivery-work-item-flow.md`。
- 对delivery work-item 而言，除 `work.md` 外，可按需补 `implementation-plan.md`、`subwork-*.md`、`verification.md` 等内部文档；`handoff.md` 仅在主入口文档不足以承载复杂交接上下文时，作为增强件按需补充。
- 对delivery work-item 而言，规划文档如果需要保留，应放在 work-item 目录内，例如 `implementation-plan.md`；不要把模块 / 主题层的 `planning.md` 当作默认结构恢复。
- 对delivery work-item 而言，代码完成后的验证与必要回归，默认应在同一个 work-item 内闭环完成；不再默认外拆独立regression work-item。
- 对delivery work-item 而言，`work.md` 及按需存在的 `subwork-*.md` 默认都需要支持中断后续推；至少应能从主入口文档中恢复当前路径选择、当前进展、接力入口与下一步动作。
- 对独立 `regression` work-item 而言，其流程、文档集合与恢复规则，见 `references/regression-work-item-flow.md`。

## 5.1 Archive 归档层

位置：`docs-TWO/archive/`

当前默认结构：
- `docs-TWO/archive/work-items/`：已完成并退出当前工作区的 work-item

说明：
- archive 是顶层归档分类，不再把归档层塞在 `work-items/` 内部。
- 当前默认只归档 work-item；未来如果出现其他稳定的归档需求，再按对象类型扩展子目录。
- archive 表示退出当前工作区，不表示删除。

## 6. Regression Work-item 的 Drift Handling

当regression work-item 发现“代码与 truth 不一致”时，当前采用轻量三分法：
- `truth 过时`：代码合理，但 truth 没有同步更新
- `code 偏离`：truth 仍然成立，但代码跑偏了
- `暂时无法判断`：当前证据不足，不能立即判断该改 truth 还是改 code

默认动作：
- `truth 过时` → 更新 truth，不直接改代码
- `code 偏离` → 修正代码，不直接改 truth
- `暂时无法判断` → 挂起为待确认冲突，不自动改 truth，也不自动宣判代码错误

鲁棒性原则：
- 先分类，再动作
- 在证据不足时，不自动回写 truth，也不自动修正代码

## 6.1 记忆回填（Memory Backfill）

默认理解：
- 记忆回填是一条流程，不是新的顶层对象类型
- 它用于把 skill 外发生的实现 / 修复 / 技术判断，回填到现有 truth / knowledge 体系中

默认落点规则：
- 目标模块明确 → 优先回填模块 `current-truth.md` 或模块 `knowledge/`
- 可跨对象复用 → 优先回填顶层 `knowledge/`
- 暂时无法判断归属 → 先进入 `intake/` 作为待归类记忆项

如需完整流程规则，见 `references/memory-backfill-flow.md`。

## 7. Skill 固有 Reference 层

位置：`skills/truth-work-orchestrator/references/`

用途：
- 承接 skill 自身的操作规则、文档结构、主持模式与轻量对象模板
- 用于指导 skill 如何工作，而不是承接模块知识、主题知识或共享知识

## 术语约定

- 当前默认术语采用：**模块**。
- 这里的“模块”指稳定的软件结构对象，对应目录层为 `modules/`。
- 不再保留“组件”作为并行默认术语；如具体上下文必须使用别名，应在局部说明，不回写为全局默认规则。

## 边界规则

- 模块与主题都是稳定对象，但前者偏软件模块，后者偏非软件模块型讨论对象。
- work-item 层承接围绕对象发起的一次完整工作推进；共享知识层承接跨对象复用知识。
- `current-truth.md` 放结论；`knowledge/` 放支撑这些结论的知识资料。
- 子模块支持轻量文件与目录两种形态：默认使用 `submodule-*.md`。
- 只有被显式说明为 **目录子模块** 时，才使用 `submodule-*/current-truth.md`。
- 目录子模块支持继续嵌套下一层 `submodule-*`，形成分形结构；但默认不为了结构而递归。
- 当前只定义产物的**位置、职责与边界**，不预设固定正文格式。
