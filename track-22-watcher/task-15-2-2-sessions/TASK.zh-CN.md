# 实现 Client Session Management

英文标题：Implement Client Session Management
网页：<https://builddistributedsystem.com/tracks/watcher/tasks/task-15-2-2-sessions>

课程：22. 观察者：ZooKeeper/etcd 模型
任务序号：7
短标题：Sessions
难度：intermediate
子主题：Watches和Sessions

## 中文导读

本题要求你完成 `实现 Client Session Management`。

重点关注：`session`、`heartbeat`、`session timeout`、`session expiry`、`reconnection`。

建议先按提示逐步实现：Each 客户端 is assigned a session ID on connection。

协议字段、消息类型、输入输出格式请以本文件中的代码块和测试用例为准。

## 题目说明

Every ZooKeeper 客户端 operates within a session. The session tracks the 客户端's liveness和is the basis用于ephemeral 节点 lifetime和watch delivery.

**Session lifecycle**:
1. 客户端 connects和receives a unique session ID
2. 客户端 sends heartbeats (pings) every `tickTime` (default 2 seconds)
3. If the 服务端 misses heartbeats用于`sessionTimeout` (default 10 seconds), the session expires
4. On expiry: ephemeral 节点 created by this session are deleted, watches are removed
5. If the 客户端 reconnects before 超时, the session is preserved，包含all its state

```JSON
请求:  {"type": "session_create", "msg_id": 1, "timeout_ms": 10000}
响应: {"type": "session_create_ok", "in_reply_to": 1, "session_id": "s-001", "timeout_ms": 10000}

请求:  {"type": "session_heartbeat", "msg_id": 2, "session_id": "s-001"}
响应: {"type": "session_heartbeat_ok", "in_reply_to": 2, "session_id": "s-001", "remaining_ms": 10000}
```

## 涉及概念

- `session`
- `heartbeat`
- `session timeout`
- `session expiry`
- `reconnection`

## 实现提示

- Each 客户端 is assigned a session ID on connection
- 客户端 sends heartbeats every tick_time (2 seconds default)
- If the 服务端 misses heartbeats用于session_timeout (10s default), the session expires
- On session expiry: all ephemeral 节点 are deleted, all watches are removed
- Clients can reconnect within the 超时 window without losing their session

## 测试用例

### 1. 创建 session returns session ID

session_create_ok should include a unique session_id和the timeout_ms.

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"session_create","msg_id":2,"timeout_ms":10000}}
```

期望输出：

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

### 2. Heartbeat extends session

session_heartbeat_ok should show remaining_ms > 0.

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"session_create","msg_id":2,"timeout_ms":10000}}
{"src":"c1","dest":"n1","body":{"type":"session_heartbeat","msg_id":3,"session_id":"s-001"}}
```

期望输出：

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

## 参考资料

- [ZooKeeper Sessions](https://zookeeper.apache.org/doc/current/zookeeperProgrammers.html#ch_zkSessions)：ZooKeeper documentation on session management和heartbeats

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
