# Layout and Templates

## Canonical directory layout

```text
/Users/flowkehurly/.memory-data/
  general/
    index.md
    logs/
      2026/
        2026-04.md
    topics/
    sops/
    tools/
  <module>/
    index.md
    logs/
    topics/
    sops/
    tools/
```

## Index template

```md
# 模块索引：<module>

## 模块说明
记录属于“<module>”模块的长期记忆、日志、主题、SOP 和工具。

## Topics
- 暂无

## SOPs
- 暂无

## Tools
- 暂无

## Recent Updates
- 暂无
```

## Topic template

```md
---
title: <title>
module: <module>
type: topic
tags: [tag1, tag2]
updated_at: YYYY-MM-DD
---

# <title>

## 摘要
<1-3 句摘要>

## 细节
- ...
```

## SOP template

```md
---
title: <title>
module: <module>
type: sop
tags: [tag1, tag2]
updated_at: YYYY-MM-DD
related_tools:
  - tools/<tool-name>.py
---

# <title>

## 适用场景
<何时使用>

## 步骤
1. ...
2. ...
3. ...
```

## Log entry template

```md
# YYYY-MM

## YYYY-MM-DD HH:MM
- Record: <fact or event>
- Tags: tag1, tag2
```
