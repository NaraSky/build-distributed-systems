# 实现 Graceful Shutdown，包含In-Flight Drain

英文标题：Implement Graceful Shutdown，包含In-Flight Drain
网页：<https://builddistributedsystem.com/tracks/networker/tasks/task-5-1-3-graceful-shutdown>

课程：17. 网络器：TCP 与协议基础
任务序号：3
短标题：Graceful Shutdown
难度：intermediate
子主题：TCP From Scratch

## 中文导读

本题要求你完成 `实现 Graceful Shutdown，包含In-Flight Drain`。

重点关注：`graceful shutdown`、`drain`、`in-flight requests`、`connection lifecycle`。

建议先按提示逐步实现：On shutdown signal, stop accepting new connections immediately。

协议字段、消息类型、输入输出格式请以本文件中的代码块和测试用例为准。

## 题目说明

Implement graceful shutdown: when the 服务端 receives a shutdown signal, it should drain all in-flight requests before closing sockets. New connections are rejected during draining.

Implement handlers:

```JSON
请求:  {"type": "tcp_request", "msg_id": 1, "data": "process_this", "latency_ms": 500}
响应: {"type": "tcp_request_ok", "in_reply_to": 1, "result": "processed", "duration_ms": 500}

请求:  {"type": "tcp_shutdown", "msg_id": 2, "drain_timeout_ms": 5000}
响应: {"type": "tcp_shutdown_ok", "in_reply_to": 2, "status": "draining", "in_flight": 2}

请求:  {"type": "tcp_request", "msg_id": 3, "data": "new_request", "latency_ms": 100}
响应: {"type": "tcp_request_error", "in_reply_to": 3, "error": "server_shutting_down"}

请求:  {"type": "tcp_drain_status", "msg_id": 4}
响应: {"type": "tcp_drain_status_ok", "in_reply_to": 4, "status": "drained", "remaining": 0, "took_ms": 500}
```

## 涉及概念

- `graceful shutdown`
- `drain`
- `in-flight requests`
- `connection lifecycle`

## 实现提示

- On shutdown signal, stop accepting new connections immediately
- Wait用于all in-flight requests to complete before closing sockets
- Track the number of in-flight requests，包含a 计数器
- Set a maximum drain 超时: force-close after N seconds
- Test by sending requests和initiating shutdown mid-flight

## 测试用例

### 1. Normal request processing

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"tcp_request","msg_id":2,"data":"hello","latency_ms":0}}
```

期望输出：

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
{"src": "n1", "dest": "c1", "body": {"type": "tcp_request_ok", "in_reply_to": 2, "result": "processed", "duration_ms": 0, "msg_id": 1}}
```

### 2. Shutdown starts drain

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"tcp_shutdown","msg_id":2,"drain_timeout_ms":5000}}
```

期望输出：

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
{"src": "n1", "dest": "c1", "body": {"type": "tcp_shutdown_ok", "in_reply_to": 2, "status": "draining", "in_flight": 0, "msg_id": 1}}
```

## 参考资料

- [Graceful Shutdown in Go](https://pkg.go.dev/net/http#Server.Shutdown)：How Go standard library implements graceful HTTP 服务端 shutdown

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
