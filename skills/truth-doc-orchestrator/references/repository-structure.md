# Repository Structure

## 顶层目录

```text
docs-specs-flo/
  index/
    00-全局导航.md

  shared-truths/
    00-共享真相索引.md
    protocols/
    domain/
    ui-ux/
    engineering/

  modules/
    <模块名>/
      00-模块导航.md

      facts/
        00-事实索引.md
        10-当前能力地图.md
        protocols/
        domain/
        ui-ux/
        references/

      intents/
        active/
          <意图ID>-<意图名>/
            00-意图总览.md
            10-事实基础.md
            20-意图图谱.md
            30-行为语义.md
            40-工程落地.md
            50-验证与回归.md
            attachments/
        settled/
          00-沉淀索引.md
          <意图ID>-<意图名>.md
```

## 目录职责

### `index/`
只做全局导航，不承载正文细节。

### `shared-truths/`
放跨模块复用的稳定真相。优先向上抽离协议、领域、UI/UX 与工程模式。

### `modules/<模块名>/00-模块导航.md`
模块唯一入口。负责：
- 当前真相入口
- 事实区入口
- 活跃意图入口
- 沉淀结果入口
- 共享真相入口
- 建议阅读顺序

### `facts/`
模块事实真相区，不放活跃意图目标，不放未确认设想。

### `intents/active/`
活跃意图区。每个意图一个独立目录，承载本次目标定义、事实基础、图谱、行为、工程、验证。

### `intents/settled/`
已沉淀意图区。每个意图只保留一个单文件沉淀结果，用于追溯和导航，不再承接新范围。

## 放置规则

- 新的事实沉淀优先进入 `facts/`
- 新的活跃工作一律开在 `intents/active/`
- 意图完成后，一律压缩为 `intents/settled/<意图>.md`
- 若内容跨模块稳定复用，优先晋升到 `shared-truths/`
- `00-模块导航.md` 与 `00-全局导航.md` 只做入口，不写大段正文

## attachments/ 用途

`attachments/` 只放补充材料：
- 截图
- 样例请求 / 响应
- 导出图
- 原始材料副本
- 需要就地引用的辅助文件

不要把主文档写进 `attachments/`。
