# 构建 gRPC 拦截器：日志、认证与限流

英文标题：Build gRPC Interceptors for Logging, Auth, and Rate Limiting
网页：<https://builddistributedsystem.com/tracks/networker/tasks/task-5-3-4-grpc-interceptors>

课程：17. 网络器：TCP 与协议基础
任务序号：14
短标题：gRPC 拦截器
难度：高级
子主题：gRPC 与 Protocol Buffers

## 中文导读

这道题让你构建一个 gRPC 拦截器（Interceptor）管道。拦截器类似于 Web 开发中的中间件（Middleware），它们像洋葱一样一层层包裹在实际的业务处理逻辑外面，在请求到达处理器之前和之后执行额外的逻辑。你将实现三个拦截器：日志记录、身份认证和限流，并把它们串成一个调用链。这是生产级 gRPC 服务中不可或缺的基础设施。

## 题目说明

构建一个 gRPC 拦截器管道。拦截器是包裹在 gRPC 处理器外层的中间件，在实际的服务方法执行前后运行额外的逻辑。

拦截器调用链：`logging -> auth -> rate_limit -> handler`

实现以下消息处理器：

```json
Request:  {"type": "grpc_call", "msg_id": 1, "service": "KeyValue", "method": "Get", "request": {"key": "k1"}, "metadata": {"authorization": "Bearer valid_token"}}
Response: {"type": "grpc_call_ok", "in_reply_to": 1, "status": "OK", "interceptors_applied": ["logging", "auth", "rate_limit"], "response": {"key": "k1", "value": "v1", "found": true}}

Request:  {"type": "grpc_call", "msg_id": 2, "service": "KeyValue", "method": "Get", "request": {"key": "k1"}, "metadata": {}}
Response: {"type": "grpc_call_ok", "in_reply_to": 2, "status": "UNAUTHENTICATED", "interceptor_failed": "auth"}

Request:  {"type": "grpc_interceptor_stats", "msg_id": 3}
Response: {"type": "grpc_interceptor_stats_ok", "in_reply_to": 3, "stats": {
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

- 拦截器是 gRPC 调用的中间件，类似于 HTTP 中间件
- 它们在实际处理器的前后运行
- 将多个拦截器串联起来：logging -> auth -> rate_limit -> handler
- 认证拦截器检查元数据中是否包含有效的令牌
- 限流器使用令牌桶算法，按客户端 IP 进行限流

## 测试用例

### 1. 已认证的请求通过所有拦截器

验证说明：grpc_call_ok 的状态为 OK，interceptors_applied 包含全部三个拦截器。

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"grpc_call","msg_id":2,"service":"KeyValue","method":"Put","request":{"key":"k1","value":"v1"},"metadata":{"authorization":"Bearer valid_token"}}}
```

期望输出：

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

### 2. 缺少认证令牌时在认证拦截器处失败

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

- [gRPC Interceptors in Go](https://grpc.io/docs/guides/interceptors/)：如何为 gRPC 实现客户端和服务端拦截器

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
