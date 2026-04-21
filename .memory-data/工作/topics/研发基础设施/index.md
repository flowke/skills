# 研发基础设施

- [GitLab 仓库地址反推规则](./GitLab 仓库地址反推规则.md)
- `git.100tal.com` 仓库默认分支约定：测试走 `dev`，灰度走 `gray`；除非项目文档另有说明。
- `git.100tal.com` 线上 tag 约定：MR 合并到 `master` 后，基于最新 tag 默认按 patch 升级，tag 格式为 `vX.Y.Z`，默认打在 `origin/master` 的最新 merge commit 上；tag 说明优先用户给，否则从 MR 标题提取。
