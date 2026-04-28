# 实现 a gRPC Unary RPC 服务

英文标题：Implement a gRPC Unary RPC Service
网页：<https://builddistributedsystem.com/tracks/networker/tasks/task-5-3-2-grpc-unary>

课程：17. 网络器：TCP 与协议基础
任务序号：12
短标题：gRPC Unary
难度：intermediate
子主题：gRPC和Protocol Buffers

## 中文导读

本题要求你完成 `实现 a gRPC Unary RPC 服务`。

重点关注：`gRPC`、`unary RPC`、`HTTP/2`、`service definition`、`stub`。

建议先按提示逐步实现：Unary RPC: 客户端 sends one 请求, 服务端 sends one 响应。

协议字段、消息类型、输入输出格式请以本文件中的代码块和测试用例为准。

## 题目说明

Implement a gRPC-style unary RPC service. In unary RPC, the 客户端 sends exactly one 请求和receives exactly one 响应.

gRPC 消息 format on the wire:
`[compressed_flag: 1 byte][message_length: 4 bytes][protobuf_message]`

Implement a simple KeyValue service:

```JSON
请求:  {"type": "grpc_call", "msg_id": 1, "service": "KeyValue", "method": "Get", "请求": {"key": "user:1"}}
响应: {"type": "grpc_call_ok", "in_reply_to": 1, "status": "OK", "响应": {"key": "user:1", "value": "Alice", "found": true}}

请求:  {"type": "grpc_call", "msg_id": 2, "service": "KeyValue", "method": "Put", "请求": {"key": "user:2", "value": "Bob"}}
响应: {"type": "grpc_call_ok", "in_reply_to": 2, "status": "OK", "响应": {"written": true}}

请求:  {"type": "grpc_call", "msg_id": 3, "service": "KeyValue", "method": "Get", "请求": {"key": "missing"}}
响应: {"type": "grpc_call_ok", "in_reply_to": 3, "status": "NOT_FOUND", "响应": {"key": "missing", "found": false}}
```

## 涉及概念

- `gRPC`
- `unary RPC`
- `HTTP/2`
- `service definition`
- `stub`

## 实现提示

- Unary RPC: 客户端 sends one 请求, 服务端 sends one 响应
- gRPC uses HTTP/2 as its transport protocol
- Each RPC method maps to a (service, method) pair
- The 请求和响应 are protobuf-encoded 消息
- gRPC adds a 5-byte header: 1 byte compressed flag + 4 bytes 消息 length

## 测试用例

### 1. Put和Get a key

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"grpc_call","msg_id":2,"service":"KeyValue","method":"Put","request":{"key":"k1","value":"v1"}}}
{"src":"c1","dest":"n1","body":{"type":"grpc_call","msg_id":3,"service":"KeyValue","method":"Get","request":{"key":"k1"}}}
```

期望输出：

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
{"src": "n1", "dest": "c1", "body": {"type": "grpc_call_ok", "in_reply_to": 2, "status": "OK", "response": {"written": true}, "msg_id": 1}}
{"src": "n1", "dest": "c1", "body": {"type": "grpc_call_ok", "in_reply_to": 3, "status": "OK", "response": {"key": "k1", "value": "v1", "found": true}, "msg_id": 2}}
```

### 2. Get missing key returns NOT_FOUND

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"grpc_call","msg_id":2,"service":"KeyValue","method":"Get","request":{"key":"missing"}}}
```

期望输出：

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
{"src": "n1", "dest": "c1", "body": {"type": "grpc_call_ok", "in_reply_to": 2, "status": "NOT_FOUND", "response": {"key": "missing", "found": false}, "msg_id": 1}}
```

## 参考资料

- [gRPC Core Concepts](https://grpc.io/docs/what-is-grpc/core-concepts/)：Overview of gRPC service definitions, RPC types,和lifecycle

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
