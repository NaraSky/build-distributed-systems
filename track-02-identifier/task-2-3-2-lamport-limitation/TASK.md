# Demonstrate Lamport Clock Causality Limitation

Website: <https://builddistributedsystem.com/tracks/identifier/tasks/task-2-3-2-lamport-limitation>

Track: 2. The Identifier
Task order: 12
Short title: Causality Limitation
Difficulty: intermediate
Subtrack: Logical Clocks as IDs

## Problem

Lamport clocks guarantee: if A happens-before B, then L(A) < L(B). But the **converse is not true**: L(A) < L(B) does NOT mean A happened before B. Two concurrent events on different nodes can have any relative clock values.

Your task is to build an event tracker that demonstrates this limitation:

1. Track events on the local node with their Lamport timestamps
2. Accept events from remote nodes with their timestamps  
3. Implement a `check_causality` handler that, given two event IDs, reports whether causality can be determined from Lamport clocks alone

```json
Request:  {"type": "record_event", "msg_id": 1, "event_id": "e1", "data": "write x=1"}
Response: {"type": "record_event_ok", "in_reply_to": 1, "event_id": "e1", "clock": 1, "node": "n1"}
```

```json
Request:  {"type": "check_causality", "msg_id": 3, "event_a": "e1", "event_b": "e2"}
Response: {"type": "check_causality_ok", "in_reply_to": 3,
           "clock_a": 1, "clock_b": 2,
           "lamport_says": "a_before_b",
           "actual": "unknown"}
```

The `lamport_says` field reports what Lamport ordering suggests. The `actual` field is always "unknown" for events on different nodes (since Lamport clocks cannot determine true causality in that case).

## Concepts

- causality
- concurrent events
- partial order
- happens-before relation

## Hints

- L(A) < L(B) does NOT imply A happened before B
- Two independent events on different nodes can have any clock ordering
- Construct a scenario where two events have ordered clocks but are concurrent
- The converse of the Lamport property fails: ordered clocks do not imply causality
- This limitation motivates vector clocks

## Test Cases

### 1. Record event returns clock and node

Input:

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"record_event","msg_id":2,"event_id":"e1","data":"write x"}}
```

Expected output:

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
{"src": "n1", "dest": "c1", "body": {"type": "record_event_ok", "event_id": "e1", "clock": 1, "node": "n1", "in_reply_to": 2, "msg_id": 1}}
```

### 2. Check causality between two local events

Input:

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"record_event","msg_id":2,"event_id":"e1","data":"a"}}
{"src":"c1","dest":"n1","body":{"type":"record_event","msg_id":3,"event_id":"e2","data":"b"}}
{"src":"c1","dest":"n1","body":{"type":"check_causality","msg_id":4,"event_a":"e1","event_b":"e2"}}
```

Expected output:

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
{"src": "n1", "dest": "c1", "body": {"type": "record_event_ok", "event_id": "e1", "clock": 1, "node": "n1", "in_reply_to": 2, "msg_id": 1}}
{"src": "n1", "dest": "c1", "body": {"type": "record_event_ok", "event_id": "e2", "clock": 2, "node": "n1", "in_reply_to": 3, "msg_id": 2}}
{"src": "n1", "dest": "c1", "body": {"type": "check_causality_ok", "clock_a": 1, "clock_b": 2, "lamport_says": "a_before_b", "actual": "causal", "in_reply_to": 4, "msg_id": 3}}
```

## Resources

- [Logical Clocks - Martin Kleppmann](https://martin.kleppmann.com/2020/12/02/bloom-filter-hash-graph-sync.html): Kleppmann on clock systems and distributed ordering

## Java Starter

The matching local starter file is:

```text
src/main/java/Main.java
```
