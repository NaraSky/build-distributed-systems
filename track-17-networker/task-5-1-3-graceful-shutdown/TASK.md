# Implement Graceful Shutdown with In-Flight Drain

Website: <https://builddistributedsystem.com/tracks/networker/tasks/task-5-1-3-graceful-shutdown>

Track: 17. The Networker
Task order: 3
Short title: Graceful Shutdown
Difficulty: intermediate
Subtrack: TCP From Scratch

## Problem

Implement graceful shutdown: when the server receives a shutdown signal, it should drain all in-flight requests before closing sockets. New connections are rejected during draining.

Implement handlers:

```json
Request:  {"type": "tcp_request", "msg_id": 1, "data": "process_this", "latency_ms": 500}
Response: {"type": "tcp_request_ok", "in_reply_to": 1, "result": "processed", "duration_ms": 500}

Request:  {"type": "tcp_shutdown", "msg_id": 2, "drain_timeout_ms": 5000}
Response: {"type": "tcp_shutdown_ok", "in_reply_to": 2, "status": "draining", "in_flight": 2}

Request:  {"type": "tcp_request", "msg_id": 3, "data": "new_request", "latency_ms": 100}
Response: {"type": "tcp_request_error", "in_reply_to": 3, "error": "server_shutting_down"}

Request:  {"type": "tcp_drain_status", "msg_id": 4}
Response: {"type": "tcp_drain_status_ok", "in_reply_to": 4, "status": "drained", "remaining": 0, "took_ms": 500}
```

## Concepts

- graceful shutdown
- drain
- in-flight requests
- connection lifecycle

## Hints

- On shutdown signal, stop accepting new connections immediately
- Wait for all in-flight requests to complete before closing sockets
- Track the number of in-flight requests with a counter
- Set a maximum drain timeout: force-close after N seconds
- Test by sending requests and initiating shutdown mid-flight

## Test Cases

### 1. Normal request processing

Input:

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"tcp_request","msg_id":2,"data":"hello","latency_ms":0}}
```

Expected output:

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
{"src": "n1", "dest": "c1", "body": {"type": "tcp_request_ok", "in_reply_to": 2, "result": "processed", "duration_ms": 0, "msg_id": 1}}
```

### 2. Shutdown starts drain

Input:

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"tcp_shutdown","msg_id":2,"drain_timeout_ms":5000}}
```

Expected output:

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
{"src": "n1", "dest": "c1", "body": {"type": "tcp_shutdown_ok", "in_reply_to": 2, "status": "draining", "in_flight": 0, "msg_id": 1}}
```

## Resources

- [Graceful Shutdown in Go](https://pkg.go.dev/net/http#Server.Shutdown): How Go standard library implements graceful HTTP server shutdown

## Java Starter

The matching local starter file is:

```text
src/main/java/Main.java
```
