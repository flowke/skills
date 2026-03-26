# Truth Work Orchestrator Work-item 模型说明

## 当前结论

`truth-work-orchestrator` 已完全进入 `work-item` 终态口径。

当前正式对象模型为：
- `intake`
- `modules`
- `topics`
- `work-items`
- `knowledge`
- `archive/work-items`

其中：
- `work-item` 是正式对象名
- `work` 只作为口语简称使用，不作为系统正式命名
- 已完成 work-item 不留在当前工作区，而是转入 `docs-TWO/archive/work-items/`

## Work-item 的正式语义

`work-item` 不是狭义执行动作，也不是临时待办卡片。

它是一个**工作承接对象**，可以承接：
- 模块 / 子模块 / 主题提出的新需求
- 从 intake 正式启动的工作
- 需要跨会话、跨设备、跨执行者续推的复杂推进
- 需要明确记录验证、回补、恢复入口与证据链的工作

因此：
- 提模块需求时，可以立即创建一个挂接该对象的 `work-item`
- 在挂接对象上同时留下极轻量的 `intent / declared` 痕迹
- work-item 推进完成后，把稳定结果回补到挂接对象或知识层

## 类型与边界

当前正式 work-item 类型收敛为：
- `delivery`
- `regression`

说明：
- `delivery` 承接从需求进入实施、验证、修正、回补与收口的闭环
- `regression` 承接独立验证、漂移判断与后续动作建议
- 验证如果只是 delivery 闭环的一部分，默认留在同一个 delivery work-item 内完成，而不是机械外拆

## 完成定义

对于挂接了模块 / 子模块 / 主题的 work-item：

> 只有在回补挂接对象完成后，才可标记为完成。

这意味着：
- 实施完成 ≠ 完成
- 验证完成 ≠ 完成
- 只有回补完成，才算真正完成

完成后的默认动作：
- 从 `docs-TWO/work-items/` 移出
- 转入 `docs-TWO/archive/work-items/`
- 保留证据链，不删除

## 接力哲学

接力不是一个附加步骤，而是整个 skill 的底层哲学。

默认要求：
- `current-truth.md`
- `work.md`
- `subwork-*.md`
- `verification.md`

这些主入口文档本身就应足以支持恢复。

因此：
- 默认不依赖 `handoff.md`
- 只有当主入口文档不足以承载复杂交接上下文时，才按需补一个 `handoff.md`
- 更新对象时，要同步更新当前状态、当前进展、恢复入口、下一步动作与不要误判为已完成的事项

## 子模块结构

当前子模块采用双形态模型：
- 默认：**轻量子模块** → `submodule-xxx.md`
- 显式说明“目录子模块”时：**目录子模块** → `submodule-xxx/current-truth.md`

目录子模块支持继续分形展开。

默认规则：
- 没有显式说明“目录子模块”时，一律按轻量子模块创建
- 只有需要独立 `knowledge/`、需要继续下钻或需要长期演化时，才使用目录子模块

## 模块提需求的推荐 workflow

推荐 workflow：
1. 在模块 / 子模块上提出新需求
2. 立即创建挂接该对象的 work-item
3. 在模块 / 子模块 truth 上留下极轻量的 `intent / declared` 痕迹
4. 推进 work-item，完成实施 / 验证 / 回补
5. 回补完成后，把 work-item 标完成并移入 archive

这个 workflow 的重点不是“把需求降成执行动作”，而是：
- 为该需求立刻创建一个正式工作承接对象
- 让实现、验证、回补、归档和恢复都落在同一条清晰链路里

## 当前目录约定

```text
docs-TWO/
├── intake/
├── modules/
├── topics/
├── work-items/
├── knowledge/
└── archive/
    └── work-items/
```

work-item 目录的最小形态：

```text
docs-TWO/work-items/YYMMDD-<中文工作项名>/
├── work.md
├── implementation-plan.md        # 按需
├── verification.md               # 按需
├── subwork-*.md                  # 按需
├── handoff.md                    # 仅在主入口不足时按需
└── attachments/                  # 按需
```

## 当前状态

当前仓库中的 `truth-work-orchestrator` 已按上述终态口径统一：
- 正式对象名统一为 `work-item`
- 当前工作目录统一为 `work-items/`
- 归档目录统一为 `archive/work-items/`
- 入口文件统一为 `work.md`
- 子工作项统一为 `subwork-*.md`
- 类型统一为 `delivery` / `regression`
