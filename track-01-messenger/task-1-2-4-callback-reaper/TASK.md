# Implement Callback Reaper for Leaked RPCs

Website: <https://builddistributedsystem.com/tracks/messenger/tasks/task-1-2-4-callback-reaper>

Track: 1. The Messenger
Task order: 9
Short title: Callback Reaper
Difficulty: intermediate
Subtrack: RPC and the Request-Response Model

## Problem

When a node sends an async RPC but the recipient crashes or the network drops the message, the callback stays in memory forever. This is a **resource leak** that can eventually consume all available memory.

Your task is to implement a **callback reaper** that:

1. Records the timestamp when each callback is registered
2. Periodically scans for callbacks older than a threshold (default: 2 seconds)
3. Removes expired callbacks and invokes them with a timeout error
4. Reports how many callbacks were reaped

Implement a `pending_count` message type that returns the number of currently pending callbacks:

```json
Request:  {"type": "pending_count", "msg_id": 1}
Response: {"type": "pending_count_ok", "in_reply_to": 1, "count": 5}
```

Also implement a `send_fire_forget` message type that sends an RPC without expecting a reply (to simulate leaked callbacks):

```json
Request:  {"type": "send_fire_forget", "msg_id": 1, "target": "n2", "payload": {"type": "echo", "echo": "lost"}}
Response: {"type": "send_fire_forget_ok", "in_reply_to": 1, "pending": 1}
```

## Concepts

- resource cleanup
- memory leaks
- periodic tasks
- garbage collection

## Hints

- Store the timestamp when each callback is registered
- Periodically scan the callbacks dictionary for expired entries
- Use time.time() to get the current timestamp in seconds
- A reaper interval of 500ms is a good starting point
- When reaping, invoke the callback with an error or None to signal timeout

## Test Cases

### 1. Pending count starts at zero

Input:

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"pending_count","msg_id":2}}
```

Expected output:

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
{"src": "n1", "dest": "c1", "body": {"type": "pending_count_ok", "count": 0, "in_reply_to": 2, "msg_id": 1}}
```

### 2. Fire-and-forget increases pending count

Input:

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1","n2"]}}
{"src":"c1","dest":"n1","body":{"type":"send_fire_forget","msg_id":2,"target":"n2","payload":{"type":"echo","echo":"lost"}}}
```

Expected output:

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
{"src": "n1", "dest": "n2", "body": {"type": "echo", "echo": "lost", "msg_id": 1}}
{"src": "n1", "dest": "c1", "body": {"type": "send_fire_forget_ok", "pending": 1, "in_reply_to": 2, "msg_id": 2}}
```

## Resources

- [Resource Leaks in Distributed Systems](https://sre.google/sre-book/handling-overload/): Google SRE book chapter on managing resource limits and overload

## Java Starter

The matching local starter file is:

```text
src/main/java/Main.java
```
