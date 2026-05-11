---
title: GitLab-默认分支合并工作流
module: 工作
type: sop
tags: [GitLab, 分支合并, worktree, 默认工作流, dev, gray]
updated_at: 2026-04-21
related_tools:
  - tools/merge_branch_via_detached_worktree.py
---

# GitLab-默认分支合并工作流

## 适用范围

适用于公司 GitLab 仓库中的日常分支合并场景，尤其是把当前工作分支或指定分支合并到 `dev`、`gray` 等集成分支的操作。

## 默认目标

在**不切换当前工作目录分支**的前提下，把源分支安全地合并到目标分支，并尽量避免污染当前工作区或误操作已有 worktree。

## 默认实现策略

1. **不切换当前工作目录分支**。
2. 先 `git fetch origin`，确保远程分支状态最新。
3. 默认使用 **detached 临时 worktree**，基于 `origin/<target>` 创建临时工作树。
4. 在临时 worktree 中创建临时分支并执行 merge。
5. 合并成功后，执行 `git push origin HEAD:<target>`。
6. 清理临时 worktree。

## 关于已有 target worktree 的默认规则

- 如果目标分支（如 `dev`、`gray`）已经在另一个 worktree 中检出，**默认不直接复用**该 worktree。
- 只有在明确确认以下条件时，才可以考虑复用：
  - worktree 干净，无未提交改动
  - 不处于 merge / rebase / cherry-pick 等中间状态
  - 可以确认该 worktree 当前无人依赖或可安全接管
- 在未确认上述条件前，优先继续使用 detached 临时 worktree。

## 这样做的原因

- 避免切换当前开发分支
- 避免污染当前工作区
- 避免误操作正在使用中的 target worktree
- 更适合脚本化和自动化执行
- 即使发生冲突，也更容易把问题限定在临时目录内处理

## 推荐工具

- `tools/merge_branch_via_detached_worktree.py`

## 典型用法

### 合并到 dev

```bash
python tools/merge_branch_via_detached_worktree.py \
  --repo /path/to/repo \
  --source <source_branch> \
  --target dev \
  --execute
```

### 合并到 gray

```bash
python tools/merge_branch_via_detached_worktree.py \
  --repo /path/to/repo \
  --source <source_branch> \
  --target gray \
  --execute
```

## 使用场景映射

- 当用户说“发测试”时，若该仓库约定测试环境由 `dev` 承载，则默认按本 SOP 合并到 `dev`。
- 当用户说“发灰”或“发灰度”时，若该仓库约定灰度环境由 `gray` 承载，则默认按本 SOP 合并到 `gray`。
- 若某个项目有自己的分支约定，应在项目级 SOP 中引用本 SOP，并覆盖目标分支名称或发布入口等项目特定信息。
