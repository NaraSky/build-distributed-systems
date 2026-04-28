# 实现优雅关闭与请求排空

英文标题：Implement Graceful Shutdown with In-Flight Drain
网页：<https://builddistributedsystem.com/tracks/networker/tasks/task-5-1-3-graceful-shutdown>

课程：17. 网络器：TCP 与协议基础
任务序号：3
短标题：优雅关闭
难度：进阶
子主题：从零实现 TCP

## 中文导读

这道题让你实现服务器的优雅关闭（Graceful Shutdown）。想象一家餐厅打烊时，不会把正在用餐的客人赶走，而是停止接待新客人，等现有客人吃完再关门。服务器的优雅关闭也是同样的道理：收到关闭信号后，拒绝新请求，等待正在处理中的请求全部完成（排空），然后再安全地关闭所有连接。这在生产环境中非常重要，可以避免数据丢失和请求中断。

## 题目说明

实现优雅关闭功能：当服务器收到关闭信号时，应先排空所有正在处理中的请求（In-flight Requests），然后再关闭套接字。在排空期间，新的连接请求应被拒绝。

实现以下消息处理器：

```json
Request:  {"type": "tcp_request", "msg_id": 1, "data": "process_this", "latency_ms": 500}
Response: {"type": "tcp_request_ok", "in_reply_to": 1, "result": "processed", "duration_ms": 500}

Request:  {"type": "tcp_shutdown", "msg_id": 2, "drain_timeout_ms": 5000}
Response: {"type": "tcp_shutdown_ok", "in_reply_to": 2, "status": "draining", "in_flight": 2}

Request:  {"type": "tcp_request", "msg_id": 3, "data": "new_request", "latency_ms": 100}
Response: {"type": "tcp_request_error", "in_reply_to": 3, "error": "server_shutting_down"}

Request:  {"type": "tcp_drain_status", "msg_id": 4}
Response: {"type": "tcp_drain_status_ok", "in_reply_to": 4, "status": "drained", "remaining": 0, "took_ms": 500}
```

## 涉及概念

- `graceful shutdown`
- `drain`
- `in-flight requests`
- `connection lifecycle`

## 实现提示

- 收到关闭信号后，立即停止接受新连接
- 等待所有正在处理中的请求完成后再关闭套接字
- 使用计数器跟踪正在处理中的请求数量
- 设置最大排空超时时间：如果超时仍有未完成的请求，强制关闭
- 可以通过发送请求后立即触发关闭来测试排空逻辑

## 测试用例

### 1. 正常的请求处理

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

### 2. 关闭后开始排空

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

- [Graceful Shutdown in Go](https://pkg.go.dev/net/http#Server.Shutdown)：Go 标准库中 HTTP 服务器优雅关闭的实现方式

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
