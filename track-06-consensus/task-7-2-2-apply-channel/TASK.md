# Implement the Apply Channel for State Machine

Website: <https://builddistributedsystem.com/tracks/consensus/tasks/task-7-2-2-apply-channel>

Track: 6. The Consensus
Task order: 7
Short title: Apply Channel
Difficulty: intermediate
Subtrack: Commitment and Application

## Problem

Implement an apply channel that feeds committed log entries to the state machine. The state machine is a simple key-value store that processes `Put`, `Get`, and `Delete` commands.

```json
Request:  {"type": "apply_entries", "msg_id": 1, "entries": [
    {"index": 1, "term": 1, "command": {"op": "put", "key": "x", "value": "1"}},
    {"index": 2, "term": 1, "command": {"op": "put", "key": "y", "value": "2"}},
    {"index": 3, "term": 1, "command": {"op": "get", "key": "x"}}
]}
Response: {"type": "apply_entries_ok", "in_reply_to": 1, "results": [
    {"index": 1, "result": "ok"},
    {"index": 2, "result": "ok"},
    {"index": 3, "result": "1"}
], "last_applied": 3}

Request:  {"type": "get_state", "msg_id": 2}
Response: {"type": "get_state_ok", "in_reply_to": 2, "state": {"x": "1", "y": "2"}, "last_applied": 3}
```

## Concepts

- apply channel
- state machine
- committed entries
- deterministic replay

## Hints

- Committed entries flow into an apply channel in order
- The state machine reads from the channel and applies commands sequentially
- Applied entries must never be re-applied (track lastApplied index)
- The state machine must be deterministic: same commands = same state
- Commands flow: client -> leader log -> replicated -> committed -> applied

## Test Cases

### 1. Apply put entries builds state

get_state_ok should show state: {"x": "hello"}, last_applied: 1.

Input:

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"apply_entries","msg_id":2,"entries":[{"index":1,"term":1,"command":{"op":"put","key":"x","value":"hello"}}]}}
{"src":"c1","dest":"n1","body":{"type":"get_state","msg_id":3}}
```

Expected output:

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

### 2. Apply get returns current value

apply_entries_ok results: index 1 result: ok, index 2 result: "42".

Input:

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"apply_entries","msg_id":2,"entries":[{"index":1,"term":1,"command":{"op":"put","key":"x","value":"42"}},{"index":2,"term":1,"command":{"op":"get","key":"x"}}]}}
```

Expected output:

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

## Resources

- [State Machine Replication](https://en.wikipedia.org/wiki/State_machine_replication): How replicated state machines process deterministic commands from a log

## Java Starter

The matching local starter file is:

```text
src/main/java/Main.java
```
