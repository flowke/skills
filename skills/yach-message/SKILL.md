---
name: yach-message
description: 发送知音楼消息的技能。适用于给个人或群发送知音楼机器人消息、markdown 消息、文本消息、@提及，以及基于原始 message JSON 调用 Yach 消息通知接口。关键词：知音楼发消息、Yach 发消息、数字伙伴发消息、群消息、私聊消息、markdown 消息、机器人消息、@某人、group_id、to_work_code。
---

# yach-message

这个 skill 用于**主动发送知音楼消息**，而不是读取知音楼文档。

优先处理以下场景：
- 给某个员工发送知音楼机器人私聊消息
- 给某个群发送知音楼机器人群消息
- 发送 `text` / `markdown` 消息
- 在消息中 `@工号` / `@手机号` / `@所有人`
- 用户给出原始 message JSON，希望直接透传到消息接口

默认不负责：
- OpenClaw 网关接入与长连接对话
- 文档导入导出
- 工作通知 / 应用消息推送（可后续扩展）

## 配置

优先使用工作区配置，缺失时回退到全局配置：
1. `<当前工作区>/.yach-config.json`
2. `~/.yach-config.json`

推荐配置：

```json
{
  "appkey": "YOUR_APPKEY",
  "appsecret": "YOUR_APPSECRET",
  "agent_id": "YOUR_ROBOT_ID",
  "app_id": "YOUR_APP_ID",
  "base_url": "https://yach-oapi.zhiyinlou.com"
}
```

其中本 skill 的最小必需字段是：
- `appkey`
- `appsecret`
- `base_url`

`agent_id` / `app_id` 当前版本保留为可选字段，供后续扩展使用。

始终先解析实际生效配置：

```bash
python3 scripts/resolve_yach_config.py --summary
python3 scripts/resolve_yach_config.py --path
python3 scripts/get_access_token.py --masked
```

## 发送路径

### 1) 给个人发机器人私聊消息

使用：`scripts/send_single_message.py`

优先传：
- `--to-work-code`：按工号发送
- `--to-user-id`：按 yach 用户 ID 发送

至少二选一，均支持多个值，以半角竖线 `|` 分隔。

示例：

```bash
python3 scripts/send_single_message.py \
  --to-work-code '076429' \
  --msgtype text \
  --content '你好，这是一条测试消息' \
  --dry-run
```

```bash
python3 scripts/send_single_message.py \
  --to-work-code '076429|091805' \
  --msgtype markdown \
  --title '发布提醒' \
  --content '# 发布完成\n- 环境：prod\n- 时间：17:00'
```

### 2) 给群发机器人群消息

使用：`scripts/send_group_message.py`

示例：

```bash
python3 scripts/send_group_message.py \
  --group-id '2740956956' \
  --msgtype markdown \
  --title '今晚发布' \
  --content '# 今晚发布\n请相关同学关注' \
  --dry-run
```

### 3) 实验版：以本人 / 指定员工身份发送

使用：
- `scripts/send_as_user_single_message.py`
- `scripts/send_as_user_group_message.py`

这两个脚本走的是“普通消息”接口，而不是“机器人消息”接口。

**前提条件**：
- 你必须知道发送者的 `from_user_id`（例如 `yach131763`）
- 单聊时还必须知道接收者的 `to_user_id`
- 当前应用必须具备以员工身份发送的权限，否则即使参数正确也会被接口拒绝

示例（单聊，先 dry-run）：

```bash
python3 scripts/send_as_user_single_message.py \
  --from-user-id 'yach131763' \
  --to-user-id 'yach076429' \
  --msgtype text \
  --content '你好，我本人来打个招呼' \
  --dry-run
```

示例（群聊，先 dry-run）：

```bash
python3 scripts/send_as_user_group_message.py \
  --from-user-id 'yach131763' \
  --group-id '2740956956' \
  --msgtype markdown \
  --title '测试消息' \
  --content '# 我本人发一条测试消息' \
  --dry-run
```

### 3) 直接发送原始 message JSON

当用户明确给出了完整消息结构，或需要高级消息类型时，优先直接透传：

```bash
python3 scripts/send_single_message.py \
  --to-work-code '076429' \
  --message-file /absolute/path/to/message.json
```

或：

```bash
python3 scripts/send_group_message.py \
  --group-id '2740956956' \
  --message-json '{"msgtype":"text","text":{"content":"hello"}}'
```

## 文本 / markdown 规则

### text
- `content` 必填
- 支持 `at.atWorkCodes` / `at.atMobiles` / `at.isAtAll`
- 内容建议不超过 5000 字符

### markdown
- `title` 建议提供；缺失时脚本会自动从正文首行推断
- `text` 为 markdown 主体
- 可选 `image`
- 支持同样的 `at` 结构

## 推荐执行策略

1. 先 `--dry-run` 预览要发送的 endpoint 与 body
2. 确认接收人 / 群 ID 正确后再实际发送
3. 默认自动生成 `message_id`，用于业务去重
4. 若用户提到“工号”，优先用 `--to-work-code`
5. 若用户提到“群号 / group_id”，用群消息脚本

## 安全要求

- 不要把真实 `appkey` / `appsecret` / `access_token` 写入 skill 仓库
- 不要在回复里回显完整 token
- 若仅需展示请求内容，优先使用 `--dry-run`

## 参考资料

需要确认接口与消息结构时，读取：
- `references/message-apis.md`
