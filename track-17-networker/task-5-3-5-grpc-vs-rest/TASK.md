# Compare gRPC vs REST: Latency, Size, and DX

Website: <https://builddistributedsystem.com/tracks/networker/tasks/task-5-3-5-grpc-vs-rest>

Track: 17. The Networker
Task order: 15
Short title: gRPC vs REST
Difficulty: intermediate
Subtrack: gRPC and Protocol Buffers

## Problem

Compare gRPC and REST across multiple dimensions. Build both a REST-style and gRPC-style endpoint for the same service and measure the differences.

Implement comparison handlers:

```json
Request:  {"type": "rest_call", "msg_id": 1, "method": "GET", "path": "/api/users/1"}
Response: {"type": "rest_call_ok", "in_reply_to": 1, "status": 200, "body": {"id": 1, "name": "Alice"}, "content_type": "application/json", "size_bytes": 28}

Request:  {"type": "grpc_call", "msg_id": 2, "service": "Users", "method": "GetUser", "request": {"id": 1}}
Response: {"type": "grpc_call_ok", "in_reply_to": 2, "status": "OK", "response": {"id": 1, "name": "Alice"}, "size_bytes": 9}

Request:  {"type": "compare_protocols", "msg_id": 3, "num_calls": 100}
Response: {"type": "compare_protocols_ok", "in_reply_to": 3, "comparison": {
    "rest": {"avg_size_bytes": 28, "avg_latency_us": 500, "browser_support": true, "code_gen": false},
    "grpc": {"avg_size_bytes": 9, "avg_latency_us": 120, "browser_support": false, "code_gen": true},
    "size_reduction_pct": 67.9,
    "latency_reduction_pct": 76.0
}}
```

## Concepts

- REST
- gRPC
- HTTP/2
- JSON vs protobuf
- developer experience

## Hints

- gRPC uses HTTP/2 (multiplexing, header compression) while REST typically uses HTTP/1.1
- Protobuf encoding is 3-10x smaller than JSON for the same data
- gRPC has built-in code generation; REST requires manual client libraries
- REST is more browser-friendly; gRPC requires gRPC-Web for browser clients
- Compare on: serialization size, latency, tooling, debugging ease

## Test Cases

### 1. REST call returns JSON

rest_call_ok with status 200, JSON body, and content_type application/json.

Input:

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"rest_call","msg_id":2,"method":"GET","path":"/api/users/1"}}
```

Expected output:

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

### 2. gRPC call returns protobuf-sized response

grpc_call_ok should show size_bytes significantly smaller than equivalent REST response.

Input:

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"grpc_call","msg_id":2,"service":"Users","method":"GetUser","request":{"id":1}}}
```

Expected output:

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

## Resources

- [gRPC vs REST Performance Comparison](https://cloud.google.com/blog/products/api-management/understanding-grpc-openapi-and-rest-and-when-to-use-them): Google Cloud blog comparing gRPC, REST, and OpenAPI

## Java Starter

The matching local starter file is:

```text
src/main/java/Main.java
```
