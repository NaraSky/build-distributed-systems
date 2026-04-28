# Compare gRPC vs REST: 延迟, Size,和DX

英文标题：Compare gRPC vs REST: Latency, Size,和DX
网页：<https://builddistributedsystem.com/tracks/networker/tasks/task-5-3-5-grpc-vs-rest>

课程：17. 网络器：TCP 与协议基础
任务序号：15
短标题：gRPC vs REST
难度：intermediate
子主题：gRPC和Protocol Buffers

## 中文导读

本题要求你完成 `Compare gRPC vs REST: 延迟, Size,和DX`。

重点关注：`REST`、`gRPC`、`HTTP/2`、`JSON vs protobuf`、`developer experience`。

建议先按提示逐步实现：gRPC uses HTTP/2 (multiplexing, header compression) while REST typically uses HTTP/1.1。

协议字段、消息类型、输入输出格式请以本文件中的代码块和测试用例为准。

## 题目说明

Compare gRPC和REST across multiple dimensions. Build both a REST-style和gRPC-style endpoint用于the same service和measure the differences.

Implement comparison handlers:

```JSON
请求:  {"type": "rest_call", "msg_id": 1, "method": "GET", "path": "/api/users/1"}
响应: {"type": "rest_call_ok", "in_reply_to": 1, "status": 200, "body": {"id": 1, "name": "Alice"}, "content_type": "application/JSON", "size_bytes": 28}

请求:  {"type": "grpc_call", "msg_id": 2, "service": "Users", "method": "GetUser", "请求": {"id": 1}}
响应: {"type": "grpc_call_ok", "in_reply_to": 2, "status": "OK", "响应": {"id": 1, "name": "Alice"}, "size_bytes": 9}

请求:  {"type": "compare_protocols", "msg_id": 3, "num_calls": 100}
响应: {"type": "compare_protocols_ok", "in_reply_to": 3, "comparison": {
    "rest": {"avg_size_bytes": 28, "avg_latency_us": 500, "browser_support": true, "code_gen": false},
    "grpc": {"avg_size_bytes": 9, "avg_latency_us": 120, "browser_support": false, "code_gen": true},
    "size_reduction_pct": 67.9,
    "latency_reduction_pct": 76.0
}}
```

## 涉及概念

- `REST`
- `gRPC`
- `HTTP/2`
- `JSON vs protobuf`
- `developer experience`

## 实现提示

- gRPC uses HTTP/2 (multiplexing, header compression) while REST typically uses HTTP/1.1
- Protobuf encoding is 3-10x smaller than JSON用于the same data
- gRPC has built-in code generation; REST requires manual 客户端 libraries
- REST is more browser-friendly; gRPC requires gRPC-Web用于browser clients
- Compare on: serialization size, latency, tooling, debugging ease

## 测试用例

### 1. REST call returns JSON

rest_call_ok，包含status 200, JSON body,和content_type application/JSON.

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"rest_call","msg_id":2,"method":"GET","path":"/api/users/1"}}
```

期望输出：

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

### 2. gRPC call returns protobuf-sized response

grpc_call_ok should show size_bytes significantly smaller than equivalent REST 响应.

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"grpc_call","msg_id":2,"service":"Users","method":"GetUser","request":{"id":1}}}
```

期望输出：

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

## 参考资料

- [gRPC vs REST Performance Comparison](https://cloud.google.com/blog/products/api-management/understanding-grpc-openapi-and-rest-and-when-to-use-them)：Google Cloud blog comparing gRPC, REST,和OpenAPI

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
