# Implement End-to-End Distributed Tracing System

Website: <https://builddistributedsystem.com/tracks/tracer/tasks/task-23-1-5-distributed-tracing>

Track: 25. The Tracer
Task order: 5
Short title: End-to-End Tracing
Difficulty: advanced
Subtrack: Distributed Tracing

## Problem

Individual span operations give you the building blocks. End-to-end tracing connects them: every service creates and propagates spans, logs are correlated with trace IDs, and you get complete visibility across the entire call chain without manual wiring.

Implement a node that supports full distributed tracing infrastructure:

```json
// Auto-instrument three services, then handle a request
{ "type": "instrument_service", "msg_id": 1,
  "services": ["web","api","db"], "auto": true }
{ "type": "http_request", "path": "/api/users/123" }
-> { "type": "trace_complete",
    "trace_id": "<uuid>",
    "services": ["web","api","db"], "span_count": 3 }

// Attach trace_id to logs for correlation
{ "type": "log", "msg_id": 3,
  "message": "Processing request", "trace_id": "abc123" }
{ "type": "search_logs", "msg_id": 4, "trace_id": "abc123" }
-> { "type": "search_results", "in_reply_to": 4,
    "logs": [{"service":"service","message":"Processing request",
               "trace_id":"abc123"}] }
```

## Concepts

- auto-instrumentation
- manual instrumentation
- log-trace correlation
- service mesh tracing

## Hints

- Auto-instrumentation: wrap each service with a tracing interceptor that creates spans automatically
- Manual: tracer.startSpan(name) -> do work -> span.end() (or span.recordException(e) on error)
- Log-trace correlation: attach trace_id to every log entry; index logs by trace_id
- Service mesh sidecar: injects tracing at the network layer without application code changes
- span_count = number of services instrumented in the call chain

## Test Cases

### 1. Instrument multiple services

Auto-instrumentation should create one span per service in the call chain.

Input:

```json
{"src":"instrumentor","dest":"services","body":{"type":"instrument_service","msg_id":1,"services":["web","api","db"],"auto":true}}
{"src":"user","dest":"web","body":{"type":"http_request","path":"/api/users/123"}}
```

Expected output:

```text
{"type": "trace_complete", "trace_id": ".*", "services": ["web", "api", "db"], "span_count": 3}
```

### 2. Manual instrumentation

Manual instrumentation should create one span with proper lifecycle handling.

Input:

```json
{"src":"developer","dest":"code","body":{"type":"manual_instrument","msg_id":1,"code":"async function process() { const span = tracer.startSpan('process'); try { await work(); span.end(); } catch(e) { span.recordException(e); throw; } }"}}
```

Expected output:

```text
{"type": "instrumentation_ok", "in_reply_to": 1, "spans_created": 1}
```

## Resources

- [OpenTelemetry](https://opentelemetry.io/docs/): Vendor-neutral standard for distributed tracing, metrics, and logs

## Java Starter

The matching local starter file is:

```text
src/main/java/Main.java
```
