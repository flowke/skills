# Works Implement Naming

## 1. 讨论目标
- 确定把 `$works` 中的 `Delivery` 正式改名为 `Implement`，并收敛新的概念边界。

## 2. 当前输入
- 用户认为现在的 `Delivery` 概念偏窄。
- 希望这个模式用来维护“代码实现这一整套流程”。
- 即使需求文档来自别处，而不是当前 `Discuss`，也应该可以直接创建一个对应容器。
- 用户已明确选择方案 A：把 `Delivery` 改名为 `Implement`。

## 3. 当前理解
- `Implement` 用来表达“围绕某个实现目标持续推进代码落地”。
- 它不应只被理解为 Discuss 之后的交付收口。
- 它可以承接多种上游来源：`Discuss`、外部 PRD、issue、设计稿、已有文档、口头指令等。

## 4. 当前板块
### 板块 A：Implement 的命名与定位
- 当前结论：正式采用 `Implement` 作为模式名。
- 当前结论：`Implement` 表示“某项实现工作的持续推进容器”，而不是“最后交付”。
- 待确认：是否需要把一些措辞进一步从“本轮”改成“当前阶段”，避免又收窄回单次交付。
- 下一步：把 skill 文案、引用文件名和文档模板同步切到 `Implement`。

## 5. 待确认问题
- `Implement` 的目录结构是否最终定为 `docs-works/implements/...`，还是保留 `deliveries` 目录只改模式名。

## 6. 下一步建议
- 选项 1：模式名先统一切到 `Implement`，目录名稍后再统一。
- 选项 2：模式名与目录名一起调整成 `docs-works/implements/...`。
