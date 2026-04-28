# 实现 Distributed Trace Collector

英文标题：Implement Distributed Trace Collector
网页：<https://builddistributedsystem.com/tracks/tracer/tasks/task-23-1-3-trace-collector>

课程：25. 追踪器：可观测性
任务序号：3
短标题：Trace Collector
难度：intermediate
子主题：Distributed Tracing

## 中文导读

本题要求你完成 `实现 Distributed Trace Collector`。

重点关注：`trace collector`、`span aggregation`、`trace sampling`、`late spans`、`trace queries`。

建议先按提示逐步实现：Group spans by trace_id; emit trace_complete when a trace has received all its spans。

协议字段、消息类型、输入输出格式请以本文件中的代码块和测试用例为准。

## 题目说明

A trace collector receives spans from many services, groups them by trace ID,和stores the assembled traces. It also applies sampling to reduce 存储 volume和gracefully handles spans that arrive after a trace was already closed.

Implement a 节点 that manages span collection和trace assembly:

```JSON
// Spans from two services assembled into one trace
{ "type": "span", "trace_id": "t1", "span_id": "s1", "service": "A" }
{ "type": "span", "trace_id": "t1", "span_id": "s2", "service": "B",
  "parent_span_id": "s1" }
-> { "type": "trace_complete", "trace_id": "t1", "span_count": 2 }

// 1% sampling: reject most traces
{ "type": "span", "trace_id": "t2", "service": "fast" }
(sampling_rate: 0.01)
-> { "type": "span_accepted",
    "sampled": false, "reason": "Trace not sampled (1% rate)" }

// Query traces by service
{ "type": "query_traces", "msg_id": 1,
  "service": "service-a", "time_range": "1h" }
-> { "type": "query_results", "in_reply_to": 1,
    "traces": 125, "avg_duration_ms": 45 }
```

Late spans用于a completed trace return `"action": "update_trace"` rather than being dropped.

## 涉及概念

- `trace collector`
- `span aggregation`
- `trace sampling`
- `late spans`
- `trace queries`

## 实现提示

- Group spans by trace_id; emit trace_complete when a trace has received all its spans
- Sampling: hash(trace_id) % 100 < (sampling_rate * 100) to decide consistently per trace
- query_traces filters by service和returns span count和average duration
- Late spans用于an already-completed trace should update it rather than be dropped
- span_count increments，包含each new span用于the same trace_id

## 测试用例

### 1. Aggregate spans into traces

Same trace_id spans should be grouped和trace marked complete.

输入：

```json
{"src":"service_a","dest":"collector","body":{"type":"span","trace_id":"t1","span_id":"s1","service":"A"}}
{"src":"service_b","dest":"collector","body":{"type":"span","trace_id":"t1","span_id":"s2","service":"B","parent_span_id":"s1"}}
```

期望输出：

```text
{"type": "trace_complete", "trace_id": "t1", "span_count": 2}
```

### 2. Trace sampling

At 1% sampling rate, this trace should not be sampled.

输入：

```json
{"src":"service","dest":"collector","body":{"type":"span","trace_id":"t2","span_id":"s3","service":"fast"},"sampling_rate":0.01}
```

期望输出：

```text
{"type": "span_accepted", "sampled": false, "reason": "Trace not sampled (1% rate)"}
```

## 参考资料

- [OpenTelemetry Collector](https://opentelemetry.io/docs/collector/)：How the OTel Collector receives, processes,和exports telemetry

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
