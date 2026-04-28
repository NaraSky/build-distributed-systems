# Implement Trace Analysis and Insights

Website: <https://builddistributedsystem.com/tracks/tracer/tasks/task-23-1-4-trace-analysis>

Track: 25. The Tracer
Task order: 4
Short title: Trace Analysis
Difficulty: advanced
Subtrack: Distributed Tracing

## Problem

Raw traces tell you what happened. Trace analysis tells you why it was slow and where errors are concentrated. By aggregating many traces, you surface bottlenecks, error hot-spots, service dependencies, and latency outliers.

Implement a node that analyses trace data and surfaces insights:

```json
// Identify bottleneck (db takes 94% of trace time)
{ "type": "analyze_traces", "msg_id": 1,
  "traces": [{"trace_id":"t1","duration_ms":5000,
               "spans":[{"service":"web","duration":100},
                         {"service":"api","duration":200},
                         {"service":"db","duration":4700}]}] }
-> { "type": "insights", "in_reply_to": 1,
    "bottlenecks": ["db"], "critical_path": "web->api->db",
    "optimization_suggestion": "Add caching for database queries" }

// Error rate per service
{ "type": "analyze_errors", "msg_id": 2,
  "traces": [{"trace_id":"t1","has_error":true,"service":"payment-service"},
              {"trace_id":"t2","has_error":false},
              {"trace_id":"t3","has_error":true,"service":"payment-service"}] }
-> { "type": "error_analysis", "in_reply_to": 2,
    "error_rate_by_service": {"payment-service": "66.7%"},
    "total_errors": 2 }
```

## Concepts

- bottleneck detection
- critical path
- error rate
- service map
- anomaly detection

## Hints

- Bottleneck: the span with the largest share of total trace duration
- Critical path: the chain of spans from root to leaf with the maximum total duration
- Error rate per service = error traces for that service / total traces for that service
- Service map edges: parent span service -> child span service
- Anomaly: trace duration > N * baseline p50 (e.g. 100x = high severity)

## Test Cases

### 1. Performance analysis

db takes 94% of trace duration and should be identified as bottleneck.

Input:

```json
{"src":"analyzer","dest":"insights","body":{"type":"analyze_traces","msg_id":1,"time_range":"1h","traces":[{"trace_id":"t1","duration_ms":5000,"spans":[{"service":"web","duration":100},{"service":"api","duration":200},{"service":"db","duration":4700}]}]}}
```

Expected output:

```text
{"type": "insights", "in_reply_to": 1, "bottlenecks": ["db"], "critical_path": "web->api->db", "optimization_suggestion": "Add caching for database queries"}
```

### 2. Error rate analysis

payment-service is in 2/3 error traces = 66.7% error rate.

Input:

```json
{"src":"analyzer","dest":"insights","body":{"type":"analyze_errors","msg_id":1,"traces":[{"trace_id":"t1","has_error":true,"service":"payment-service"},{"trace_id":"t2","has_error":false},{"trace_id":"t3","has_error":true,"service":"payment-service"}]}}
```

Expected output:

```text
{"type": "error_analysis", "in_reply_to": 1, "error_rate_by_service": {"payment-service": "66.7%"}, "total_errors": 2}
```

## Resources

- [Distributed Tracing with Jaeger](https://www.jaegertracing.io/docs/latest/): Jaeger docs on trace analysis and root cause investigation

## Java Starter

The matching local starter file is:

```text
src/main/java/Main.java
```
