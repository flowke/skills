---
name: truth-doc-orchestrator
description: Truth-driven documentation system for modules under docs-specs-flo. Use when Codex needs to establish facts, define active intents, express intent graphs with Mermaid, specify behavioral semantics, plan engineering rollout, define verification, settle completed intents, update current truth, or promote shared truths.
---

# Truth Doc Orchestrator

将 `docs-specs-flo/` 重构为一套 **truth-driven documentation system**：先建立事实真相，再定义意图真相，再展开行为语义、工程落地与验证闭环，最终把结果沉淀为模块当前真相与共享真相。

## Core Truth Model

先区分 6 类信息：

- **事实来源**：原始依据，回答“凭什么这么说”
- **事实真相**：基于来源确认后的现实结论，回答“现在真实是什么”
- **意图真相**：本次希望系统成立的目标定义，回答“这次要变成什么样”
- **当前真相**：当前时点团队应优先信任的模块事实与能力总览
- **假设**：为了推进而暂时接受的前提
- **待确认项**：仍未决定、会影响事实判断或意图定义的关键问题

## Repository Structure

默认文档根目录为 `docs-specs-flo/`。

- 全局导航：`index/00-全局导航.md`
- 共享真相：`shared-truths/`
- 模块入口：`modules/<模块名>/00-模块导航.md`
- 模块事实区：`modules/<模块名>/facts/`
- 活跃意图区：`modules/<模块名>/intents/active/<意图ID>-<意图名>/`
- 已沉淀意图区：`modules/<模块名>/intents/settled/`

模块事实区固定入口：
- `facts/00-事实索引.md`
- `facts/10-当前能力地图.md`

单个活跃意图固定使用以下 6 份主文档：
1. `00-意图总览.md`
2. `10-事实基础.md`
3. `20-意图图谱.md`
4. `30-行为语义.md`
5. `40-工程落地.md`
6. `50-验证与回归.md`

辅助目录：
- `attachments/`：补充图片、导出物、样例材料等

## Working Modes

先识别当前工作属于哪一类：

1. 事实来源整理
2. 事实区维护
3. 活跃意图定义
4. 意图图谱整理
5. 行为语义整理
6. 工程落地规划
7. 验证与回归整理
8. 沉淀整理
9. 共享真相晋升
10. 模块导航维护

## Core Workflow

### A. 活跃意图标准顺序

1. 识别并补齐事实来源
2. 沉淀事实真相到 `facts/`
3. 写 `00-意图总览.md`
4. 写 `10-事实基础.md`
5. 写 `20-意图图谱.md`
6. 写 `30-行为语义.md`
7. 写 `40-工程落地.md`
8. 写 `50-验证与回归.md`
9. 意图完成后执行沉淀整理
10. 生成 `intents/settled/<意图ID>-<意图名>.md`
11. 更新 `facts/10-当前能力地图.md`
12. 必要时晋升到 `shared-truths/`
13. 更新 `00-模块导航.md`
14. 从 `intents/active/` 移除原完整目录

### B. 沉淀整理目标

沉淀的对象不是“过程文档本身”，而是：

- 新确认的事实真相
- 已兑现的意图真相
- 已证实或证伪的假设
- 模块当前真相的更新
- 可跨模块复用的共享真相

## Document Semantics

- `facts/00-事实索引.md`：事实导航层
- `facts/10-当前能力地图.md`：当前真相总览层
- `00-意图总览.md`：意图真相入口层
- `10-事实基础.md`：意图成立的事实底座
- `20-意图图谱.md`：意图的正式图谱表达层
- `30-行为语义.md`：意图到系统行为的映射层
- `40-工程落地.md`：受事实约束的工程实施层
- `50-验证与回归.md`：意图兑现验证层
- `intents/settled/<意图>.md`：真相更新结果层

## Hard Gates

- **事实未立，不进入意图**
- **意图未清，不进入行为**
- **行为未清，不进入工程**
- **验证未闭环，不算完成**
- **当前真相未更新，不算沉淀完成**

## Mermaid Usage Rule

Mermaid 是正式表达工具，不是装饰。

当出现以下情况时，优先用 Mermaid：
- 角色多于 2 个
- 状态多于 3 个
- 存在异步交互
- 存在明显分支、回退、补偿逻辑
- 纯文字已经难以稳定表达意图或行为

推荐图种：
- `flowchart`：目标路径、模块结构、分支流转
- `sequenceDiagram`：角色交互、接口时序
- `stateDiagram-v2`：状态机、生命周期
- `erDiagram`：对象关系、领域结构
- `journey`：用户路径

## Output Contracts

### 沉淀结果固定输出结构

执行“沉淀整理”时，优先输出为：

```md
# <模块名> <意图ID>-<意图名> 沉淀结果

## 1. 新确认的事实真相
## 2. 已兑现的意图真相
## 3. 假设验证结果
## 4. 当前真相更新
## 5. 共享真相晋升
## 6. 原活跃意图目录处理
```

若某项为空，显式写“无”或“本次无需更新”。

## References

按需读取以下文件，不要一次性加载全部细节：

- truth model：`references/truth-model.md`
- repository structure：`references/repository-structure.md`
- document semantics：`references/document-semantics.md`
- active intent workflow：`references/active-intent-workflow.md`
- settlement workflow：`references/settlement-workflow.md`
- diagram guidelines：`references/diagram-guidelines.md`
- templates：`references/templates.md`
- status model：`references/status-model.md`
