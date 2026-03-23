# Output Model

`discuss-and-distill` 当前管理的产出采用“模块 + task”模型。

## 顶层结构

位置：`docs-discuss-and-distill/`

当前顶层包含三类主要产物：
- `modules/`：模块树
- `tasks/`：task 树
- `knowledge/`：共享知识层（当前仍保留为顶层目录，后续可继续讨论）

## 1. 模块树

位置：`docs-discuss-and-distill/modules/`

用途：
- 承接稳定的讨论对象
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

## 3. 共享知识层

位置：`docs-discuss-and-distill/knowledge/`

用途：
- 承接可被多个模块直接引用的共享知识
- 放置 API 协议、技术工作机制、系统约束、长期约定等内容

说明：
- 当前仍保留为顶层目录。
- 当前只定义位置与职责，不预设固定正文格式。

## 4. Task 树

位置：`docs-discuss-and-distill/tasks/`

用途：
- 承接围绕模块发起的一次执行活动
- 将代码落地流程从模块本体中抽离出来

当前第一类 task：
- 代码落地 task

说明：
- task 是执行层对象，不是模块内部阶段文件。
- 当前先定义 task 的位置与角色，不预设 task 内部模板。

## 5. Skill 固有 Reference 层

位置：`skills/discuss-and-distill/references/`

用途：
- 承接 skill 自身的操作规则、文档结构、主持模式与阶段模板
- 用于指导 skill 如何工作，而不是承接模块知识或共享知识

## 边界规则

- 模块层承接稳定对象；task 层承接围绕模块发起的一次执行活动。
- `current-truth.md` 放结论；`knowledge/` 放支撑这些结论的知识资料。
- `submodule-*.md` 放模块内部的子模块 truth；不要把子模块扩展成目录级递归结构。
- 当前只定义产物的**位置、职责与边界**，不预设固定正文格式。

## 已被替代的旧模型

下面这组旧规则已不再作为当前核心模型：
- 以“主题”为核心单位
- 在主题目录下默认放置 `planning.md` / `regression.md`

当前它们应视为被新的“模块 + task”模型替代。
