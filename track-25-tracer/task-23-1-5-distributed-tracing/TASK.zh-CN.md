# 实现 End-to-End Distributed Tracing System

英文标题：Implement End-to-End Distributed Tracing System
网页：<https://builddistributedsystem.com/tracks/tracer/tasks/task-23-1-5-distributed-tracing>

课程：25. 追踪器：可观测性
任务序号：5
短标题：End-to-End Tracing
难度：advanced
子主题：Distributed Tracing

## 中文导读

本题要求你完成 `实现 End-to-End Distributed Tracing System`。

重点关注：`auto-instrumentation`、`manual instrumentation`、`log-trace correlation`、`service mesh tracing`。

建议先按提示逐步实现：Auto-instrumentation: wrap each service，包含a tracing interceptor that creates spans automatically。

协议字段、消息类型、输入输出格式请以本文件中的代码块和测试用例为准。

## 题目说明

Individual span operations give you the building blocks. End-to-end tracing connects them: every service creates和propagates spans, logs are correlated，包含trace IDs,和you get complete visibility across the entire call chain without manual wiring.

Implement a 节点 that supports full distributed tracing infrastructure:

```JSON
// Auto-instrument three services, then handle a 请求
{ "type": "instrument_service", "msg_id": 1,
  "services": ["web","api","db"], "auto": true }
{ "type": "http_request", "path": "/api/users/123" }
-> { "type": "trace_complete",
    "trace_id": "<uuid>",
    "services": ["web","api","db"], "span_count": 3 }

// Attach trace_id to logs用于correlation
{ "type": "日志", "msg_id": 3,
  "消息": "Processing 请求", "trace_id": "abc123" }
{ "type": "search_logs", "msg_id": 4, "trace_id": "abc123" }
-> { "type": "search_results", "in_reply_to": 4,
    "logs": [{"service":"service","消息":"Processing 请求",
               "trace_id":"abc123"}] }
```

## 涉及概念

- `auto-instrumentation`
- `manual instrumentation`
- `log-trace correlation`
- `service mesh tracing`

## 实现提示

- Auto-instrumentation: wrap each service，包含a tracing interceptor that creates spans automatically
- Manual: tracer.startSpan(name) -> do work -> span.end() (or span.recordException(e) on error)
- 日志-trace correlation: attach trace_id to every 日志 entry; 索引 logs by trace_id
- Service mesh sidecar: injects tracing at the 网络 layer without application code changes
- span_count = number of services instrumented in the call chain

## 测试用例

### 1. Instrument multiple services

Auto-instrumentation should create one span per service in the call chain.

输入：

```json
{"src":"instrumentor","dest":"services","body":{"type":"instrument_service","msg_id":1,"services":["web","api","db"],"auto":true}}
{"src":"user","dest":"web","body":{"type":"http_request","path":"/api/users/123"}}
```

期望输出：

```text
{"type": "trace_complete", "trace_id": ".*", "services": ["web", "api", "db"], "span_count": 3}
```

### 2. Manual instrumentation

Manual instrumentation should create one span，包含proper lifecycle handling.

输入：

```json
{"src":"developer","dest":"code","body":{"type":"manual_instrument","msg_id":1,"code":"async function process() { const span = tracer.startSpan('process'); try { await work(); span.end(); } catch(e) { span.recordException(e); throw; } }"}}
```

期望输出：

```text
{"type": "instrumentation_ok", "in_reply_to": 1, "spans_created": 1}
```

## 参考资料

- [OpenTelemetry](https://opentelemetry.io/docs/)：Vendor-neutral standard用于distributed tracing, metrics,和logs

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
