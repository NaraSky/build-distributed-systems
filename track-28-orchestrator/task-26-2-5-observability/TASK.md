# Implement Service Mesh Observability

Website: <https://builddistributedsystem.com/tracks/orchestrator/tasks/task-26-2-5-observability>

Track: 28. The Orchestrator
Task order: 10
Short title: Observability
Difficulty: intermediate
Subtrack: Service Mesh

## Problem

Observability in a service mesh means collecting metrics, traces, and logs from every sidecar proxy automatically, without changing application code. The three pillars together let you understand what is happening and diagnose problems quickly.

Implement a node that handles all three observability signals:

```json
// Record a request metric (latency + status code)
{ "type": "record", "msg_id": 1,
  "service": "api", "duration_ms": 150, "status": 200 }
-> { "type": "metrics_recorded", "in_reply_to": 1,
    "service": "api", "request_count": 1 }

// Create a distributed trace with a span
{ "type": "trace", "msg_id": 2,
  "operation": "GET /api/users" }
-> { "type": "trace_created", "in_reply_to": 2,
    "trace_id": "<uuid>", "span_id": "<uuid>" }

// Query access logs by service
{ "type": "query", "msg_id": 3,
  "filter": {"source_service": "api", "target_service": "database"} }
-> { "type": "access_logs", "in_reply_to": 3,
    "logs": [{"source_service": "api", "target_service": "database", "count": 50}] }

// Generate service dependency graph
{ "type": "generate", "msg_id": 4 }
-> { "type": "service_graph", "in_reply_to": 4,
    "nodes": ["api", "database", "cache"],
    "edges": [{"source": "api", "target": "database", "request_count": 500}] }
```

## Concepts

- metrics
- distributed tracing
- access logs
- service graph
- golden signals

## Hints

- record stores one request metric: service name, duration_ms, and HTTP status code
- trace creates a trace with a unique trace_id and a span for the given operation
- query returns access logs filtered by source_service and/or target_service
- generate builds a service graph: nodes are service names, edges are (source, target, count) pairs
- request_count increments by 1 for every record call for that service

## Test Cases

### 1. Collect service metrics

Should record the metric and return the updated request count.

Input:

```json
{"src":"sidecar","dest":"metrics","body":{"type":"record","msg_id":1,"service":"api","duration_ms":150,"status":200}}
```

Expected output:

```text
{"type": "metrics_recorded", "in_reply_to": 1, "service": "api", "request_count": 1}
```

### 2. Create distributed trace

Should create a trace with unique trace_id and span_id.

Input:

```json
{"src":"service-a","dest":"tracer","body":{"type":"trace","msg_id":1,"operation":"GET /api/users"}}
```

Expected output:

```text
{"type": "trace_created", "in_reply_to": 1, "trace_id": ".*", "span_id": ".*"}
```

## Resources

- [Observability in a Service Mesh](https://istio.io/latest/docs/concepts/observability/): How Istio collects metrics, traces, and logs from sidecars

## Java Starter

The matching local starter file is:

```text
src/main/java/Main.java
```
