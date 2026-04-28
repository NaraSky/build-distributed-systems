# gRPC 与 REST 对比：延迟、体积与开发体验

英文标题：Compare gRPC vs REST: Latency, Size, and DX
网页：<https://builddistributedsystem.com/tracks/networker/tasks/task-5-3-5-grpc-vs-rest>

课程：17. 网络器：TCP 与协议基础
任务序号：15
短标题：gRPC 与 REST 对比
难度：进阶
子主题：gRPC 与 Protocol Buffers

## 中文导读

这道题让你从多个维度对比 gRPC 和 REST 两种通信方式。在实际项目中，选择哪种方案取决于具体场景。REST 基于 HTTP/1.1，使用 JSON 编码，浏览器友好，调试方便；gRPC 基于 HTTP/2，使用 Protobuf 编码，数据更紧凑，延迟更低，还自带代码生成。通过同时实现两种端点并测量它们的差异，你将对两者的优劣有切实的理解，而不只是停留在理论层面。

## 题目说明

从多个维度对比 gRPC 和 REST。为同一个服务分别构建 REST 风格和 gRPC 风格的端点，并测量它们之间的差异。

实现以下对比用的消息处理器：

```json
Request:  {"type": "rest_call", "msg_id": 1, "method": "GET", "path": "/api/users/1"}
Response: {"type": "rest_call_ok", "in_reply_to": 1, "status": 200, "body": {"id": 1, "name": "Alice"}, "content_type": "application/json", "size_bytes": 28}

Request:  {"type": "grpc_call", "msg_id": 2, "service": "Users", "method": "GetUser", "request": {"id": 1}}
Response: {"type": "grpc_call_ok", "in_reply_to": 2, "status": "OK", "response": {"id": 1, "name": "Alice"}, "size_bytes": 9}

Request:  {"type": "compare_protocols", "msg_id": 3, "num_calls": 100}
Response: {"type": "compare_protocols_ok", "in_reply_to": 3, "comparison": {
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

- gRPC 使用 HTTP/2（支持多路复用和头部压缩），而 REST 通常使用 HTTP/1.1
- 对于相同的数据，Protobuf 编码的体积比 JSON 小 3 到 10 倍
- gRPC 内置代码生成工具；REST 需要手动编写客户端库
- REST 对浏览器更友好；gRPC 需要通过 gRPC-Web 才能在浏览器中使用
- 从以下维度进行对比：序列化体积、延迟、工具链、调试便捷性

## 测试用例

### 1. REST 调用返回 JSON

验证说明：rest_call_ok 的状态码为 200，包含 JSON 响应体，content_type 为 application/json。

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"rest_call","msg_id":2,"method":"GET","path":"/api/users/1"}}
```

期望输出：

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

### 2. gRPC 调用返回 Protobuf 大小的响应

验证说明：grpc_call_ok 中的 size_bytes 应明显小于等价的 REST 响应。

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

- [gRPC vs REST Performance Comparison](https://cloud.google.com/blog/products/api-management/understanding-grpc-openapi-and-rest-and-when-to-use-them)：Google Cloud 博客对比 gRPC、REST 和 OpenAPI 的文章

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
