---
title: edu-content-studio
module: 工作
type: topic
tags: [repo, gitlab, work]
updated_at: 2026-04-22
---

# 仓库身份

- 仓库名：`edu-content-studio`
- 本地目录：`/Users/flowkehurly/Documents/AAA/comp/edu-content-studio`
- remote：`https://git.100tal.com/wangxiao_xueyan_suyang_fe/edu-content-studio.git`
- 仓库页面：`https://git.100tal.com/wangxiao_xueyan_suyang_fe/edu-content-studio`
- 说明：`README.md` 标题为“内容生产平台”，可作为仓库身份线索之一。

# 说明

- 此文件仅保留仓库身份锚点（repo identity），不再存放用户的通用工作交互偏好。
- “当用户说仓库页面时直接输出地址”的偏好已迁移到：`工作/topics/assistant-交互偏好.md`

## 项目级约束：万物生成器修改默认从共享源头入手

在 `edu-content-studio` 仓库里，当用户说“修改万物生成器相关的东西”时，默认不要先把需求理解成只改单个页面入口。

更稳妥的默认理解是：

1. 优先定位共享源头链路；
2. 先改共享配置 / 表单 / 回填逻辑；
3. 预期让所有复用这条链路的页面一起生效；
4. 只有当用户明确说“只改单页 / 只改某个入口”时，才收窄范围。

### 共享源头锚点

万物生成器相关页面有很多复用 `GeneratorFlow` 共享链路。修改视频 / 动图生成相关能力时，优先检查：

- `src/components/GeneratorFlow/config_panel/options.getters.ts`
- `src/components/GeneratorFlow/config_panel/mode.video.ts`
- `src/components/GeneratorFlow/config_panel/mode.video-entry.ts`
- `src/components/GeneratorFlow/PromptPanel.vue`
- `src/components/GeneratorFlow/MediaFlow.vue`

### 已确认会联动的页面样例

- 万物生成器 V2 的动图生成：`src/pages/contentProductionToolsV2/imageCreator/index.vue`
- 万物生成器 V1 进入的 `FeedFlow?mode=video`：`src/pages/contentProductionTools/imageCreator/index.vue`、`src/pages/FeedFlow/index.vue`
- 视频生成任务 video 页：`src/pages/videoGenerator/task/viewVideo/index.vue`
  - 该页通过 `MediaFlow + filter-modes=['video']` 复用同一套视频 selector / 回填逻辑
- legacy 动图页面：`src/pages/contentProductionTools/movingImage/components/ImageOption.vue`
  - 如果共享链路已改，这类本地硬编码表单也要同步补齐，避免新旧页面不一致

### 反例

- 不要默认认为“万物生成器 = 某一个页面入口”
- 不要只看到一个页面就只改那个页面，尤其是视频 / 动图能力
- `video-generator-task/role` 走的是 `filter-modes=['image']`，不应自动归入视频 selector 变更范围
