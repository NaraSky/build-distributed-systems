# 添加 a Connection Pool，包含Configurable Backlog

英文标题：Add a Connection Pool，包含Configurable Backlog
网页：<https://builddistributedsystem.com/tracks/networker/tasks/task-5-1-2-connection-pool>

课程：17. 网络器：TCP 与协议基础
任务序号：2
短标题：Connection Pool
难度：intermediate
子主题：TCP From Scratch

## 中文导读

本题要求你完成 `添加 a Connection Pool，包含Configurable Backlog`。

重点关注：`connection pool`、`backlog`、`concurrency`、`resource management`。

建议先按提示逐步实现：Track the number of active connections，包含a 计数器。

协议字段、消息类型、输入输出格式请以本文件中的代码块和测试用例为准。

## 题目说明

Extend your TCP 服务端 to accept up to N concurrent connections. When N is exceeded, 队列 new connections in a backlog. If the backlog is also full, reject the connection.

Implement handlers:

```JSON
请求:  {"type": "pool_config", "msg_id": 1, "max_connections": 3, "backlog_size": 5}
响应: {"type": "pool_config_ok", "in_reply_to": 1}

请求:  {"type": "pool_connect", "msg_id": 2, "client_id": "c1"}
响应: {"type": "pool_connect_ok", "in_reply_to": 2, "status": "connected", "active": 1, "queued": 0}

请求:  {"type": "pool_connect", "msg_id": 5, "client_id": "c4"}
响应: {"type": "pool_connect_ok", "in_reply_to": 5, "status": "queued", "active": 3, "queued": 1}

请求:  {"type": "pool_disconnect", "msg_id": 6, "client_id": "c1"}
响应: {"type": "pool_disconnect_ok", "in_reply_to": 6, "promoted": "c4", "active": 3, "queued": 0}
```

## 涉及概念

- `connection pool`
- `backlog`
- `concurrency`
- `resource management`

## 实现提示

- Track the number of active connections，包含a 计数器
- When max connections is reached, either 队列 or reject new connections
- Use a configurable backlog size用于queued connections
- Decrement the 计数器 when a connection is closed
- Consider what happens when the 队列 itself is full

## 测试用例

### 1. Configure pool和connect

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"pool_config","msg_id":2,"max_connections":2,"backlog_size":3}}
{"src":"c1","dest":"n1","body":{"type":"pool_connect","msg_id":3,"client_id":"c1"}}
```

期望输出：

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
{"src": "n1", "dest": "c1", "body": {"type": "pool_config_ok", "in_reply_to": 2, "msg_id": 1}}
{"src": "n1", "dest": "c1", "body": {"type": "pool_connect_ok", "in_reply_to": 3, "status": "connected", "active": 1, "queued": 0, "msg_id": 2}}
```

### 2. Exceeding max connections queues

Third pool_connect_ok should show status: queued, active: 2, queued: 1.

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"pool_config","msg_id":2,"max_connections":2,"backlog_size":3}}
{"src":"c1","dest":"n1","body":{"type":"pool_connect","msg_id":3,"client_id":"c1"}}
{"src":"c1","dest":"n1","body":{"type":"pool_connect","msg_id":4,"client_id":"c2"}}
{"src":"c1","dest":"n1","body":{"type":"pool_connect","msg_id":5,"client_id":"c3"}}
```

期望输出：

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

## 参考资料

- [TCP Backlog和Connection Queuing](https://veithen.io/2014/01/01/how-tcp-backlog-works-in-linux.html)：Deep dive into how TCP backlog works in Linux

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
