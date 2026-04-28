# Add Message Envelope Logger with Timestamps

Website: <https://builddistributedsystem.com/tracks/messenger/tasks/task-1-3-2-envelope-logger>

Track: 1. The Messenger
Task order: 12
Short title: Envelope Logger
Difficulty: intermediate
Subtrack: The Protocol Beneath

## Problem

In production distributed systems, **message tracing** is critical for debugging. When something goes wrong, you need to answer: "What messages did this node send and receive, and when?"

Your task is to add a message envelope logger to your node:

1. Every received message should be logged with: timestamp, direction (RECV), src, dest, body type
2. Every sent message should be logged with: timestamp, direction (SENT), src, dest, body type
3. Logs are stored in an in-memory buffer (most recent 100 entries)
4. Implement a `get_log` message type that returns the log entries

```json
Request:  {"type": "get_log", "msg_id": 1, "count": 5}
Response: {"type": "get_log_ok", "in_reply_to": 1, "entries": [
    {"ts": "2024-01-01T00:00:00", "dir": "RECV", "src": "c0", "dest": "n1", "msg_type": "init"},
    {"ts": "2024-01-01T00:00:00", "dir": "SENT", "src": "n1", "dest": "c0", "msg_type": "init_ok"}
]}
```

The `count` field specifies how many recent entries to return. If fewer entries exist, return all of them.

## Concepts

- logging
- observability
- message tracing
- timestamps

## Hints

- Log each message as a single line with a timestamp prefix
- Include direction (SENT or RECV), src, dest, and body type
- Use ISO 8601 format for timestamps
- Log to stderr so it does not interfere with stdout message passing
- Implement a get_log message type that returns recent log entries

## Test Cases

### 1. Init and echo produce correct output

Input:

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"echo","msg_id":2,"echo":"log-test"}}
```

Expected output:

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
{"src": "n1", "dest": "c1", "body": {"type": "echo_ok", "echo": "log-test", "in_reply_to": 2, "msg_id": 1}}
```

### 2. Get log returns entries after init

The second output line is a get_log_ok with entries containing RECV init, SENT init_ok, and RECV get_log. Exact timestamps vary so only structure is checked.

Input:

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"get_log","msg_id":2,"count":10}}
```

Expected output:

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

## Resources

- [Distributed Tracing](https://opentelemetry.io/docs/concepts/observability-primer/): OpenTelemetry primer on observability in distributed systems

## Java Starter

The matching local starter file is:

```text
src/main/java/Main.java
```
