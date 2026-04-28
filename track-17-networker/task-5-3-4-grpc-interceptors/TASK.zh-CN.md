# 构建 gRPC Interceptors用于Logging, Auth,和Rate Limiting

英文标题：Build gRPC Interceptors用于Logging, Auth,和Rate Limiting
网页：<https://builddistributedsystem.com/tracks/networker/tasks/task-5-3-4-grpc-interceptors>

课程：17. 网络器：TCP 与协议基础
任务序号：14
短标题：gRPC Interceptors
难度：advanced
子主题：gRPC和Protocol Buffers

## 中文导读

本题要求你完成 `构建 gRPC Interceptors用于Logging, Auth,和Rate Limiting`。

重点关注：`interceptor`、`middleware`、`authentication`、`rate limiting`、`request pipeline`。

建议先按提示逐步实现：Interceptors are middleware用于gRPC calls, similar to HTTP middleware。

协议字段、消息类型、输入输出格式请以本文件中的代码块和测试用例为准。

## 题目说明

Build a gRPC interceptor pipeline. Interceptors are middleware that wrap gRPC handler calls, running logic before和after the actual service method.

Interceptor chain: `logging -> auth -> rate_limit -> handler`

Implement handlers:

```JSON
请求:  {"type": "grpc_call", "msg_id": 1, "service": "KeyValue", "method": "Get", "请求": {"key": "k1"}, "元数据": {"authorization": "Bearer valid_token"}}
响应: {"type": "grpc_call_ok", "in_reply_to": 1, "status": "OK", "interceptors_applied": ["logging", "auth", "rate_limit"], "响应": {"key": "k1", "value": "v1", "found": true}}

请求:  {"type": "grpc_call", "msg_id": 2, "service": "KeyValue", "method": "Get", "请求": {"key": "k1"}, "元数据": {}}
响应: {"type": "grpc_call_ok", "in_reply_to": 2, "status": "UNAUTHENTICATED", "interceptor_failed": "auth"}

请求:  {"type": "grpc_interceptor_stats", "msg_id": 3}
响应: {"type": "grpc_interceptor_stats_ok", "in_reply_to": 3, "stats": {
    "total_requests": 2, "auth_failures": 1, "rate_limited": 0
}}
```

## 涉及概念

- `interceptor`
- `middleware`
- `authentication`
- `rate limiting`
- `request pipeline`

## 实现提示

- Interceptors are middleware用于gRPC calls, similar to HTTP middleware
- They run before和after the actual handler
- Chain multiple interceptors: logging -> auth -> rate_limit -> handler
- Auth interceptor checks 元数据用于a valid token
- Rate limiter uses a token bucket per 客户端 IP

## 测试用例

### 1. Authenticated request passes all interceptors

grpc_call_ok，包含status OK和interceptors_applied containing all three interceptors.

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"grpc_call","msg_id":2,"service":"KeyValue","method":"Put","request":{"key":"k1","value":"v1"},"metadata":{"authorization":"Bearer valid_token"}}}
```

期望输出：

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

### 2. Missing auth token fails at auth interceptor

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"grpc_call","msg_id":2,"service":"KeyValue","method":"Get","request":{"key":"k1"},"metadata":{}}}
```

期望输出：

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
{"src": "n1", "dest": "c1", "body": {"type": "grpc_call_ok", "in_reply_to": 2, "status": "UNAUTHENTICATED", "interceptor_failed": "auth", "msg_id": 1}}
```

## 参考资料

- [gRPC Interceptors in Go](https://grpc.io/docs/guides/interceptors/)：How to implement 客户端和服务端 interceptors用于gRPC

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
