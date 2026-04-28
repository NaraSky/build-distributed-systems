# 实现端到端分布式追踪系统

英文标题：Implement End-to-End Distributed Tracing System
网页：<https://builddistributedsystem.com/tracks/tracer/tasks/task-23-1-5-distributed-tracing>

课程：25. 追踪器：可观测性
任务序号：5
短标题：End-to-End Tracing
难度：高级
子主题：Distributed Tracing

## 中文导读

这道题要求你实现一个完整的端到端分布式追踪系统。前面的任务让你掌握了跨度的各项基础操作，而这道题把它们全部串联起来：每个服务自动创建和传播跨度、日志与追踪标识关联、整条调用链的完整可见性，无需手动接线。这是分布式追踪子主题的综合实战。

## 题目说明

前面的任务给了你分布式追踪的各个积木块，而端到端追踪则把它们串联起来：每个服务都创建并传播跨度，日志通过追踪标识进行关联，你无需手动接线就能获得整条调用链的完整可见性。

请实现一个节点，支持完整的分布式追踪基础设施：

```json
// 自动探针注入三个服务，然后处理一个请求
{ "type": "instrument_service", "msg_id": 1,
  "services": ["web","api","db"], "auto": true }
{ "type": "http_request", "path": "/api/users/123" }
-> { "type": "trace_complete",
    "trace_id": "<uuid>",
    "services": ["web","api","db"], "span_count": 3 }

// 将 trace_id 附加到日志中实现关联
{ "type": "log", "msg_id": 3,
  "message": "Processing request", "trace_id": "abc123" }
{ "type": "search_logs", "msg_id": 4, "trace_id": "abc123" }
-> { "type": "search_results", "in_reply_to": 4,
    "logs": [{"service":"service","message":"Processing request",
               "trace_id":"abc123"}] }
```

## 概念说明

**自动探针注入**（Auto-instrumentation）就像给每个服务装上一个透明的"记录仪"，它会自动为每次请求创建跨度，开发者不需要修改业务代码。**日志与追踪关联**则是把日志条目和追踪标识绑定在一起，这样你在排查问题时，可以通过一个追踪标识同时找到对应的追踪数据和日志信息。

## 涉及概念

- `auto-instrumentation`
- `manual instrumentation`
- `log-trace correlation`
- `service mesh tracing`

## 实现提示

- 自动探针注入：为每个服务包装一个追踪拦截器，自动创建跨度
- 手动探针注入：`tracer.startSpan(name)` -> 执行业务逻辑 -> `span.end()`（出错时调用 `span.recordException(e)`）
- 日志与追踪关联：为每条日志附加 trace_id；按 trace_id 建立日志索引
- 服务网格边车：在网络层注入追踪功能，无需修改应用代码
- span_count 等于调用链中被注入探针的服务数量

## 测试用例

### 1. 为多个服务注入探针

自动探针注入应当在调用链中为每个服务创建一个跨度。

输入：

```json
{"src":"instrumentor","dest":"services","body":{"type":"instrument_service","msg_id":1,"services":["web","api","db"],"auto":true}}
{"src":"user","dest":"web","body":{"type":"http_request","path":"/api/users/123"}}
```

期望输出：

```text
{"type": "trace_complete", "trace_id": ".*", "services": ["web", "api", "db"], "span_count": 3}
```

### 2. 手动探针注入

手动探针注入应当创建一个跨度并正确管理其生命周期。

输入：

```json
{"src":"developer","dest":"code","body":{"type":"manual_instrument","msg_id":1,"code":"async function process() { const span = tracer.startSpan('process'); try { await work(); span.end(); } catch(e) { span.recordException(e); throw; } }"}}
```

期望输出：

```text
{"type": "instrumentation_ok", "in_reply_to": 1, "spans_created": 1}
```

## 参考资料

- [OpenTelemetry](https://opentelemetry.io/docs/)：厂商中立的分布式追踪、指标和日志标准

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
