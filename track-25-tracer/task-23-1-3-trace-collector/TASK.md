# Implement Distributed Trace Collector

Website: <https://builddistributedsystem.com/tracks/tracer/tasks/task-23-1-3-trace-collector>

Track: 25. The Tracer
Task order: 3
Short title: Trace Collector
Difficulty: intermediate
Subtrack: Distributed Tracing

## Problem

A trace collector receives spans from many services, groups them by trace ID, and stores the assembled traces. It also applies sampling to reduce storage volume and gracefully handles spans that arrive after a trace was already closed.

Implement a node that manages span collection and trace assembly:

```json
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

Late spans for a completed trace return `"action": "update_trace"` rather than being dropped.

## Concepts

- trace collector
- span aggregation
- trace sampling
- late spans
- trace queries

## Hints

- Group spans by trace_id; emit trace_complete when a trace has received all its spans
- Sampling: hash(trace_id) % 100 < (sampling_rate * 100) to decide consistently per trace
- query_traces filters by service and returns span count and average duration
- Late spans for an already-completed trace should update it rather than be dropped
- span_count increments with each new span for the same trace_id

## Test Cases

### 1. Aggregate spans into traces

Same trace_id spans should be grouped and trace marked complete.

Input:

```json
{"src":"service_a","dest":"collector","body":{"type":"span","trace_id":"t1","span_id":"s1","service":"A"}}
{"src":"service_b","dest":"collector","body":{"type":"span","trace_id":"t1","span_id":"s2","service":"B","parent_span_id":"s1"}}
```

Expected output:

```text
{"type": "trace_complete", "trace_id": "t1", "span_count": 2}
```

### 2. Trace sampling

At 1% sampling rate, this trace should not be sampled.

Input:

```json
{"src":"service","dest":"collector","body":{"type":"span","trace_id":"t2","span_id":"s3","service":"fast"},"sampling_rate":0.01}
```

Expected output:

```text
{"type": "span_accepted", "sampled": false, "reason": "Trace not sampled (1% rate)"}
```

## Resources

- [OpenTelemetry Collector](https://opentelemetry.io/docs/collector/): How the OTel Collector receives, processes, and exports telemetry

## Java Starter

The matching local starter file is:

```text
src/main/java/Main.java
```
