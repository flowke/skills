# Yach Message APIs (MVP scope)

本文件总结 `yach-message` 当前版本实际使用的官方接口与消息格式。

## 1. 获取 access_token

```http
GET https://yach-oapi.zhiyinlou.com/gettoken?appkey={appkey}&appsecret={appsecret}
```

兼容两种返回结构：
- `{"access_token":"..."}`
- `{"code":200,"obj":{"access_token":"..."}}`

## 2. 点对点机器人消息

官方文档：
- https://yach-open-doc.zhiyinlou.com/server-api/notification/%E6%99%AE%E9%80%9A%E6%B6%88%E6%81%AF.html

接口：

```http
POST /v1/single/message/send?access_token=ACCESS_TOKEN
```

核心参数：
- `to_user_id`：Yach 用户 ID，可用 `|` 分隔多个
- `to_work_code`：员工工号，可用 `|` 分隔多个
- `message`：消息体 JSON
- `message_id`：业务去重 ID（建议传）

说明：
- `to_user_id` 与 `to_work_code` 至少其一非空
- `sscard` 不支持批量发送
- 文档注明该接口单机器人限频为 **60 次/分钟**

## 3. 点对点机器人群消息

官方文档：
- https://yach-open-doc.zhiyinlou.com/server-api/notification/%E6%99%AE%E9%80%9A%E6%B6%88%E6%81%AF.html

接口：

```http
POST /group/robot/message/send?access_token=ACCESS_TOKEN
```

核心参数：
- `group_id`
- `message`
- `message_id`

## 4. 文本消息格式

官方文档：
- https://yach-open-doc.zhiyinlou.com/server-api/notification/%E6%B6%88%E6%81%AF%E7%B1%BB%E5%9E%8B%E4%B8%8E%E6%95%B0%E6%8D%AE%E6%A0%BC%E5%BC%8F.html

示例：

```json
{
  "msgtype": "text",
  "text": {
    "content": "你好，这是一条文本消息"
  },
  "at": {
    "atMobiles": ["150********"],
    "atWorkCodes": ["171765"],
    "isAtAll": false
  }
}
```

说明：
- `content` 必填
- 官方说明：只有 `text`、`markdown` 类型支持 `@`

## 5. Markdown 消息格式

官方文档：
- https://yach-open-doc.zhiyinlou.com/server-api/notification/%E6%B6%88%E6%81%AF%E7%B1%BB%E5%9E%8B%E4%B8%8E%E6%95%B0%E6%8D%AE%E6%A0%BC%E5%BC%8F.html

示例：

```json
{
  "msgtype": "markdown",
  "markdown": {
    "title": "首屏展示标题",
    "image": "https://example.com/example.jpg",
    "text": "# 这是支持 markdown 的文本\n- 列表1"
  },
  "at": {
    "atWorkCodes": ["171765"],
    "isAtAll": false
  }
}
```

说明：
- `title` 建议填写
- `image` 可选
- `text` 为 markdown 正文
- `at` 为可选

## 6. 当前 skill 的实现边界

当前版本只封装：
- `text`
- `markdown`
- 原始 `message JSON` 透传

如需支持：
- `sscard`
- 图片 / 文件 / 视频
- 工作通知 / 应用消息推送

建议直接按官方文档扩展对应脚本。


## 7. 实验版：以员工身份发送

官方文档同样位于：
- https://yach-open-doc.zhiyinlou.com/server-api/notification/%E6%99%AE%E9%80%9A%E6%B6%88%E6%81%AF.html

### 点对点普通消息

```http
POST /single/message/send?access_token=ACCESS_TOKEN
```

核心参数：
- `from_user_id`：发送者 Yach 用户 ID，例如 `yach131763`
- `to_user_id`：接收者 Yach 用户 ID，例如 `yach076429`
- `message`
- `message_id`

### 点对群消息

```http
POST /group/message/send?access_token=ACCESS_TOKEN
```

核心参数：
- `from_user_id`
- `group_id`
- `message`
- `message_id`

说明：
- 这两个接口从参数语义上属于“以员工身份发送”而非“机器人身份发送”
- 当前 skill 只把它们作为 **实验版链路** 封装
- 是否真正可用，取决于当前 `appkey/appsecret` 对应应用是否具备该权限
- 建议始终先 `--dry-run`，再做小范围真实验证
