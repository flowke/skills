---
title: GitLab 仓库地址反推规则
module: 工作
type: topic
tags: [GitLab, 仓库, remote, origin, 100tal]
updated_at: 2026-04-21
---

# GitLab 仓库地址反推规则

## 适用背景

公司内部仓库普遍使用 GitLab。当本地仓库的 `origin` 指向 `git.100tal.com`（或同类公司 GitLab 域名）时，可以把它视为 GitLab 仓库来源，并据此反推出仓库页面地址与后续操作链接。

## 反推规则

若执行：

```bash
git remote get-url origin
```

得到类似：

```text
https://git.100tal.com/<group>/<project>.git
```

则可反推出：

- 仓库页面地址：`https://git.100tal.com/<group>/<project>`
- MR 新建页：`https://git.100tal.com/<group>/<project>/merge_requests/new?...`
- Tag 页面：`https://git.100tal.com/<group>/<project>/tags` 或 `/tags/new?...`

## 使用建议

1. 当用户要求“给我 MR 链接”或“给我 tag 链接”时，优先先读取 `origin`。
2. 只要远程地址明显属于公司 GitLab（如 `git.100tal.com`），就可以按 GitLab 规则拼接页面 URL，而不是依赖当前工作区上下文描述。
3. 若远程地址以 `.git` 结尾，生成页面链接时应去掉 `.git`。
4. 如果同时需要 source branch / target branch，再结合当前分支名与目标分支名拼接完整链接。

## 说明

这是一条公司级经验，可跨多个仓库复用，不应只记录在单个项目 SOP 中。
