# Implement Vector Clocks

Website: <https://builddistributedsystem.com/tracks/timekeeper/tasks/task-4-3-1-vector-clock-impl>

Track: 16. The Timekeeper
Task order: 11
Short title: Vector Clock Impl
Difficulty: intermediate
Subtrack: Vector Clocks

## Problem

Vector clocks extend Lamport clocks by maintaining a vector of N integers (one per node) instead of a single counter. This lets you determine causal relationships between events across nodes.

Rules:
1. **Local event**: increment own slot: `vc[self] += 1`
2. **Send**: increment own slot, attach full vector to message
3. **Receive**: `vc[i] = max(vc[i], msg_vc[i])` for all i, then increment own slot

Implement vector clock handlers:

```json
Request:  {"type": "tick", "msg_id": 1}
Response: {"type": "tick_ok", "in_reply_to": 1, "clock": [1, 0, 0]}

Request:  {"type": "send_msg", "msg_id": 2, "dest": "n2", "payload": "hello"}
Response: {"type": "send_msg_ok", "in_reply_to": 2, "clock": [2, 0, 0]}

Request:  {"type": "recv_msg", "msg_id": 3, "from": "n2", "remote_clock": [0, 5, 0], "payload": "hi"}
Response: {"type": "recv_msg_ok", "in_reply_to": 3, "clock": [3, 5, 0]}

Request:  {"type": "get_clock", "msg_id": 4}
Response: {"type": "get_clock_ok", "in_reply_to": 4, "clock": [3, 5, 0]}
```

## Concepts

- vector clock
- causal ordering
- partial order
- distributed time

## Hints

- Each node maintains a vector of N integers, one slot per node in the cluster
- On any local event: increment your own slot
- On send: increment your own slot, attach the full vector to the message
- On receive: take element-wise max of local and received vectors, then increment own slot
- Initialize all slots to 0 on startup

## Test Cases

### 1. Tick increments own slot only

Input:

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1","n2","n3"]}}
{"src":"c1","dest":"n1","body":{"type":"tick","msg_id":2}}
{"src":"c1","dest":"n1","body":{"type":"tick","msg_id":3}}
{"src":"c1","dest":"n1","body":{"type":"get_clock","msg_id":4}}
```

Expected output:

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
{"src": "n1", "dest": "c1", "body": {"type": "tick_ok", "in_reply_to": 2, "clock": [1, 0, 0], "msg_id": 1}}
{"src": "n1", "dest": "c1", "body": {"type": "tick_ok", "in_reply_to": 3, "clock": [2, 0, 0], "msg_id": 2}}
{"src": "n1", "dest": "c1", "body": {"type": "get_clock_ok", "in_reply_to": 4, "clock": [2, 0, 0], "msg_id": 3}}
```

### 2. Receive merges vectors via element-wise max

Input:

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1","n2"]}}
{"src":"c1","dest":"n1","body":{"type":"tick","msg_id":2}}
{"src":"n2","dest":"n1","body":{"type":"recv_msg","msg_id":3,"from":"n2","remote_clock":[0,7],"payload":"hi"}}
{"src":"c1","dest":"n1","body":{"type":"get_clock","msg_id":4}}
```

Expected output:

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
{"src": "n1", "dest": "c1", "body": {"type": "tick_ok", "in_reply_to": 2, "clock": [1, 0], "msg_id": 1}}
{"src": "n1", "dest": "n2", "body": {"type": "recv_msg_ok", "in_reply_to": 3, "clock": [2, 7], "msg_id": 2}}
{"src": "n1", "dest": "c1", "body": {"type": "get_clock_ok", "in_reply_to": 4, "clock": [2, 7], "msg_id": 3}}
```

## Resources

- [Vector Clocks - Why It Is Hard to Tell the Time](https://riak.com/posts/technical/vector-clocks-revisited/index.html): Practical explanation of vector clocks with real-world examples

## Java Starter

The matching local starter file is:

```text
src/main/java/Main.java
```
