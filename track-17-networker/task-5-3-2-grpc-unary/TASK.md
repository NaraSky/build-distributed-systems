# Implement a gRPC Unary RPC Service

Website: <https://builddistributedsystem.com/tracks/networker/tasks/task-5-3-2-grpc-unary>

Track: 17. The Networker
Task order: 12
Short title: gRPC Unary
Difficulty: intermediate
Subtrack: gRPC and Protocol Buffers

## Problem

Implement a gRPC-style unary RPC service. In unary RPC, the client sends exactly one request and receives exactly one response.

gRPC message format on the wire:
`[compressed_flag: 1 byte][message_length: 4 bytes][protobuf_message]`

Implement a simple KeyValue service:

```json
Request:  {"type": "grpc_call", "msg_id": 1, "service": "KeyValue", "method": "Get", "request": {"key": "user:1"}}
Response: {"type": "grpc_call_ok", "in_reply_to": 1, "status": "OK", "response": {"key": "user:1", "value": "Alice", "found": true}}

Request:  {"type": "grpc_call", "msg_id": 2, "service": "KeyValue", "method": "Put", "request": {"key": "user:2", "value": "Bob"}}
Response: {"type": "grpc_call_ok", "in_reply_to": 2, "status": "OK", "response": {"written": true}}

Request:  {"type": "grpc_call", "msg_id": 3, "service": "KeyValue", "method": "Get", "request": {"key": "missing"}}
Response: {"type": "grpc_call_ok", "in_reply_to": 3, "status": "NOT_FOUND", "response": {"key": "missing", "found": false}}
```

## Concepts

- gRPC
- unary RPC
- HTTP/2
- service definition
- stub

## Hints

- Unary RPC: client sends one request, server sends one response
- gRPC uses HTTP/2 as its transport protocol
- Each RPC method maps to a (service, method) pair
- The request and response are protobuf-encoded messages
- gRPC adds a 5-byte header: 1 byte compressed flag + 4 bytes message length

## Test Cases

### 1. Put and Get a key

Input:

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"grpc_call","msg_id":2,"service":"KeyValue","method":"Put","request":{"key":"k1","value":"v1"}}}
{"src":"c1","dest":"n1","body":{"type":"grpc_call","msg_id":3,"service":"KeyValue","method":"Get","request":{"key":"k1"}}}
```

Expected output:

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
{"src": "n1", "dest": "c1", "body": {"type": "grpc_call_ok", "in_reply_to": 2, "status": "OK", "response": {"written": true}, "msg_id": 1}}
{"src": "n1", "dest": "c1", "body": {"type": "grpc_call_ok", "in_reply_to": 3, "status": "OK", "response": {"key": "k1", "value": "v1", "found": true}, "msg_id": 2}}
```

### 2. Get missing key returns NOT_FOUND

Input:

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"grpc_call","msg_id":2,"service":"KeyValue","method":"Get","request":{"key":"missing"}}}
```

Expected output:

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
{"src": "n1", "dest": "c1", "body": {"type": "grpc_call_ok", "in_reply_to": 2, "status": "NOT_FOUND", "response": {"key": "missing", "found": false}, "msg_id": 1}}
```

## Resources

- [gRPC Core Concepts](https://grpc.io/docs/what-is-grpc/core-concepts/): Overview of gRPC service definitions, RPC types, and lifecycle

## Java Starter

The matching local starter file is:

```text
src/main/java/Main.java
```
