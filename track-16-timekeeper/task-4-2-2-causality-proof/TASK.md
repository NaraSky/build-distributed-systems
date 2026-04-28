# Prove Lamport Clock Causality and Its Limitation

Website: <https://builddistributedsystem.com/tracks/timekeeper/tasks/task-4-2-2-causality-proof>

Track: 16. The Timekeeper
Task order: 7
Short title: Causality Proof
Difficulty: advanced
Subtrack: Lamport Clocks

## Problem

Lamport clocks guarantee: if event A **happened-before** event B, then L(A) < L(B). But the converse is NOT true - L(A) < L(B) does NOT mean A caused B. Events may be **concurrent** (neither caused the other).

Your task is to build a system that:
1. Records events with Lamport timestamps
2. Tracks the actual causal chain (send/receive links)
3. Compares what Lamport timestamps tell us vs actual causality

Implement:
```json
Request:  {"type": "record_event", "msg_id": 1, "event_id": "e1", "caused_by": null}
Response: {"type": "record_event_ok", "in_reply_to": 1, "clock": 1}

Request:  {"type": "record_event", "msg_id": 2, "event_id": "e2", "caused_by": "e1"}
Response: {"type": "record_event_ok", "in_reply_to": 2, "clock": 2}

Request:  {"type": "check_causality", "msg_id": 3, "event_a": "e1", "event_b": "e2"}
Response: {"type": "check_causality_ok", "in_reply_to": 3,
           "lamport_says": "a_before_b", "actual": "a_before_b", "correct": true}
```

## Concepts

- happened-before
- causality
- concurrent events
- Lamport limitation

## Hints

- If A happened-before B, then L(A) < L(B) - this is guaranteed
- The converse is NOT true: L(A) < L(B) does NOT imply A happened-before B
- Construct a counterexample with two independent nodes that never communicate
- Node n1 ticks once (L=1), node n2 ticks twice (L=2) - L(n1) < L(n2) but they are concurrent
- Report whether two events are causal or concurrent based on Lamport timestamps alone

## Test Cases

### 1. Record two causal events

Input:

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"record_event","msg_id":2,"event_id":"e1","caused_by":null}}
{"src":"c1","dest":"n1","body":{"type":"record_event","msg_id":3,"event_id":"e2","caused_by":"e1"}}
```

Expected output:

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
{"src": "n1", "dest": "c1", "body": {"type": "record_event_ok", "in_reply_to": 2, "clock": 1, "msg_id": 1}}
{"src": "n1", "dest": "c1", "body": {"type": "record_event_ok", "in_reply_to": 3, "clock": 2, "msg_id": 2}}
```

### 2. Check causality of causal pair

Input:

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"record_event","msg_id":2,"event_id":"e1","caused_by":null}}
{"src":"c1","dest":"n1","body":{"type":"record_event","msg_id":3,"event_id":"e2","caused_by":"e1"}}
{"src":"c1","dest":"n1","body":{"type":"check_causality","msg_id":4,"event_a":"e1","event_b":"e2"}}
```

Expected output:

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
{"src": "n1", "dest": "c1", "body": {"type": "record_event_ok", "in_reply_to": 2, "clock": 1, "msg_id": 1}}
{"src": "n1", "dest": "c1", "body": {"type": "record_event_ok", "in_reply_to": 3, "clock": 2, "msg_id": 2}}
{"src": "n1", "dest": "c1", "body": {"type": "check_causality_ok", "in_reply_to": 4, "lamport_says": "a_before_b", "actual": "a_before_b", "correct": true, "msg_id": 3}}
```

## Resources

- [Happened-Before Relation](https://en.wikipedia.org/wiki/Happened-before): Wikipedia explanation of the happened-before partial order

## Java Starter

The matching local starter file is:

```text
src/main/java/Main.java
```
