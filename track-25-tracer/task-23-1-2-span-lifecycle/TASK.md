# Implement Span Lifecycle Management

Website: <https://builddistributedsystem.com/tracks/tracer/tasks/task-23-1-2-span-lifecycle>

Track: 25. The Tracer
Task order: 2
Short title: Span Lifecycle
Difficulty: intermediate
Subtrack: Distributed Tracing

## Problem

A span represents one operation within a trace: it has a name, start and end timestamps, status, and optionally events and links. The span kind identifies whether the operation is an incoming server call, an outgoing client call, or internal work.

Implement a node that manages span lifecycles:

```json
// Full lifecycle: create -> event -> end
{ "type": "create_span", "msg_id": 1, "name": "GET /api/users/123" }
{ "type": "span_event", "span_id": "span1", "event": "db.query" }
{ "type": "span_end", "span_id": "span1", "status": "OK" }
-> { "type": "span_complete",
    "span_id": "span1", "duration_us": 10000, "status": "OK" }

// Error during span -> ERROR status
{ "type": "create_span", "msg_id": 2, "name": "GET /api/users/999" }
{ "type": "span_error", "span_id": "span2", "error": "User not found" }
-> { "type": "span_complete",
    "span_id": "span2", "status": "ERROR", "error": "User not found" }

// CLIENT kind for outbound calls
{ "type": "create_span", "msg_id": 3,
  "name": "GET /api/data", "kind": "CLIENT" }
-> { "type": "span_created", "span_id": "span1", "kind": "CLIENT" }
```

## Concepts

- span lifecycle
- span kind
- span events
- span links
- duration

## Hints

- Span starts on create_span and ends on span_end; duration = end_time - start_time
- Default status is OK; span_error sets status=ERROR with the error message
- Span kind: SERVER for incoming requests, CLIENT for outbound calls to other services
- Span events are timestamped point-in-time annotations inside a span
- Span links connect related spans that are not in a direct parent-child relationship

## Test Cases

### 1. Span lifecycle progression

Span should track start to end and calculate duration.

Input:

```json
{"src":"service","dest":"tracer","body":{"type":"create_span","msg_id":1,"name":"GET /api/users/123"}}
{"type":"span_event","span_id":"span1","event":"db.query"}
{"type":"span_end","span_id":"span1","status":"OK"}
```

Expected output:

```text
{"src": "tracer", "dest": "service", "body": {"type": "span_complete", "span_id": "span1", "duration_us": 10000, "status": "OK"}}
```

### 2. Span with error status

span_error should set status=ERROR with the error message.

Input:

```json
{"src":"service","dest":"tracer","body":{"type":"create_span","msg_id":1,"name":"GET /api/users/999"}}
{"type":"span_error","span_id":"span2","error":"User not found"}
```

Expected output:

```text
{"src": "tracer", "dest": "service", "body": {"type": "span_complete", "span_id": "span2", "status": "ERROR", "error": "User not found"}}
```

## Resources

- [OpenTelemetry Trace Spec](https://opentelemetry.io/docs/concepts/signals/traces/): OpenTelemetry specification for spans and traces

## Java Starter

The matching local starter file is:

```text
src/main/java/Main.java
```
