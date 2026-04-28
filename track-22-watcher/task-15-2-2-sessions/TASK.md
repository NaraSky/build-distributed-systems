# Implement Client Session Management

Website: <https://builddistributedsystem.com/tracks/watcher/tasks/task-15-2-2-sessions>

Track: 22. The Watcher
Task order: 7
Short title: Sessions
Difficulty: intermediate
Subtrack: Watches and Sessions

## Problem

Every ZooKeeper client operates within a session. The session tracks the client's liveness and is the basis for ephemeral node lifetime and watch delivery.

**Session lifecycle**:
1. Client connects and receives a unique session ID
2. Client sends heartbeats (pings) every `tickTime` (default 2 seconds)
3. If the server misses heartbeats for `sessionTimeout` (default 10 seconds), the session expires
4. On expiry: ephemeral nodes created by this session are deleted, watches are removed
5. If the client reconnects before timeout, the session is preserved with all its state

```json
Request:  {"type": "session_create", "msg_id": 1, "timeout_ms": 10000}
Response: {"type": "session_create_ok", "in_reply_to": 1, "session_id": "s-001", "timeout_ms": 10000}

Request:  {"type": "session_heartbeat", "msg_id": 2, "session_id": "s-001"}
Response: {"type": "session_heartbeat_ok", "in_reply_to": 2, "session_id": "s-001", "remaining_ms": 10000}
```

## Concepts

- session
- heartbeat
- session timeout
- session expiry
- reconnection

## Hints

- Each client is assigned a session ID on connection
- Client sends heartbeats every tick_time (2 seconds default)
- If the server misses heartbeats for session_timeout (10s default), the session expires
- On session expiry: all ephemeral nodes are deleted, all watches are removed
- Clients can reconnect within the timeout window without losing their session

## Test Cases

### 1. Create session returns session ID

session_create_ok should include a unique session_id and the timeout_ms.

Input:

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"session_create","msg_id":2,"timeout_ms":10000}}
```

Expected output:

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

### 2. Heartbeat extends session

session_heartbeat_ok should show remaining_ms > 0.

Input:

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"session_create","msg_id":2,"timeout_ms":10000}}
{"src":"c1","dest":"n1","body":{"type":"session_heartbeat","msg_id":3,"session_id":"s-001"}}
```

Expected output:

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

## Resources

- [ZooKeeper Sessions](https://zookeeper.apache.org/doc/current/zookeeperProgrammers.html#ch_zkSessions): ZooKeeper documentation on session management and heartbeats

## Java Starter

The matching local starter file is:

```text
src/main/java/Main.java
```
