# 实现 Application-Level TCP Keep-Alive

英文标题：Implement Application-Level TCP Keep-Alive
网页：<https://builddistributedsystem.com/tracks/networker/tasks/task-5-1-4-keepalive>

课程：17. 网络器：TCP 与协议基础
任务序号：4
短标题：TCP Keep-Alive
难度：intermediate
子主题：TCP From Scratch

## 中文导读

本题要求你完成 `实现 Application-Level TCP Keep-Alive`。

重点关注：`keep-alive`、`heartbeat`、`connection health`、`idle detection`。

建议先按提示逐步实现：Send periodic ping 消息 to detect silent 客户端 failures。

协议字段、消息类型、输入输出格式请以本文件中的代码块和测试用例为准。

## 题目说明

Implement application-level TCP keep-alive detection. If a 客户端 goes silent用于more than 30 seconds, detect it和close the connection. Use periodic ping 消息 instead of OS-level keep-alive.

Implement handlers:

```JSON
请求:  {"type": "ka_register", "msg_id": 1, "client_id": "c1", "timeout_ms": 30000, "ping_interval_ms": 10000}
响应: {"type": "ka_register_ok", "in_reply_to": 1}

请求:  {"type": "ka_heartbeat", "msg_id": 2, "client_id": "c1"}
响应: {"type": "ka_heartbeat_ok", "in_reply_to": 2, "last_seen_ms_ago": 0}

请求:  {"type": "ka_check", "msg_id": 3, "current_time_ms": 45000}
响应: {"type": "ka_check_ok", "in_reply_to": 3, "expired": ["c1"], "active": ["c2"]}

请求:  {"type": "ka_status", "msg_id": 4}
响应: {"type": "ka_status_ok", "in_reply_to": 4, "connections": [
    {"client_id": "c2", "last_seen_ms_ago": 5000, "status": "active"}
]}
```

## 涉及概念

- `keep-alive`
- `heartbeat`
- `connection health`
- `idle detection`

## 实现提示

- Send periodic ping 消息 to detect silent 客户端 failures
- Track the last activity timestamp用于each connection
- If no activity用于> 30s, send a ping. If no pong within 5s, close the connection
- Do not rely on OS-level keep-alive; implement at the application layer
- Maintain a connection state table，包含last_seen timestamps

## 测试用例

### 1. Register a client用于keep-alive

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"ka_register","msg_id":2,"client_id":"c1","timeout_ms":30000,"ping_interval_ms":10000}}
```

期望输出：

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
{"src": "n1", "dest": "c1", "body": {"type": "ka_register_ok", "in_reply_to": 2, "msg_id": 1}}
```

### 2. Heartbeat resets last_seen

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"ka_register","msg_id":2,"client_id":"c1","timeout_ms":30000,"ping_interval_ms":10000}}
{"src":"c1","dest":"n1","body":{"type":"ka_heartbeat","msg_id":3,"client_id":"c1"}}
```

期望输出：

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
{"src": "n1", "dest": "c1", "body": {"type": "ka_register_ok", "in_reply_to": 2, "msg_id": 1}}
{"src": "n1", "dest": "c1", "body": {"type": "ka_heartbeat_ok", "in_reply_to": 3, "last_seen_ms_ago": 0, "msg_id": 2}}
```

## 参考资料

- [TCP Keep-Alive in Detail](https://tldp.org/HOWTO/TCP-Keepalive-HOWTO/)：Understanding TCP keep-alive at both OS和application levels

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
