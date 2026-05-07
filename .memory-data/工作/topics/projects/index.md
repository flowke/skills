---
title: 项目信息索引
module: 工作
type: topic
tags: [项目, 索引, 仓库, 发布入口]
updated_at: 2026-05-07
---

# 项目信息索引

统一记录各项目的身份信息、仓库绑定、发布入口，以及**相对通用发布流程的项目差异**。

发布流程默认遵循：`sops/项目默认工作流程.md`。

发线上最后一步默认输出该项目的线上发布页。

当前跨项目默认协作者 / 对接人为：**杜涔涔**（见 `topics/同事/杜涔涔.md`）。

对 `git.100tal.com` 上的大多数项目，默认规则还包括：

- 发测试目标分支：`dev`
- 发灰 / 发灰度目标分支：`gray`
- 发线上时：第二步后默认先停下来，待用户说“合并完了，继续”后，再基于最新 tag 按 patch 升级
- tag 格式默认：`vX.Y.Z`
- tag 默认打在 `origin/master` 的最新 merge commit 上
- tag 说明默认：优先用户给；否则由我根据本次工作内容总结成一句简短话

除非某个项目另有说明。

如某个项目没有稳定差异，就不要再为它单独建一份发布流程 SOP。

## 超级教研

- 项目名：**超级教研**
- 仓库名称：`ai-ppt`
- 仓库地址：`https://git.100tal.com/wangxiao_xueyan_suyang_fe/ai-ppt`
- 仓库身份锚点：`topics/repos/ai-ppt.md`
- 测试发布页：[cloud-test 发布页](https://cloud-test.tal.com/k8s-fe/appManage/appManageCenter/appDetail/imageManage?id=2826932)
- 未来课件子应用测试发布页：[cloud-test 发布页](https://cloud-test.tal.com/k8s-fe/appManage/appManageCenter/appDetail/imageManage?id=2827456)
- 未来课件子应用灰度发布页：[cloud 灰度发布页](https://cloud.tal.com/k8s-fe/appManage/appManageCenter/appDetail/imageManage?id=35125)
- 未来课件子应用子应用发布页：[cloud 发布页](https://cloud.tal.com/k8s-fe/appManage/appManageCenter/appDetail/imageManage?id=35121)
- 灰度发布页：[cloud 灰度发布页](https://cloud.tal.com/k8s-fe/appManage/appManageCenter/appDetail/imageManage?id=34527)
- 线上发布页：[cloud 线上发布页](https://cloud.tal.com/k8s-fe/appManage/appManageCenter/releaseDetail?id=33556&cd_id=721588)
- 项目差异：当前未记录

## 内容生产平台

- 项目名：**内容生产平台**
- 仓库名称：`edu-content-studio`
- 仓库地址：`https://git.100tal.com/wangxiao_xueyan_suyang_fe/edu-content-studio.git`
- 仓库身份锚点：`topics/repos/edu-content-studio.md`
- 测试发布页：[cloud-test 发布页](https://cloud-test.tal.com/k8s-fe/appManage/appManageCenter/appDetail/imageManage?id=1011606)
- 灰度发布页：[cloud 灰度发布页](https://cloud.tal.com/k8s-fe/appManage/appManageCenter/appDetail/imageManage?id=26435)
- 线上发布页：[cloud 线上发布页](https://cloud.tal.com/k8s-fe/appManage/appManageCenter/appDetail/imageManage?id=26440)
- 项目差异：万物生成器相关修改默认优先从共享源头链路入手，见 `topics/repos/edu-content-studio.md`
