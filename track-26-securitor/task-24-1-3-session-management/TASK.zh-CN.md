# 实现 Secure Session Management

英文标题：Implement Secure Session Management
网页：<https://builddistributedsystem.com/tracks/securitor/tasks/task-24-1-3-session-management>

课程：26. 安全器：认证、授权与加密
任务序号：3
短标题：Session Management
难度：intermediate
子主题：Authentication和Authorization

## 中文导读

本题要求你完成 `实现 Secure Session Management`。

重点关注：`session`、`session ID`、`session fixation`、`session expiry`、`session storage`。

建议先按提示逐步实现：Session ID must be cryptographically random (use uuid or similar)。

协议字段、消息类型、输入输出格式请以本文件中的代码块和测试用例为准。

## 题目说明

Sessions store authentication state 服务端-side. After login, the 服务端 creates a session record keyed by a random ID和sends that ID to the 客户端 as a cookie. On every subsequent 请求, the 客户端 presents the ID和the 服务端 looks up the session.

Implement a 节点 that manages 服务端-side sessions:

```JSON
// Create a new session after successful login
{ "type": "create_session", "msg_id": 1, "user_id": "user123" }
-> { "type": "session_created", "in_reply_to": 1,
    "session_id": "<crypto-random-uuid>",
    "expires_at": <unix-timestamp> }

// Validate a session cookie on incoming 请求
{ "type": "validate_session", "msg_id": 2, "session_id": "abc123" }
-> { "type": "session_valid", "in_reply_to": 2,
    "user_id": "user123", "expires_in": 3600 }

// Regenerate session ID after privilege change (prevents fixation)
{ "type": "regenerate_session", "msg_id": 3, "old_session_id": "abc123" }
-> { "type": "session_regenerated", "in_reply_to": 3,
    "new_session_id": "<new-uuid>" }

// Destroy session on logout
{ "type": "destroy_session", "msg_id": 4, "session_id": "abc123" }
-> { "type": "session_destroyed", "in_reply_to": 4,
    "消息": "Session destroyed" }
```

## 涉及概念

- `session`
- `session ID`
- `session fixation`
- `session expiry`
- `session storage`

## 实现提示

- Session ID must be cryptographically random (use uuid or similar)
- validate_session returns user_id和expires_in from the stored session
- regenerate_session creates a NEW random session_id和copies all session data to it
- destroy_session removes the session from 存储 permanently
- Session expiry: track created_at + ttl; return session_invalid if expired

## 测试用例

### 1. 创建 session

Should create session，包含random session_id和expiry timestamp.

输入：

```json
{"src":"auth","dest":"session","body":{"type":"create_session","msg_id":1,"user_id":"user123"}}
```

期望输出：

```text
{"type": "session_created", "in_reply_to": 1, "session_id": ".*", "expires_at": ".*"}
```

### 2. Validate session

Valid session_id should return user_id和remaining time.

输入：

```json
{"src":"api","dest":"session","body":{"type":"validate_session","msg_id":1,"session_id":"abc123"}}
```

期望输出：

```text
{"type": "session_valid", "in_reply_to": 1, "user_id": "user123", "expires_in": 3600}
```

## 参考资料

- [OWASP Session Management](https://owasp.org/www-community/attacks/Session_fixation)：Session fixation attacks和how to prevent them

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
