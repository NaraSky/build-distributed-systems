# Build gRPC Interceptors for Logging, Auth, and Rate Limiting

Website: <https://builddistributedsystem.com/tracks/networker/tasks/task-5-3-4-grpc-interceptors>

Track: 17. The Networker
Task order: 14
Short title: gRPC Interceptors
Difficulty: advanced
Subtrack: gRPC and Protocol Buffers

## Problem

Build a gRPC interceptor pipeline. Interceptors are middleware that wrap gRPC handler calls, running logic before and after the actual service method.

Interceptor chain: `logging -> auth -> rate_limit -> handler`

Implement handlers:

```json
Request:  {"type": "grpc_call", "msg_id": 1, "service": "KeyValue", "method": "Get", "request": {"key": "k1"}, "metadata": {"authorization": "Bearer valid_token"}}
Response: {"type": "grpc_call_ok", "in_reply_to": 1, "status": "OK", "interceptors_applied": ["logging", "auth", "rate_limit"], "response": {"key": "k1", "value": "v1", "found": true}}

Request:  {"type": "grpc_call", "msg_id": 2, "service": "KeyValue", "method": "Get", "request": {"key": "k1"}, "metadata": {}}
Response: {"type": "grpc_call_ok", "in_reply_to": 2, "status": "UNAUTHENTICATED", "interceptor_failed": "auth"}

Request:  {"type": "grpc_interceptor_stats", "msg_id": 3}
Response: {"type": "grpc_interceptor_stats_ok", "in_reply_to": 3, "stats": {
    "total_requests": 2, "auth_failures": 1, "rate_limited": 0
}}
```

## Concepts

- interceptor
- middleware
- authentication
- rate limiting
- request pipeline

## Hints

- Interceptors are middleware for gRPC calls, similar to HTTP middleware
- They run before and after the actual handler
- Chain multiple interceptors: logging -> auth -> rate_limit -> handler
- Auth interceptor checks metadata for a valid token
- Rate limiter uses a token bucket per client IP

## Test Cases

### 1. Authenticated request passes all interceptors

grpc_call_ok with status OK and interceptors_applied containing all three interceptors.

Input:

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"grpc_call","msg_id":2,"service":"KeyValue","method":"Put","request":{"key":"k1","value":"v1"},"metadata":{"authorization":"Bearer valid_token"}}}
```

Expected output:

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

### 2. Missing auth token fails at auth interceptor

Input:

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"grpc_call","msg_id":2,"service":"KeyValue","method":"Get","request":{"key":"k1"},"metadata":{}}}
```

Expected output:

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
{"src": "n1", "dest": "c1", "body": {"type": "grpc_call_ok", "in_reply_to": 2, "status": "UNAUTHENTICATED", "interceptor_failed": "auth", "msg_id": 1}}
```

## Resources

- [gRPC Interceptors in Go](https://grpc.io/docs/guides/interceptors/): How to implement client and server interceptors for gRPC

## Java Starter

The matching local starter file is:

```text
src/main/java/Main.java
```
