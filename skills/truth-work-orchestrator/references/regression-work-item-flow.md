# Regression Work-item Flow

当 `truth-work-orchestrator` 需要创建、维护或收口一个 **regression work-item** 时，优先参考这里。

> 注：这里的 **regression work-item / 工作承接对象** 不应被理解为狭义执行动作。

目标：
- 让regression work-item成为一个清晰的**验证型工作承接对象**，而不是“顺手补查一下”的临时动作
- 明确它与delivery work-item 的边界
- 让regression work-item在中断后也能依靠主入口文档恢复进度
- 稳定承接 drift handling：判断该更新 truth、修正 code，还是继续补证据
- 让当前 work-item 区保持可读：完成regression work-item退出 `work-items/`，进入顶层 `archive/work-items/`

## 1. 核心定位

regression work-item的默认心智是：
- **它默认不以实施新代码为主目标**
- **它负责判断当前代码是否仍与 truth 一致**
- **它的主要产出是判断、分类、证据与后续动作建议**

一句话：

> regression work-item = 一个基于 truth 的代码状态检查 work-item。

### 1.1 Continuity-by-Default Rule

regression work-item默认也遵守“接力不是单独步骤，而是对象底层要求”的规则：
- `work.md` 默认就是regression work-item的主入口与接力入口
- `verification.md` 负责展开详细证据，但不承担唯一恢复入口职责
- 暂停、切换会话、切换设备或切换执行者时，默认先更新主入口文档
- `handoff.md` 仅在主入口文档不足以承载复杂交接上下文时，作为增强件按需创建

## 2. 与delivery work-item 的边界

默认原则：
- 如果验证 / 回归只是当前代码实施闭环的一部分 → **留在delivery work-item 内完成**
- 如果验证目标已经独立、范围明显外扩、当前重点是先判断现状而不是继续实施 → **新起regression work-item**

更适合新起regression work-item的场景：
- 上线前 / 发布前的独立检查
- 对既有代码现状做专项回归
- 多模块联动后的统一验证
- 当前主要目标是判断 `truth 过时` 还是 `code 偏离`
- 需要先做检查结论，再决定是否新起delivery work-item 修复

## 3. 标准流程骨架

### 阶段 1：创建与挂接

目标：让regression work-item先成为一个明确对象。

此阶段至少要明确：
- 工作项类型：`regression`
- 挂接对象：模块 / 主题 / 子模块，或暂时为空
- 当前状态：建议从 `待回归` 或 `回归中` 起步
- 当前目标：本轮到底在检查什么

### 阶段 2：读取 truth 基线

目标：先明确“依据什么来判断当前代码对不对”。

至少要明确：
- 当前 truth 是什么
- 哪些行为 / 约束 / 结论是当前基线
- 哪些条目是本轮回归必须对照的依据

说明：
- regression work-item默认先读 truth，再看代码
- 如果 truth 本身就明显不稳，应先记录这一点，不要假装基线清晰

### 阶段 3：定义回归范围与方式

目标：明确这轮查什么、怎么查、查到什么程度。

至少覆盖：
- 本轮覆盖范围
- 本轮不覆盖范围
- 回归方式
- 证据来源

回归方式可以包括：
- 代码阅读
- 运行验证
- 测试结果核对
- 手工走查
- 日志 / 现象比对

### 阶段 4：执行回归检查

目标：把实际观察结果记录下来，而不是只保留一个模糊印象。

此阶段建议明确：
- 实际行为
- 观察结果
- 发现的问题
- 证据
- 当前判断倾向

说明：
- regression work-item不是只写最终结论
- 中间证据和观察结果也应留下，以支持后续恢复或复核

### 阶段 5：drift handling 分类

目标：判断当前偏差属于哪一类。

当前采用轻量三分法：
- `truth 过时`
- `code 偏离`
- `暂时无法判断`

默认动作：
- `truth 过时` → 更新 truth，不直接改代码
- `code 偏离` → 修正代码，不直接改 truth
- `暂时无法判断` → 挂起为待确认冲突，不自动改 truth，也不自动宣判代码错误

### 阶段 6：完成收口与后续动作

目标：让regression work-item不仅有结论，还有明确后续动作。

至少收口：
- 本次回归检查了什么
- 最终结论是什么
- 漂移分类是什么
- 建议动作是什么
- 是否需要新起delivery work-item 或回写 truth

说明：
- regression work-item可以以“判断完成”收口
- 不要求它自己继续承担代码修复
- 但要明确后续是谁来接、接什么
- 如果回归 work-item 挂接了模块 / 子模块 / 主题，且结论需要回补对象，则回补完成前不应标记为 `已完成`

## 4. 推荐状态集合

当前建议regression work-item使用下面这些状态：
- `待回归`
- `回归中`
- `待判断`
- `待回写`
- `已完成`
- `已挂起`

说明：
- regression work-item的状态机应服务于“检查 → 判断 → 处置建议”
- `待回写` 对挂接对象的回归 work-item 很重要：对象尚未回补前，不应跳到 `已完成`
- `已完成` 是终态，默认应很快转入 `archive/work-items/`，而不是长期停留在 `work-items/`

## 5. regression work-item的推荐文档集合

### 强必有
- `work.md`

### 高概率需要
- `verification.md`

### 按需添加
- `attachments/`
- `handoff.md`（仅在主入口文档不足以承载复杂交接上下文时）

### 各文档职责

#### `work.md`
作为regression work-item的主入口，用来维护：
- 工作项类型
- 挂接对象
- 当前状态
- 当前目标
- truth 基线
- 回归范围
- 当前发现
- 当前进展
- 接力入口 / 恢复入口
- 漂移分类
- 推荐动作
- 下一步动作

#### `verification.md`
用于承接较复杂regression work-item的详细检查记录，推荐在下面情况创建：
- 范围较大
- 证据较多
- 存在多轮检查或复核
- 需要把详细验证过程和 `work.md` 分开

#### `handoff.md`
作为增强型交接说明，推荐只在下面情况创建：
- 主入口文档不足以承载复杂交接上下文
- 需要跨多人 / 多轮长期接力，且额外压缩说明明显更省成本
- 需要把复杂背景、风险提醒或移交要求集中写给新的执行者

#### `attachments/`
用于承接regression work-item的截图、日志、导出物、测试报告等附件资料。

## 6. 可中断恢复规则

优先遵守下面规则：

1. `work.md` 必须能回答：**现在在查什么、依据什么在查、已经查到哪里、下一步查什么**。
2. `verification.md` 应尽量记录：**已检查范围、未检查范围、当前发现、当前证据**。
3. 如果准备中断，优先更新 `当前状态`、`当前发现`、`当前判断倾向`、`接力入口`、`下一步动作`。
4. 默认先依靠 `work.md` 与 `verification.md` 完成续推；只有主入口明显承载不下时，才补 `handoff.md`。
5. work-item 一旦完成收口，应退出 `work-items/` 并转入 `archive/work-items/`，不要让已完成 work-item 混在当前工作区里。
6. 恢复时默认顺序：先读 `work.md`，再读 `verification.md`；如果存在复杂交接补充，再读 `handoff.md`。

## 7. 推荐目录形态

### 当前 work-item 最小形态

```text
docs-TWO/work-items/YYMMDD-<中文工作项名>/
├── work.md
```

### 当前 work-item 常见扩展形态

```text
docs-TWO/work-items/YYMMDD-<中文工作项名>/
├── work.md
├── verification.md
└── attachments/
```

### 当前 work-item 按需增强交接形态

```text
docs-TWO/work-items/YYMMDD-<中文工作项名>/
├── work.md
├── verification.md
├── handoff.md
└── attachments/
```

### archive 归档形态

```text
docs-TWO/archive/work-items/YYMMDD-<中文工作项名>/
├── work.md
├── verification.md
└── ...
```
