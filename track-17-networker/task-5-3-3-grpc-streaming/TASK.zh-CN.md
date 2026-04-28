# 实现 gRPC 服务端流和双向流

英文标题：Implement gRPC Server and Bidirectional Streaming
网页：<https://builddistributedsystem.com/tracks/networker/tasks/task-5-3-3-grpc-streaming>

课程：17. 网络器：TCP 与协议基础
任务序号：13
短标题：gRPC 流式调用
难度：高级
子主题：gRPC 与 Protocol Buffers

## 中文导读

这道题让你实现 gRPC 的流式调用，包括服务端流（Server Streaming）和双向流（Bidirectional Streaming）。与一元调用不同，流式调用允许一方或双方发送多条消息。服务端流就像订阅一个日志推送：你发一个请求说"我要看错误日志"，服务器就源源不断地把匹配的日志推送给你。双向流更像聊天室，双方可以同时发送消息。这是构建实时推送、事件订阅等场景的基础。

## 题目说明

实现 gRPC 的流式远程过程调用：

1. **服务端流**：客户端发送一个请求，服务器返回一个响应流（多条消息）
2. **双向流**：双方同时发送消息流

以日志监控服务为例：

```json
Request:  {"type": "grpc_server_stream", "msg_id": 1, "service": "LogWatcher", "method": "WatchLogs", "request": {"filter": "ERROR", "limit": 3}}
Response: [
    {"type": "grpc_stream_msg", "in_reply_to": 1, "seq": 1, "data": {"level": "ERROR", "msg": "disk full"}},
    {"type": "grpc_stream_msg", "in_reply_to": 1, "seq": 2, "data": {"level": "ERROR", "msg": "connection reset"}},
    {"type": "grpc_stream_msg", "in_reply_to": 1, "seq": 3, "data": {"level": "ERROR", "msg": "timeout"}},
    {"type": "grpc_stream_end", "in_reply_to": 1, "status": "OK", "count": 3}
]

Request:  {"type": "grpc_bidi_stream_open", "msg_id": 2, "service": "Chat", "method": "BiDiChat"}
Response: {"type": "grpc_bidi_stream_open_ok", "in_reply_to": 2, "stream_id": "s1"}

Request:  {"type": "grpc_bidi_stream_send", "msg_id": 3, "stream_id": "s1", "data": {"text": "hello"}}
Response: {"type": "grpc_bidi_stream_recv", "in_reply_to": 3, "data": {"text": "echo: hello"}}
```

## 涉及概念

- `server streaming`
- `bidirectional streaming`
- `HTTP/2 streams`
- `flow control`

## 实现提示

- 服务端流：客户端发送一个请求，服务器返回多条响应
- 双向流：双方通过同一个连接发送多条消息
- 流中的每条消息都使用相同的 gRPC 分帧格式（压缩标志 + 长度）
- 服务器通过 gRPC 尾部元数据（grpc-status）来通知流结束
- 跟踪流的状态：OPEN（打开）、HALF_CLOSED（半关闭）、CLOSED（已关闭）

## 测试用例

### 1. 服务端流返回多条消息

验证说明：应收到 2 条 grpc_stream_msg 响应，随后是一条 grpc_stream_end，其中 count 为 2。

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"grpc_server_stream","msg_id":2,"service":"LogWatcher","method":"WatchLogs","request":{"filter":"ERROR","limit":2}}}
```

期望输出：

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

### 2. 双向流的打开与发送

验证说明：grpc_bidi_stream_open_ok 应返回一个 stream_id。grpc_bidi_stream_recv 应将消息回声返回。

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"grpc_bidi_stream_open","msg_id":2,"service":"Chat","method":"BiDiChat"}}
{"src":"c1","dest":"n1","body":{"type":"grpc_bidi_stream_send","msg_id":3,"stream_id":"s1","data":{"text":"hello"}}}
```

期望输出：

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

## 参考资料

- [gRPC Streaming](https://grpc.io/docs/what-is-grpc/core-concepts/#server-streaming-rpc)：gRPC 服务端流和双向流 RPC 类型的介绍

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
