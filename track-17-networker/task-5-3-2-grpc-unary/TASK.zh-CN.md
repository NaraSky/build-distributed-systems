# 实现 gRPC 一元调用服务

英文标题：Implement a gRPC Unary RPC Service
网页：<https://builddistributedsystem.com/tracks/networker/tasks/task-5-3-2-grpc-unary>

课程：17. 网络器：TCP 与协议基础
任务序号：12
短标题：gRPC 一元调用
难度：进阶
子主题：gRPC 与 Protocol Buffers

## 中文导读

这道题让你实现 gRPC 风格的一元调用（Unary RPC）服务。一元调用是最简单的 RPC 模式：客户端发送一个请求，服务器返回一个响应，就像普通的函数调用一样。gRPC 基于 HTTP/2 协议传输，使用 Protobuf 编码消息体，并在消息前加上 5 字节的头部（1 字节压缩标志 + 4 字节消息长度）。通过实现一个简单的键值存储服务，你将掌握 gRPC 的基本工作模式。

## 题目说明

实现一个 gRPC 风格的一元调用服务。在一元调用中，客户端发送恰好一个请求，接收恰好一个响应。

gRPC 消息在线路上的格式：
`[compressed_flag: 1 字节][message_length: 4 字节][protobuf_message]`

实现一个简单的键值存储服务：

```json
Request:  {"type": "grpc_call", "msg_id": 1, "service": "KeyValue", "method": "Get", "request": {"key": "user:1"}}
Response: {"type": "grpc_call_ok", "in_reply_to": 1, "status": "OK", "response": {"key": "user:1", "value": "Alice", "found": true}}

Request:  {"type": "grpc_call", "msg_id": 2, "service": "KeyValue", "method": "Put", "request": {"key": "user:2", "value": "Bob"}}
Response: {"type": "grpc_call_ok", "in_reply_to": 2, "status": "OK", "response": {"written": true}}

Request:  {"type": "grpc_call", "msg_id": 3, "service": "KeyValue", "method": "Get", "request": {"key": "missing"}}
Response: {"type": "grpc_call_ok", "in_reply_to": 3, "status": "NOT_FOUND", "response": {"key": "missing", "found": false}}
```

## 涉及概念

- `gRPC`
- `unary RPC`
- `HTTP/2`
- `service definition`
- `stub`

## 实现提示

- 一元调用：客户端发送一个请求，服务器返回一个响应
- gRPC 使用 HTTP/2 作为传输协议
- 每个 RPC 方法映射到一个（服务名, 方法名）的组合
- 请求和响应都是 Protobuf 编码的消息
- gRPC 在消息前加了 5 字节头部：1 字节压缩标志 + 4 字节消息长度

## 测试用例

### 1. 写入并读取一个键

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

### 2. 读取不存在的键返回 NOT_FOUND

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

- [gRPC Core Concepts](https://grpc.io/docs/what-is-grpc/core-concepts/)：gRPC 服务定义、RPC 类型和生命周期的概览

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
