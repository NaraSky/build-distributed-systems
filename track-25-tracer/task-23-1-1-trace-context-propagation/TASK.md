# Implement Distributed Trace Context Propagation

Website: <https://builddistributedsystem.com/tracks/tracer/tasks/task-23-1-1-trace-context-propagation>

Track: 25. The Tracer
Task order: 1
Short title: Trace Propagation
Difficulty: intermediate
Subtrack: Distributed Tracing

## Problem

Distributed tracing links spans from a single request as it flows through multiple services. Each service propagates the trace context (trace ID + parent span ID) in a header so every hop can be assembled into a single trace tree.

Implement a node that handles trace context operations:

```json
// Service B receives request with traceparent -> creates child span
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

## Concepts

- distributed tracing
- trace context
- W3C traceparent
- span
- trace tree

## Hints

- W3C traceparent format: 00-{trace_id}-{parent_span_id}-{flags}
- When service B receives a traceparent header, create a child span with parent_span_id from the header
- sampled flag: last byte 01 = sampled, 00 = not sampled
- Generate traceparent: format as 00-{trace_id}-{span_id}-01
- Trace tree depth = length of the longest parent->child chain

## Test Cases

### 1. Propagate trace context

Service B should extract trace context and create a child span.

Input:

```json
{"src":"service_a","dest":"service_b","body":{"type":"http_request","msg_id":1,"path":"/api/data","headers":{"traceparent":"00-trace123-span_a-01"}}}
```

Expected output:

```text
{"src": "service_b", "dest": "service_a", "body": {"type": "http_response", "in_reply_to": 1, "span": {"trace_id": "trace123", "span_id": "span_b", "parent_span_id": "span_a"}}}
```

### 2. Parse W3C traceparent header

Should parse traceparent into trace_id, parent_span_id, and sampled flag.

Input:

```json
{"src":"service","dest":"parser","body":{"type":"parse_traceparent","msg_id":1,"traceparent":"00-4bf92f3577b34da6a3ce929d0e0e4736-00f067aa0ba902b57-01"}}
```

Expected output:

```text
{"src": "parser", "dest": "service", "body": {"type": "parse_ok", "in_reply_to": 1, "trace_id": "4bf92f3577b34da6a3ce929d0e0e4736", "parent_span_id": "00f067aa0ba902b57", "sampled": true}}
```

## Resources

- [W3C Trace Context](https://www.w3.org/TR/trace-context/): W3C standard for distributed trace context propagation

## Java Starter

The matching local starter file is:

```text
src/main/java/Main.java
```
