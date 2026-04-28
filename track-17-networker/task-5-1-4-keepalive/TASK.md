# Implement Application-Level TCP Keep-Alive

Website: <https://builddistributedsystem.com/tracks/networker/tasks/task-5-1-4-keepalive>

Track: 17. The Networker
Task order: 4
Short title: TCP Keep-Alive
Difficulty: intermediate
Subtrack: TCP From Scratch

## Problem

Implement application-level TCP keep-alive detection. If a client goes silent for more than 30 seconds, detect it and close the connection. Use periodic ping messages instead of OS-level keep-alive.

Implement handlers:

```json
Request:  {"type": "ka_register", "msg_id": 1, "client_id": "c1", "timeout_ms": 30000, "ping_interval_ms": 10000}
Response: {"type": "ka_register_ok", "in_reply_to": 1}

Request:  {"type": "ka_heartbeat", "msg_id": 2, "client_id": "c1"}
Response: {"type": "ka_heartbeat_ok", "in_reply_to": 2, "last_seen_ms_ago": 0}

Request:  {"type": "ka_check", "msg_id": 3, "current_time_ms": 45000}
Response: {"type": "ka_check_ok", "in_reply_to": 3, "expired": ["c1"], "active": ["c2"]}

Request:  {"type": "ka_status", "msg_id": 4}
Response: {"type": "ka_status_ok", "in_reply_to": 4, "connections": [
    {"client_id": "c2", "last_seen_ms_ago": 5000, "status": "active"}
]}
```

## Concepts

- keep-alive
- heartbeat
- connection health
- idle detection

## Hints

- Send periodic ping messages to detect silent client failures
- Track the last activity timestamp for each connection
- If no activity for > 30s, send a ping. If no pong within 5s, close the connection
- Do not rely on OS-level keep-alive; implement at the application layer
- Maintain a connection state table with last_seen timestamps

## Test Cases

### 1. Register a client for keep-alive

Input:

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"ka_register","msg_id":2,"client_id":"c1","timeout_ms":30000,"ping_interval_ms":10000}}
```

Expected output:

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
{"src": "n1", "dest": "c1", "body": {"type": "ka_register_ok", "in_reply_to": 2, "msg_id": 1}}
```

### 2. Heartbeat resets last_seen

Input:

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"ka_register","msg_id":2,"client_id":"c1","timeout_ms":30000,"ping_interval_ms":10000}}
{"src":"c1","dest":"n1","body":{"type":"ka_heartbeat","msg_id":3,"client_id":"c1"}}
```

Expected output:

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
{"src": "n1", "dest": "c1", "body": {"type": "ka_register_ok", "in_reply_to": 2, "msg_id": 1}}
{"src": "n1", "dest": "c1", "body": {"type": "ka_heartbeat_ok", "in_reply_to": 3, "last_seen_ms_ago": 0, "msg_id": 2}}
```

## Resources

- [TCP Keep-Alive in Detail](https://tldp.org/HOWTO/TCP-Keepalive-HOWTO/): Understanding TCP keep-alive at both OS and application levels

## Java Starter

The matching local starter file is:

```text
src/main/java/Main.java
```
