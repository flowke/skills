---
name: yapi-interface-docs
description: 获取 YAPI 接口文档信息的技能。适用于用户提供 YAPI 页面链接或接口 ID，希望读取接口详情、输出结构化摘要、查看原始 JSON，或排查由于 cookie / 权限 / 配置导致的 YAPI 文档请求失败。也适用于用户直接提供 cookie，希望将其写入本地配置后再查询。
---

# yapi-interface-docs

这个 skill 用于**读取 YAPI 接口文档**，并优先给出**结构化摘要**，必要时再输出原始 JSON。

优先处理以下场景：
- 用户给出 YAPI 页面链接，希望获取接口文档信息
- 用户给出接口 ID，希望查看该接口详情
- 用户怀疑请求失败与 cookie / 权限 / 配置有关，希望先做排查
- 用户直接给出 cookie，希望写入本地配置后再重新查询

默认不负责：
- 通用 Swagger / Apifox / Postman 文档读取
- 自动从浏览器抓取 cookie
- 把整段 curl 文本作为主要输入格式（v1 暂不支持）

## 配置

优先使用工作区配置，缺失时回退到全局配置：
1. `<当前工作区>/.yapi-config.json`
2. `~/.yapi-config.json`

推荐配置：

```json
{
  "base_url": "https://yapi.xesv5.com",
  "cookie": "xesId=...; _yapi_token=...; ...",
  "headers": {
    "accept": "application/json, text/plain, */*",
    "referer": "https://yapi.xesv5.com/"
  },
  "timeout_sec": 20
}
```

最小必需字段：
- `base_url`
- `cookie`

建议先检查当前生效配置：

```bash
python3 scripts/resolve_yapi_config.py --summary
python3 scripts/resolve_yapi_config.py --path
python3 scripts/resolve_yapi_config.py --validate
```

如果用户直接提供 cookie，可写入全局配置：

```bash
python3 scripts/save_yapi_config.py --cookie 'xesId=...; _yapi_token=...'
```

也可以明确写入当前工作区配置：

```bash
python3 scripts/save_yapi_config.py --workspace --cookie 'xesId=...; _yapi_token=...'
```

## 获取接口文档

主入口脚本：`scripts/get_interface_doc.py`

### 1) 通过接口 ID 获取

```bash
python3 scripts/get_interface_doc.py --id 184595
```

### 2) 通过 YAPI 页面链接获取

```bash
python3 scripts/get_interface_doc.py \
  --url 'https://yapi.xesv5.com/project/3932/interface/api/184595'
```

### 3) 输出原始 JSON

```bash
python3 scripts/get_interface_doc.py --id 184595 --raw
```

### 4) 输出机器可读摘要 JSON

```bash
python3 scripts/get_interface_doc.py --id 184595 --json
```

## 默认工作流

1. 先运行 `resolve_yapi_config.py --summary` 确认当前使用哪份配置
2. 再运行 `get_interface_doc.py --id ...` 或 `--url ...`
3. 如果失败，优先判断：
   - 是否没有配置文件
   - 是否缺少 cookie
   - 是否 cookie 已失效 / 权限不足
   - 是否接口 ID 不存在
4. 如果已经判断为鉴权 / cookie 问题：
   - 直接帮用户打开登录页：`https://yapi.xesv5.com/`
   - 等用户登录完成后，再提示用户把最新 cookie 发给你
   - 收到最新 cookie 后，用 `scripts/save_yapi_config.py` 更新配置并重试

## 结果解释

默认摘要会优先展示：
- 接口标题
- 请求路径
- 请求方法
- 项目 / 分类（若响应中存在）
- path/query/header/body 参数
- 返回定义
- 接口说明 / markdown
- 接口 ID

如果你只是想排查问题，优先看报错中是否出现：
- `no .yapi-config.json found`
- `missing required keys`
- `permission`
- `login`
- `cookie`
- `token`

一旦确认是鉴权问题，本 skill 的默认恢复动作不是反复重试，而是：
1. 直接打开 `https://yapi.xesv5.com/`
2. 等用户手动登录
3. 请用户把新的 cookie 发给你
4. 立即更新 `~/.yapi-config.json` 或工作区配置后再查询

### scripts/
- `scripts/resolve_yapi_config.py`：解析当前生效配置并脱敏展示
- `scripts/save_yapi_config.py`：写入或更新 `.yapi-config.json`
- `scripts/get_interface_doc.py`：根据 ID / URL 获取接口文档
- `scripts/yapi_interface_lib.py`：公共逻辑库
