# Output Model

`discuss-and-distill` 当前管理的产出采用“模块 + 主题 + task + 知识”模型。

## 顶层结构

位置：`docs-discuss-and-distill/`

当前顶层包含四类主要产物：
- `modules/`：模块树
- `topics/`：主题树
- `tasks/`：task 树
- `knowledge/`：共享知识层

## 1. 模块树

位置：`docs-discuss-and-distill/modules/`

用途：
- 承接稳定的软件模块对象
- 记录模块本身的结论、边界、判断与待决状态
- 作为后续知识沉淀与 task 引用的对象层

### 模块目录的最小形态

每个模块目录当前最小包含：
- `current-truth.md`
- `knowledge/`
- `submodule-*.md`

说明：
- `current-truth.md` 记录模块本身当前已经确认的结论、边界、判断与待决状态。
- `knowledge/` 承接只服务当前模块或主要服务当前模块的知识资料。
- `submodule-*.md` 是模块内部的子模块 truth 文件。

## 2. 子模块 Truth

位置：模块目录内部，例如：
- `docs-discuss-and-distill/modules/<module>/submodule-xxx.md`

规则：
- 子模块 **不是目录级对象**。
- 子模块只作为模块目录内部的独立轻文件存在。
- 子模块 truth 统一使用 `submodule-` 前缀命名。

## 3. 主题树

位置：`docs-discuss-and-distill/topics/`

用途：
- 承接不明确属于某个软件模块的讨论对象
- 作为与模块并列的另一类稳定对象
- 可作为 task 的派生源或沉淀宿主

### 主题目录的最小形态

每个主题目录当前最小包含：
- `current-truth.md`

说明：
- 主题当前只承接一个 truth 文件。
- 主题不引入模块式的 `knowledge/` 与 `submodule-*.md` 结构。

## 4. 共享知识层

位置：`docs-discuss-and-distill/knowledge/`

用途：
- 承接可被多个模块或主题直接引用的共享知识
- 放置 API 协议、技术工作机制、系统约束、长期约定等内容

说明：
- 共享知识层继续保留为顶层目录。
- 当前只定义位置与职责，不预设固定正文格式。

## 5. Task 树

位置：`docs-discuss-and-distill/tasks/`

用途：
- 承接围绕模块或主题发起的一次执行活动
- 也允许 task 先独立创建，后续再挂接对象并沉淀结果

核心模型：
- task 可以先独立创建
- task 后续可以挂接到模块或主题
- task 完成后可以把结果沉淀到模块 / 主题 / 知识层

说明：
- task 是执行层对象，不是稳定对象本体。
- 当前先定义 task 的位置与角色，不预设 task 内部模板。
- 第一版 task 类型集合至少包含：直接创建任务、基于子模块的代码落地任务、面向模块的回归测试任务。
- task 的更具体命名规则与内部结构仍待后续收敛。

## 7. 回归测试 Task 的 Drift Handling

当回归测试 task 发现“代码与 truth 不一致”时，当前采用轻量三分法：
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

## 6. Skill 固有 Reference 层

位置：`skills/discuss-and-distill/references/`

用途：
- 承接 skill 自身的操作规则、文档结构、主持模式与阶段模板
- 用于指导 skill 如何工作，而不是承接模块知识、主题知识或共享知识

## 边界规则

- 模块与主题都是稳定对象，但前者偏软件模块，后者偏非软件模块型讨论对象。
- task 层承接围绕对象发起的一次执行活动；共享知识层承接跨对象复用知识。
- `current-truth.md` 放结论；`knowledge/` 放支撑这些结论的知识资料。
- `submodule-*.md` 放模块内部的子模块 truth；不要把子模块扩展成目录级递归结构。
- 当前只定义产物的**位置、职责与边界**，不预设固定正文格式。

## 已退役的旧产物

下面这组旧产物当前已退役，不再作为核心模型的一部分：
- `planning.md`
- `regression.md`

它们当前既不属于模块目录的默认文件，也不作为 task 的默认或可选文件继续保留。

## 已被替代的旧模型

下面这组旧规则已不再作为当前核心模型：
- 以“主题”为核心总单位
- 在主题目录下默认放置 `planning.md` / `regression.md`

当前它们应视为被新的“模块 + 主题 + task + 知识”模型替代。
