# discuss skill 升级需求对齐

## 当前阶段
- canonical identity 与目录迁移已完成
- 顶层产出模型已稳定为 `intake / modules / topics / tasks / knowledge`
- 代码落地 task、独立回归任务、记忆回填流程的 reference 已补齐
- 历史演化记录已迁移到 `history-archive.md`

## 当前有效边界
- `truth-work-orchestrator` 当前已不只是“讨论 / 编排”skill，而是一个以 truth 为核心、可承接 **对齐 → 编排 → 实施 → 验证 / 回归 → 回写 → 记忆回填 → 恢复续推** 的工作闭环 skill。
- skill **负责技术实施与技术验证闭环**，包括：代码落地 task、独立回归任务、记忆回填、文档续推恢复。
- skill **不替代**：最终业务拍板、最终业务验收、最终上线决策、完整项目管理职能。
- 轻重分流不再作为本 skill 的固定首步；只要当前工作需要 `truth / task / memory / recovery` 闭环，就可以直接进入本 skill。

## 当前真相
- canonical identity：`truth-work-orchestrator`
- 当前目标：把旧的 discuss 类 skill 收敛为一个以 truth 为核心、可稳定承接对象、任务、知识与记忆回填的工作闭环 skill。
- 当前主骨架：
  - **需求对齐 / truth 稳定化**
  - **一致性复盘 / 路径选择**
  - **对象编排 / task 承接**
  - **实施 / 验证 / 回归闭环**
  - **回写 / 记忆回填 / 持续沉淀**
- 一致性复盘仍是进入实施前的必要环节，至少覆盖：冲突检查、相互影响检查、遗漏项检查、待决策点检查。
- “回归”当前定义为：**代码实现后的技术验证与检查**；不再只理解为“写完代码后另开一轮外部动作”。

### 产出模型（当前生效）
- 顶层目录：`docs-TWO/`
- 顶层结构：
  - `intake/`：待处理资料与待归类记忆
  - `modules/`：稳定的软件模块对象
  - `topics/`：非软件模块型稳定讨论对象
  - `tasks/`：执行对象
  - `knowledge/`：跨对象共享知识
- 稳定对象入口文件：`current-truth.md`
- task 入口文件：`task.md`
- 子任务文件：`subtask-*.md`
- 子模块 truth 文件：`submodule-*.md`

### task 模型（当前生效）
- task 采用“**任务类型 + 挂接方式**”双维度模型。
- 当前主要任务类型：
  - `代码落地`
  - `回归测试`
- 当前主要挂接方式：
  - `独立创建`
  - `挂模块`
  - `挂主题`
  - `挂子模块`
- task 可以先独立创建，后续再挂接对象。
- task 完成后可以把结果沉淀到模块 / 主题 / knowledge 层。

### 代码落地 task（当前生效）
- 代码落地 task 默认承接：**实施 → 验证 → 必要回归 → 修正 → 回写** 的闭环。
- 默认不再把验证 / 回归机械拆成一个新 task。
- 只有当验证目标明显独立、范围明显外扩时，才按需新起独立 `回归测试` task。
- 代码落地 task 的关键目标：
  - 选择最优落地路径
  - 尽量减少返工
  - 支持中断后恢复进度
- 代码落地 task 的主要文档：
  - 必有：`task.md`
  - 按需：`implementation-plan.md`、`subtask-*.md`、`handoff.md`、`verification.md`、`attachments/`
- `task.md` 至少应能回答：
  - 现在在做什么
  - 为什么这么做
  - 已经做到哪里
  - 下一步做什么

### 独立回归任务（当前生效）
- 独立 `回归测试` task 是一个**验证型 task**，默认不以实施新代码为主目标。
- 它负责判断：当前代码是否仍与 truth 一致，并给出 drift handling 分类与后续动作建议。
- 它更适合用于：
  - 上线前 / 发布前的独立检查
  - 对既有代码现状做专项回归
  - 多模块联动后的统一验证
  - 需要先判断 `truth 过时` 还是 `code 偏离`
- drift handling 当前采用轻量三分法：
  - `truth 过时`
  - `code 偏离`
  - `暂时无法判断`
- 默认动作：
  - `truth 过时` → 更新 truth
  - `code 偏离` → 修正代码
  - `暂时无法判断` → 挂起为待确认冲突
- 独立回归任务的主要文档：
  - 必有：`task.md`
  - 高概率需要：`verification.md`
  - 按需：`handoff.md`、`attachments/`

### 记忆回填（当前生效）
- 记忆回填是一条**流程**，不是新的顶层对象类型。
- 它用于把 skill 外发生的实现 / 修复 / 技术判断，回填到现有 truth / knowledge 体系中。
- 默认落点规则：
  - 目标模块明确 → 优先回填模块 `current-truth.md` 或模块 `knowledge/`
  - 可跨对象复用 → 优先回填顶层 `knowledge/`
  - 暂时无法判断归属 → 先进入 `intake/` 作为待归类记忆项
- 记忆回填的目标不是保存全过程，而是保留“下次仍值得知道的上下文”。

### 续推恢复（当前生效）
- 所有 task 默认都应支持中断后恢复。
- 恢复优先依赖文档，而不是依赖当前会话记忆。
- 代码落地 task 恢复时默认优先看：`task.md` → `verification.md` → `handoff.md`（如果有）
- 独立回归任务恢复时默认优先看：`task.md` → `verification.md` → `handoff.md`（如果有）

### 当前主要 reference（当前生效）
- `references/output-model.md`
- `references/document-location.md`
- `references/object-templates.md`
- `references/code-delivery-task-flow.md`
- `references/regression-task-flow.md`
- `references/memory-backfill-flow.md`

## 待确认项
- 当前暂无阻塞性的待确认项。

## 未决问题
- 当前暂无阻塞性的未决问题。

## 冲突与影响检查
- 旧的“本 skill 不执行编码实现 / 不执行回归 / 不做测试动作”的表述已失效；若历史记录中仍出现，以本文件当前版本为准。
- 旧的“主题 + planning/regression”模型已被新的“模块 + 主题 + task + 知识”模型替代。
- 代码落地 task 与独立回归任务的边界已重新收口：默认闭环留在代码落地 task 内，只有验证目标独立时才新起回归任务。
- 记忆回填已明确为流程，而不是新的顶层对象。

## 下一步聚焦
1. 继续讨论模块功能。
   - 建议：按当前有效边界来定义模块职责、输入输出、与 task / knowledge / 记忆回填的关系。
   - 建议：优先选择一个具体模块做样例讨论，避免再次泛化。
2. 用真实样例验证新模型是否顺手。
   - 建议：各做一个 `代码落地 task`、`独立回归任务`、`待归类记忆` 的样例目录。
   - 建议：如果样例中暴露字段或边界问题，再做轻量修正。
