# Stage Document Templates (Deprecated)

这个 reference 已退役，仅作为兼容说明保留。

## 当前状态

- 旧模型中的 `planning.md` 与 `regression.md` 已不再作为 `truth-work-orchestrator`（历史别名：`discuss-and-distill`）的默认核心产物。
- 当前默认产物模型已切换为：`intake/`、`modules/`、`topics/`、`tasks/`、`knowledge/`。
- 新使用场景下，不再从这个文件创建新的阶段文档。

## 请改用

- 产物分层、对象边界与目录角色：`references/output-model.md`
- 落点、命名、复用或新建规则：`references/document-location.md`
- intake / task / module / topic / knowledge 的轻量模板建议：`references/object-templates.md`

## 兼容说明

如果历史文档中仍存在 `planning.md` 或 `regression.md`：
- 可继续保留其历史内容，不必为了迁移立即删除
- 但它们不再作为新的默认创建目标
- 新的流程与产物应优先按照新模型落到对应对象层
