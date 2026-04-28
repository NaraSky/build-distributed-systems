# Add a Connection Pool with Configurable Backlog

Website: <https://builddistributedsystem.com/tracks/networker/tasks/task-5-1-2-connection-pool>

Track: 17. The Networker
Task order: 2
Short title: Connection Pool
Difficulty: intermediate
Subtrack: TCP From Scratch

## Problem

Extend your TCP server to accept up to N concurrent connections. When N is exceeded, queue new connections in a backlog. If the backlog is also full, reject the connection.

Implement handlers:

```json
Request:  {"type": "pool_config", "msg_id": 1, "max_connections": 3, "backlog_size": 5}
Response: {"type": "pool_config_ok", "in_reply_to": 1}

Request:  {"type": "pool_connect", "msg_id": 2, "client_id": "c1"}
Response: {"type": "pool_connect_ok", "in_reply_to": 2, "status": "connected", "active": 1, "queued": 0}

Request:  {"type": "pool_connect", "msg_id": 5, "client_id": "c4"}
Response: {"type": "pool_connect_ok", "in_reply_to": 5, "status": "queued", "active": 3, "queued": 1}

Request:  {"type": "pool_disconnect", "msg_id": 6, "client_id": "c1"}
Response: {"type": "pool_disconnect_ok", "in_reply_to": 6, "promoted": "c4", "active": 3, "queued": 0}
```

## Concepts

- connection pool
- backlog
- concurrency
- resource management

## Hints

- Track the number of active connections with a counter
- When max connections is reached, either queue or reject new connections
- Use a configurable backlog size for queued connections
- Decrement the counter when a connection is closed
- Consider what happens when the queue itself is full

## Test Cases

### 1. Configure pool and connect

Input:

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"pool_config","msg_id":2,"max_connections":2,"backlog_size":3}}
{"src":"c1","dest":"n1","body":{"type":"pool_connect","msg_id":3,"client_id":"c1"}}
```

Expected output:

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
{"src": "n1", "dest": "c1", "body": {"type": "pool_config_ok", "in_reply_to": 2, "msg_id": 1}}
{"src": "n1", "dest": "c1", "body": {"type": "pool_connect_ok", "in_reply_to": 3, "status": "connected", "active": 1, "queued": 0, "msg_id": 2}}
```

### 2. Exceeding max connections queues

Third pool_connect_ok should show status: queued, active: 2, queued: 1.

Input:

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"pool_config","msg_id":2,"max_connections":2,"backlog_size":3}}
{"src":"c1","dest":"n1","body":{"type":"pool_connect","msg_id":3,"client_id":"c1"}}
{"src":"c1","dest":"n1","body":{"type":"pool_connect","msg_id":4,"client_id":"c2"}}
{"src":"c1","dest":"n1","body":{"type":"pool_connect","msg_id":5,"client_id":"c3"}}
```

Expected output:

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

## Resources

- [TCP Backlog and Connection Queuing](https://veithen.io/2014/01/01/how-tcp-backlog-works-in-linux.html): Deep dive into how TCP backlog works in Linux

## Java Starter

The matching local starter file is:

```text
src/main/java/Main.java
```
