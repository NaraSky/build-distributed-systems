# 实现安全会话管理

英文标题：Implement Secure Session Management
网页：<https://builddistributedsystem.com/tracks/securitor/tasks/task-24-1-3-session-management>

课程：26. 安全器
任务序号：3
短标题：会话管理
难度：进阶
子主题：认证与授权

## 中文导读

这道题要求你实现服务端会话管理，包括会话的创建、验证、重新生成和销毁。会话是传统 Web 应用中最常用的身份状态保持方式：用户登录后服务端创建一条记录，将标识通过 Cookie 发给客户端，后续请求凭此标识证明身份。理解会话管理的安全要点，是 Web 安全的基础。

## 题目说明

会话（Session）在服务端存储认证状态。用户登录成功后，服务端创建一条会话记录，以随机生成的标识作为键，并通过 Cookie 将该标识发送给客户端。此后每次请求，客户端都会携带这个标识，服务端据此查找对应的会话信息。

会话管理就像餐厅的取餐号码牌：你点完餐（登录）后，餐厅给你一个号码牌（会话标识），之后你凭号码牌取餐（访问资源）。会话固定攻击（Session Fixation）是指攻击者先获取一个会话标识，然后诱导用户使用这个标识登录，这样攻击者就能冒充用户。防范方法很简单：用户登录或权限变更后，立即重新生成一个新的会话标识。

你需要实现一个节点来管理服务端会话：

```json
// 登录成功后创建新会话
{ "type": "create_session", "msg_id": 1, "user_id": "user123" }
-> { "type": "session_created", "in_reply_to": 1,
    "session_id": "<crypto-random-uuid>",
    "expires_at": <unix-timestamp> }

// 验证传入请求中的会话 Cookie
{ "type": "validate_session", "msg_id": 2, "session_id": "abc123" }
-> { "type": "session_valid", "in_reply_to": 2,
    "user_id": "user123", "expires_in": 3600 }

// 权限变更后重新生成会话标识（防范会话固定攻击）
{ "type": "regenerate_session", "msg_id": 3, "old_session_id": "abc123" }
-> { "type": "session_regenerated", "in_reply_to": 3,
    "new_session_id": "<new-uuid>" }

// 登出时销毁会话
{ "type": "destroy_session", "msg_id": 4, "session_id": "abc123" }
-> { "type": "session_destroyed", "in_reply_to": 4,
    "message": "Session destroyed" }
```

## 涉及概念

- session
- session ID
- session fixation
- session expiry
- session storage

## 实现提示

- 会话标识必须是加密安全的随机值（使用 UUID 或类似方案）
- validate_session 从存储的会话中返回 user_id 和 expires_in
- regenerate_session 创建一个新的随机会话标识，并将原有会话数据复制过去
- destroy_session 从存储中永久删除该会话
- 会话过期：记录 created_at + ttl；如果已过期则返回 session_invalid

## 测试用例

### 1. 创建会话

应当创建会话，包含随机的会话标识和过期时间戳。

输入：

```json
{"src":"auth","dest":"session","body":{"type":"create_session","msg_id":1,"user_id":"user123"}}
```

期望输出：

```text
{"type": "session_created", "in_reply_to": 1, "session_id": ".*", "expires_at": ".*"}
```

### 2. 验证会话

有效的会话标识应当返回用户标识和剩余有效时间。

输入：

```json
{"src":"api","dest":"session","body":{"type":"validate_session","msg_id":1,"session_id":"abc123"}}
```

期望输出：

```text
{"type": "session_valid", "in_reply_to": 1, "user_id": "user123", "expires_in": 3600}
```

## 参考资料

- [OWASP Session Management](https://owasp.org/www-community/attacks/Session_fixation)：介绍会话固定攻击及其防范方法

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
