# 实现 Distributed Trace Context Propagation

英文标题：Implement Distributed Trace Context Propagation
网页：<https://builddistributedsystem.com/tracks/tracer/tasks/task-23-1-1-trace-context-propagation>

课程：25. 追踪器：可观测性
任务序号：1
短标题：Trace Propagation
难度：intermediate
子主题：Distributed Tracing

## 中文导读

本题要求你完成 `实现 Distributed Trace Context Propagation`。

重点关注：`distributed tracing`、`trace context`、`W3C traceparent`、`span`、`trace tree`。

建议先按提示逐步实现：W3C traceparent format: 00-{trace_id}-{parent_span_id}-{flags}。

协议字段、消息类型、输入输出格式请以本文件中的代码块和测试用例为准。

## 题目说明

Distributed tracing links spans from a single 请求 as it flows through multiple services. Each service propagates the trace context (trace ID + parent span ID) in a header so every hop can be assembled into a single trace tree.

Implement a 节点 that handles trace context operations:

```JSON
// Service B receives 请求，包含traceparent -> creates child span
{ "type": "http_request", "msg_id": 1, "path": "/api/data",
  "headers": {"traceparent": "00-trace123-span_a-01"} }
-> { "type": "http_response", "in_reply_to": 1,
    "span": {"trace_id": "trace123", "span_id": "span_b",
              "parent_span_id": "span_a"} }

// Parse a W3C traceparent header into its parts
{ "type": "parse_traceparent", "msg_id": 2,
  "traceparent": "00-4bf92f3577b34da6a3ce929d0e0e4736-00f067aa0ba902b57-01" }
-> { "type": "parse_ok", "in_reply_to": 2,
    "trace_id": "4bf92f3577b34da6a3ce929d0e0e4736",
    "parent_span_id": "00f067aa0ba902b57", "sampled": true }

// Reconstruct trace tree from span list
{ "type": "reconstruct_trace", "msg_id": 3,
  "spans": [{"trace_id":"t1","span_id":"s1","parent":null},
             {"trace_id":"t1","span_id":"s2","parent":"s1"},
             {"trace_id":"t1","span_id":"s3","parent":"s2"}] }
-> { "type": "trace_tree_ok", "in_reply_to": 3,
    "trace_id": "t1", "span_count": 3, "depth": 3 }
```

## 涉及概念

- `distributed tracing`
- `trace context`
- `W3C traceparent`
- `span`
- `trace tree`

## 实现提示

- W3C traceparent format: 00-{trace_id}-{parent_span_id}-{flags}
- When service B receives a traceparent header, create a child span，包含parent_span_id from the header
- sampled flag: last byte 01 = sampled, 00 = not sampled
- Generate traceparent: format as 00-{trace_id}-{span_id}-01
- Trace tree depth = length of the longest parent->child chain

## 测试用例

### 1. Propagate trace context

Service B should extract trace context和create a child span.

输入：

```json
{"src":"service_a","dest":"service_b","body":{"type":"http_request","msg_id":1,"path":"/api/data","headers":{"traceparent":"00-trace123-span_a-01"}}}
```

期望输出：

```text
{"src": "service_b", "dest": "service_a", "body": {"type": "http_response", "in_reply_to": 1, "span": {"trace_id": "trace123", "span_id": "span_b", "parent_span_id": "span_a"}}}
```

### 2. Parse W3C traceparent header

Should parse traceparent into trace_id, parent_span_id,和sampled flag.

输入：

```json
{"src":"service","dest":"parser","body":{"type":"parse_traceparent","msg_id":1,"traceparent":"00-4bf92f3577b34da6a3ce929d0e0e4736-00f067aa0ba902b57-01"}}
```

期望输出：

```text
{"src": "parser", "dest": "service", "body": {"type": "parse_ok", "in_reply_to": 1, "trace_id": "4bf92f3577b34da6a3ce929d0e0e4736", "parent_span_id": "00f067aa0ba902b57", "sampled": true}}
```

## 参考资料

- [W3C Trace Context](https://www.w3.org/TR/trace-context/)：W3C standard用于distributed trace context propagation

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
