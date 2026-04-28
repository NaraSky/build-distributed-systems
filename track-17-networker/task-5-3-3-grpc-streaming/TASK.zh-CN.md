# 实现 gRPC Server和Bidirectional Streaming

英文标题：Implement gRPC Server和Bidirectional Streaming
网页：<https://builddistributedsystem.com/tracks/networker/tasks/task-5-3-3-grpc-streaming>

课程：17. 网络器：TCP 与协议基础
任务序号：13
短标题：gRPC Streaming
难度：advanced
子主题：gRPC和Protocol Buffers

## 中文导读

本题要求你完成 `实现 gRPC Server和Bidirectional Streaming`。

重点关注：`server streaming`、`bidirectional streaming`、`HTTP/2 streams`、`flow control`。

建议先按提示逐步实现：服务端 streaming: 客户端 sends one 请求, 服务端 sends multiple responses。

协议字段、消息类型、输入输出格式请以本文件中的代码块和测试用例为准。

## 题目说明

Implement gRPC streaming RPCs:

1. **服务端 streaming**: 客户端 sends one 请求, 服务端 sends a stream of responses
2. **Bidirectional streaming**: Both sides send streams of 消息 concurrently

Use a 日志-watching service as the example:

```JSON
请求:  {"type": "grpc_server_stream", "msg_id": 1, "service": "LogWatcher", "method": "WatchLogs", "请求": {"filter": "ERROR", "limit": 3}}
响应: [
    {"type": "grpc_stream_msg", "in_reply_to": 1, "seq": 1, "data": {"level": "ERROR", "msg": "disk full"}},
    {"type": "grpc_stream_msg", "in_reply_to": 1, "seq": 2, "data": {"level": "ERROR", "msg": "connection reset"}},
    {"type": "grpc_stream_msg", "in_reply_to": 1, "seq": 3, "data": {"level": "ERROR", "msg": "超时"}},
    {"type": "grpc_stream_end", "in_reply_to": 1, "status": "OK", "count": 3}
]

请求:  {"type": "grpc_bidi_stream_open", "msg_id": 2, "service": "Chat", "method": "BiDiChat"}
响应: {"type": "grpc_bidi_stream_open_ok", "in_reply_to": 2, "stream_id": "s1"}

请求:  {"type": "grpc_bidi_stream_send", "msg_id": 3, "stream_id": "s1", "data": {"text": "hello"}}
响应: {"type": "grpc_bidi_stream_recv", "in_reply_to": 3, "data": {"text": "echo: hello"}}
```

## 涉及概念

- `server streaming`
- `bidirectional streaming`
- `HTTP/2 streams`
- `flow control`

## 实现提示

- 服务端 streaming: 客户端 sends one 请求, 服务端 sends multiple responses
- Bidirectional streaming: both sides send multiple 消息 over the same connection
- Each 消息 in the stream uses the same gRPC framing (compressed flag + length)
- The 服务端 signals end-of-stream，包含gRPC trailers (grpc-status)
- Track the stream state: OPEN, HALF_CLOSED, CLOSED

## 测试用例

### 1. Server streaming returns multiple messages

Should receive 2 grpc_stream_msg responses followed by grpc_stream_end，包含count: 2.

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"grpc_server_stream","msg_id":2,"service":"LogWatcher","method":"WatchLogs","request":{"filter":"ERROR","limit":2}}}
```

期望输出：

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

### 2. Bidi stream open和send

grpc_bidi_stream_open_ok should return a stream_id. grpc_bidi_stream_recv should echo the 消息.

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

- [gRPC Streaming](https://grpc.io/docs/what-is-grpc/core-concepts/#server-streaming-rpc)：gRPC 服务端 streaming和bidirectional streaming RPC types

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
