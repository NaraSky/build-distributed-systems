# Build a Causal-Order Chat System

Website: <https://builddistributedsystem.com/tracks/timekeeper/tasks/task-4-3-3-causal-chat>

Track: 16. The Timekeeper
Task order: 13
Short title: Causal Chat
Difficulty: advanced
Subtrack: Vector Clocks

## Problem

Build a distributed chat system where messages are displayed in causal order even when they arrive out of network order. Each message carries the sender's vector clock.

A message `m` from node `j` with vector clock `vc_m` is **deliverable** at node `i` when:
1. `vc_m[j] == vc_i[j] + 1` (it is the next expected message from j)
2. `vc_m[k] <= vc_i[k]` for all `k != j` (all causal dependencies are met)

Implement handlers:

```json
Request:  {"type": "chat_send", "msg_id": 1, "text": "hello everyone"}
Response: {"type": "chat_send_ok", "in_reply_to": 1, "clock": [1, 0]}

Request:  {"type": "chat_recv", "msg_id": 2, "from": "n2", "text": "reply", "sender_clock": [0, 1]}
Response: {"type": "chat_recv_ok", "in_reply_to": 2, "delivered": true, "clock": [1, 1]}

Request:  {"type": "get_chat_log", "msg_id": 3}
Response: {"type": "get_chat_log_ok", "in_reply_to": 3, "messages": [
    {"from": "n1", "text": "hello everyone", "clock": [1, 0]},
    {"from": "n2", "text": "reply", "clock": [0, 1]}
]}
```

## Concepts

- causal ordering
- message reordering
- causal delivery
- distributed chat

## Hints

- Attach the sender vector clock to every chat message
- Buffer incoming messages that arrive out of causal order
- A message is deliverable when all of its causal dependencies are satisfied
- Causal dependency: for message from node j with vc, you need vc[j] == your_vc[j] + 1 and vc[k] <= your_vc[k] for all k != j
- After delivering a message, check the buffer for newly deliverable messages

## Test Cases

### 1. Send a chat message increments clock

Input:

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1","n2"]}}
{"src":"c1","dest":"n1","body":{"type":"chat_send","msg_id":2,"text":"hello"}}
{"src":"c1","dest":"n1","body":{"type":"get_clock","msg_id":3}}
```

Expected output:

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
{"src": "n1", "dest": "c1", "body": {"type": "chat_send_ok", "in_reply_to": 2, "clock": [1, 0], "msg_id": 1}}
{"src": "n1", "dest": "c1", "body": {"type": "get_clock_ok", "in_reply_to": 3, "clock": [1, 0], "msg_id": 2}}
```

### 2. Receive in-order message is delivered immediately

Input:

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1","n2"]}}
{"src":"n2","dest":"n1","body":{"type":"chat_recv","msg_id":2,"from":"n2","text":"hi","sender_clock":[0,1]}}
```

Expected output:

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
{"src": "n1", "dest": "n2", "body": {"type": "chat_recv_ok", "in_reply_to": 2, "delivered": true, "clock": [1, 1], "msg_id": 1}}
```

## Resources

- [Causal Ordering in Distributed Systems](https://www.baeldung.com/cs/causal-ordering-in-distributed-systems): How causal delivery guarantees message ordering using vector clocks

## Java Starter

The matching local starter file is:

```text
src/main/java/Main.java
```
