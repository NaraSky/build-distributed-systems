# 实现 服务 Mesh Architecture

英文标题：Implement Service Mesh Architecture
网页：<https://builddistributedsystem.com/tracks/orchestrator/tasks/task-26-2-1-service-mesh>

课程：28. 编排器：容器调度与服务网格
任务序号：6
短标题：服务 Mesh
难度：advanced
子主题：服务 Mesh

## 中文导读

本题要求你完成 `实现 服务 Mesh Architecture`。

重点关注：`service mesh`、`sidecar proxy`、`service discovery`、`circuit breaker`、`retry`。

建议先按提示逐步实现：A sidecar 代理 intercepts all inbound和outbound traffic用于its service。

协议字段、消息类型、输入输出格式请以本文件中的代码块和测试用例为准。

## 题目说明

A service mesh adds a sidecar 代理 to every service. All traffic flows through these proxies, which transparently handle service discovery, retries, circuit breaking,和distributed tracing without any application code changes.

Implement a 节点 that simulates sidecar 代理 behaviour:

```JSON
// Sidecar intercepts a 请求和adds tracing context
{ "type": "call", "msg_id": 1, "path": "/api/users/123", "代理": true }
-> { "type": "proxied", "in_reply_to": 1,
    "proxied_by": "sidecar-a", "trace_id": "<uuid>" }

// Discover healthy instances of a service
{ "type": "discover", "msg_id": 2, "service": "service-b" }
-> { "type": "discovered", "in_reply_to": 2,
    "service": "service-b",
    "instances": [{"host": "10.0.1.1", "port": 8080},
                  {"host": "10.0.1.2", "port": 8080}] }

// Circuit breaker opens after too many failures
{ "type": "call", "msg_id": 3,
  "force_failures": 6, "circuit_breaker": true }
-> { "type": "circuit_breaker_open", "in_reply_to": 3,
    "service": "service-b", "reason": "Too many failures" }
```

Every 请求 proxied through the sidecar must receive a unique `trace_id` that can be propagated to downstream services用于end-to-end tracing.

## 涉及概念

- `service mesh`
- `sidecar proxy`
- `service discovery`
- `circuit breaker`
- `retry`
- `distributed tracing`

## 实现提示

- A sidecar 代理 intercepts all inbound和outbound traffic用于its service
- discover queries the service registry用于healthy instances of a named service
- Add a trace_id to every proxied 请求 so traces can be correlated across services
- Circuit breaker opens when 故障 count exceeds the threshold; fail immediately while open
- 重试，包含exponential backoff: first 重试 after base_ms, second after base_ms*2, etc.

## 测试用例

### 1. Sidecar 代理 intercepts traffic

Sidecar should intercept和forward 请求，包含a trace_id.

输入：

```json
{"src":"service-a","dest":"service-b","body":{"type":"call","msg_id":1,"path":"/api/users/123"},"proxy":true}
```

期望输出：

```text
{"type": "proxied", "in_reply_to": 1, "proxied_by": "sidecar-a", "trace_id": ".*"}
```

### 2. 服务 discovery routes to instances

Should return healthy instances from the service registry.

输入：

```json
{"src":"sidecar","dest":"registry","body":{"type":"discover","msg_id":1,"service":"service-b"}}
```

期望输出：

```text
{"type": "discovered", "in_reply_to": 1, "service": "service-b", "instances": [{"host": "10.0.1.1", "port": 8080}, {"host": "10.0.1.2", "port": 8080}]}
```

## 参考资料

- [Service Mesh Explained](https://www.nginx.com/blog/what-is-a-service-mesh/)：What a service mesh is和why you need one
- [Envoy Proxy](https://www.envoyproxy.io/)：Envoy 代理 documentation

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
