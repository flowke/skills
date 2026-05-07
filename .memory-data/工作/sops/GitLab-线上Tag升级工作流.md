---
title: GitLab-线上Tag升级工作流
module: 工作
type: sop
tags: [GitLab, tag, 发布, 自动化, git.100tal]
updated_at: 2026-05-07
related_tools:
  - tools/gitlab_release_tag.py
---

# GitLab-线上Tag升级工作流

## 适用范围

适用于 `git.100tal.com` 上大多数项目的线上 tag 升级场景。

## 默认规则

1. MR 必须先合并到 `master`。
2. 默认基于 `origin/master` 打 tag。
3. 先 `git fetch origin --prune --tags`。
4. 读取最新 `vX.Y.Z` 格式 tag。
5. 默认按 `patch` 升级。
6. 新 tag 默认打在 `origin/master` 的最新 merge commit 上。
7. tag 推送成功后，默认把**当前工作分支 fast-forward 到 `origin/master`**，用于同步本地分支基线；若具体项目文档另有差异说明，则以项目差异为准。
8. tag 说明优先使用用户显式给定文案；若用户未给，则默认由我根据本次工作内容总结成一句简短话；若仍缺失明显上下文，再退回到 MR 标题或目标 ref 的最新提交标题。

## 通用工具

使用：`tools/gitlab_release_tag.py`

### 只规划，不推送

```bash
python tools/gitlab_release_tag.py plan   --repo /path/to/repo   --mr-title '提示词平台'
```

### 直接创建并推送

```bash
python tools/gitlab_release_tag.py push   --repo /path/to/repo   --mr-title '提示词平台'
```

## 参数说明

- `--repo`：目标仓库目录
- `--ref`：打 tag 的基准 ref，默认 `origin/master`
- `--bump`：升级级别，默认 `patch`
- `--message`：tag 说明，优先级最高
- `--mr-title`：未给 `--message` 时，优先使用它作为说明
- `--no-fetch`：跳过 fetch（默认不建议）
- `--json`：输出机器可读 JSON

## 说明

- 默认不建议在 MR 未合并到 `master` 前直接推 tag。
- 默认不建议直接对当前开发分支打线上 tag。
- 如果项目存在非 `vX.Y.Z` 的 tag 风格，应在项目差异说明中单独记录。


## 恢复触发

这一步默认不是在创建 MR 后立刻执行，而是：

1. 先完成“创建 MR + 通知协作者”；
2. 暂停，等待同事完成合并；
3. 当用户明确说“合并完了，继续”或同等语义时，再恢复执行 tag 升级，以及当前工作分支 fast-forward 到 `origin/master` 的收尾动作。


## tag 说明默认策略

默认不要求用户手动给 tag 文案。

默认策略：

1. 用户显式给了文案 → 直接使用；
2. 用户没给 → 由我根据本次工作内容总结成一句简短话；
3. 若本次工作内容不足以概括 → 再回退到 MR 标题或 merge commit 标题。
