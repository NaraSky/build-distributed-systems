# Implement gRPC Server and Bidirectional Streaming

Website: <https://builddistributedsystem.com/tracks/networker/tasks/task-5-3-3-grpc-streaming>

Track: 17. The Networker
Task order: 13
Short title: gRPC Streaming
Difficulty: advanced
Subtrack: gRPC and Protocol Buffers

## Problem

Implement gRPC streaming RPCs:

1. **Server streaming**: Client sends one request, server sends a stream of responses
2. **Bidirectional streaming**: Both sides send streams of messages concurrently

Use a log-watching service as the example:

```json
Request:  {"type": "grpc_server_stream", "msg_id": 1, "service": "LogWatcher", "method": "WatchLogs", "request": {"filter": "ERROR", "limit": 3}}
Response: [
    {"type": "grpc_stream_msg", "in_reply_to": 1, "seq": 1, "data": {"level": "ERROR", "msg": "disk full"}},
    {"type": "grpc_stream_msg", "in_reply_to": 1, "seq": 2, "data": {"level": "ERROR", "msg": "connection reset"}},
    {"type": "grpc_stream_msg", "in_reply_to": 1, "seq": 3, "data": {"level": "ERROR", "msg": "timeout"}},
    {"type": "grpc_stream_end", "in_reply_to": 1, "status": "OK", "count": 3}
]

Request:  {"type": "grpc_bidi_stream_open", "msg_id": 2, "service": "Chat", "method": "BiDiChat"}
Response: {"type": "grpc_bidi_stream_open_ok", "in_reply_to": 2, "stream_id": "s1"}

Request:  {"type": "grpc_bidi_stream_send", "msg_id": 3, "stream_id": "s1", "data": {"text": "hello"}}
Response: {"type": "grpc_bidi_stream_recv", "in_reply_to": 3, "data": {"text": "echo: hello"}}
```

## Concepts

- server streaming
- bidirectional streaming
- HTTP/2 streams
- flow control

## Hints

- Server streaming: client sends one request, server sends multiple responses
- Bidirectional streaming: both sides send multiple messages over the same connection
- Each message in the stream uses the same gRPC framing (compressed flag + length)
- The server signals end-of-stream with gRPC trailers (grpc-status)
- Track the stream state: OPEN, HALF_CLOSED, CLOSED

## Test Cases

### 1. Server streaming returns multiple messages

Should receive 2 grpc_stream_msg responses followed by grpc_stream_end with count: 2.

Input:

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"grpc_server_stream","msg_id":2,"service":"LogWatcher","method":"WatchLogs","request":{"filter":"ERROR","limit":2}}}
```

Expected output:

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

### 2. Bidi stream open and send

grpc_bidi_stream_open_ok should return a stream_id. grpc_bidi_stream_recv should echo the message.

Input:

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"grpc_bidi_stream_open","msg_id":2,"service":"Chat","method":"BiDiChat"}}
{"src":"c1","dest":"n1","body":{"type":"grpc_bidi_stream_send","msg_id":3,"stream_id":"s1","data":{"text":"hello"}}}
```

Expected output:

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

## Resources

- [gRPC Streaming](https://grpc.io/docs/what-is-grpc/core-concepts/#server-streaming-rpc): gRPC server streaming and bidirectional streaming RPC types

## Java Starter

The matching local starter file is:

```text
src/main/java/Main.java
```
