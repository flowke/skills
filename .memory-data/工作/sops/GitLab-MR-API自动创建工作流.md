---
title: GitLab-MR-API自动创建工作流
module: 工作
type: sop
tags: [GitLab, MR, API, 自动化, 工作流]
updated_at: 2026-04-21
related_tools:
  - tools/gitlab_create_mr.py
  - tools/create_mr_and_notify.py
---

# GitLab-MR-API自动创建工作流

## 适用范围

适用于需要**不打开浏览器**、直接通过 GitLab API 创建 Merge Request 的工作场景。

该工作流面向“创建 MR”这一动作本身，不依赖 snippet，也不要求安装 `glab`。它是**跨项目可复用**的通用能力，不只服务于某一个项目。

## 默认实现

- 通过 `tools/gitlab_create_mr.py` 调 GitLab `merge_requests` API 创建 MR。
- 认证信息优先读取用户级配置文件：`~/.gitlab-mr-config.json`。
- 如果配置文件中没有 token，再回退读取环境变量 `GITLAB_TOKEN` / `PRIVATE_TOKEN`。
- 默认 target branch 为配置中的 `default_target_branch`；若未配置，则默认 `master`。
- 默认创建正式 MR，不默认加 `Draft:` 前缀；只有显式传入 `--draft` 时才创建 Draft MR。
- 这是跨项目默认行为。
- source branch 默认读取目标仓库当前分支。
- title 默认读取目标仓库最近一条 commit message；也可显式传入。

## 前置条件

1. 已有可用的 GitLab Personal Access Token。
2. token 已写入本机用户级配置文件或环境变量。
3. 目标仓库的 source branch 已 push 到远端。
4. 当前目录是目标 git 仓库，或通过 `--repo` 显式指定仓库目录。

## 配置文件

这是**机器级**配置，不属于共享记忆的一部分；之所以在 SOP 中提到，是为了说明默认读取规则。

默认路径：

```text
~/.gitlab-mr-config.json
```

如果需要覆盖默认位置，可通过环境变量 `GITLAB_MR_CONFIG` 指定。

建议字段：

```json
{
  "gitlab_token": "<PAT>",
  "gitlab_host": "git.100tal.com",
  "default_target_branch": "master",
  "open_after_create": false
}
```

## 推荐命令

### 在当前仓库里创建 MR

```bash
python tools/gitlab_create_mr.py create --title "feat: xxx"
```

### 指定仓库目录创建 MR

```bash
python tools/gitlab_create_mr.py create \
  --repo /path/to/repo \
  --title "feat: xxx"
```

## 跨项目调用方式

当这套能力用于其他项目时，默认不是重新造一份项目脚本，而是：

1. 继续复用通用工具 `tools/gitlab_create_mr.py`；
2. 通过 `--repo /path/to/repo` 指向目标仓库；
3. 由工具自行读取该仓库的 `origin`、当前分支和最近一条 commit message；
4. 再由项目文档决定“第二步默认协作者 / 对接人”是谁。

也就是说：

- 第一步“创建正式 MR”是通用能力；
- 第二步“把 MR 链接发给谁”是项目绑定信息。


### 指定目标分支

```bash
python tools/gitlab_create_mr.py create \
  --repo /path/to/repo \
  --title "feat: xxx" \
  --target master
```

### 从文件读取描述

```bash
python tools/gitlab_create_mr.py create \
  --repo /path/to/repo \
  --title "feat: xxx" \
  --description-file /path/to/mr-description.md
```

## 默认失败处理

### 远端没有 source branch

脚本会直接报错，并提示先执行：

```bash
git push -u origin <source_branch>
```

### source / target 相同

脚本会阻断，避免创建无意义 MR。

### token 不存在或无效

脚本会直接报错，由用户修正本机配置文件或环境变量。

## 说明

- 这是“创建 MR”能力的通用 SOP。
- 项目级发布 SOP 可以引用本文件，而不需要把 API 细节重复写进每个项目文档。
- 若未来需要增加 reviewer、assignee、draft 策略或 description 模板，可继续扩展对应工具，而不改变本 SOP 的总体定位。


## 共享工具定位

- 项目内 wrapper 可以通过环境变量 `CODEX_MEMORY_ROOT` 覆盖 memory root。
- 未设置时，默认按 `~/Documents/AAA/skills/.memory-data` 推导共享工具位置。


## 两步串联工具

当需要把“创建 MR + 通知默认协作者”串成一个动作时，使用：`tools/create_mr_and_notify.py`。

默认行为：

1. 创建正式 MR；
2. 给杜涔涔（工号 `113166`）发送一条 `text` 消息；
3. 默认模板：`涔涔, 帮合并下: {mr_url}, 盼回复`。

如果用户临时要求发给其他人，可以通过 `--notify-work-code` 覆盖接收人工号；如需指定称呼，可额外传 `--notify-name`。
