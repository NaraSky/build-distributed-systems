# Implement a Lamport Clock from Scratch

Website: <https://builddistributedsystem.com/tracks/timekeeper/tasks/task-4-2-1-lamport-basic>

Track: 16. The Timekeeper
Task order: 6
Short title: Lamport Basic
Difficulty: intermediate
Subtrack: Lamport Clocks

## Problem

A Lamport clock is the simplest logical clock. Each node maintains a single integer counter that increases with every event. The rules are:

1. **Internal event**: increment the counter
2. **Send**: increment the counter, attach it to the message
3. **Receive**: set counter = max(local_counter, message_counter) + 1

Implement a Lamport clock node with these handlers:

```json
Request:  {"type": "tick", "msg_id": 1}
Response: {"type": "tick_ok", "in_reply_to": 1, "clock": 1}

Request:  {"type": "send_msg", "msg_id": 2, "dest": "n2", "payload": "hello"}
Response: {"type": "send_msg_ok", "in_reply_to": 2, "clock": 2}

Request:  {"type": "recv_msg", "msg_id": 3, "from": "n2", "remote_clock": 5, "payload": "hi"}
Response: {"type": "recv_msg_ok", "in_reply_to": 3, "clock": 6}

Request:  {"type": "get_clock", "msg_id": 4}
Response: {"type": "get_clock_ok", "in_reply_to": 4, "clock": 6}
```

## Concepts

- Lamport clock
- logical time
- happened-before
- causal ordering

## Hints

- A Lamport clock is a single integer counter per node
- Rule 1: Increment before any send event
- Rule 2: On receive, set clock = max(local, msg_clock) + 1
- Rule 3: Increment on any internal event
- Test with 3 nodes sending messages in a ring pattern

## Test Cases

### 1. Tick increments clock

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
{"src": "n1", "dest": "c1", "body": {"type": "tick_ok", "in_reply_to": 2, "clock": 1, "msg_id": 1}}
{"src": "n1", "dest": "c1", "body": {"type": "tick_ok", "in_reply_to": 3, "clock": 2, "msg_id": 2}}
{"src": "n1", "dest": "c1", "body": {"type": "get_clock_ok", "in_reply_to": 4, "clock": 2, "msg_id": 3}}
```

### 2. Receive updates clock to max + 1

Input:

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1","n2"]}}
{"src":"c1","dest":"n1","body":{"type":"tick","msg_id":2}}
{"src":"n2","dest":"n1","body":{"type":"recv_msg","msg_id":3,"from":"n2","remote_clock":10,"payload":"hi"}}
{"src":"c1","dest":"n1","body":{"type":"get_clock","msg_id":4}}
```

Expected output:

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
{"src": "n1", "dest": "c1", "body": {"type": "tick_ok", "in_reply_to": 2, "clock": 1, "msg_id": 1}}
{"src": "n1", "dest": "n2", "body": {"type": "recv_msg_ok", "in_reply_to": 3, "clock": 11, "msg_id": 2}}
{"src": "n1", "dest": "c1", "body": {"type": "get_clock_ok", "in_reply_to": 4, "clock": 11, "msg_id": 3}}
```

## Resources

- [Time, Clocks, and the Ordering of Events - Lamport 1978](https://lamport.azurewebsites.net/pubs/time-clocks.pdf): The original paper by Leslie Lamport on logical clocks

## Java Starter

The matching local starter file is:

```text
src/main/java/Main.java
```
