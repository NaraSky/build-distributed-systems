# Implement a PN-Counter for Increment and Decrement

Website: <https://builddistributedsystem.com/tracks/counter/tasks/task-17-2-3-pn-counter>

Track: 4. The Counter
Task order: 8
Short title: PN-Counter
Difficulty: intermediate
Subtrack: G-Counter and PN-Counter

## Problem

A G-Counter only grows. To support decrements, the PN-Counter uses two G-Counters: P (positive) for increments and N (negative) for decrements.

**Data structure**: two G-Counter vectors — P and N.

**Operations**:
- `increment()`: `P.counters[my_id] += 1`
- `decrement()`: `N.counters[my_id] += 1`
- `value()`: `P.value() - N.value()` = `sum(P) - sum(N)`
- `merge(other)`: merge P vectors separately, merge N vectors separately

The value can go negative (if more decrements than increments). The CRDT properties hold because each component (P and N) is independently a valid G-Counter.

```json
Request:  {"type": "add", "msg_id": 1, "delta": 1}
Response: {"type": "add_ok", "in_reply_to": 1}

Request:  {"type": "add", "msg_id": 2, "delta": -1}
Response: {"type": "add_ok", "in_reply_to": 2}

Request:  {"type": "read", "msg_id": 3}
Response: {"type": "read_ok", "in_reply_to": 3, "value": 0}
```

## Concepts

- PN-Counter
- increment
- decrement
- two G-Counters
- subtraction

## Hints

- A PN-Counter uses TWO G-Counters: P (positive/increments) and N (negative/decrements)
- increment() increments P, decrement() increments N
- value() = P.value() - N.value()
- merge: merge P counters separately, merge N counters separately
- This supports both increment and decrement while maintaining CRDT properties

## Test Cases

### 1. Increment and decrement balance to zero

Input:

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"add","msg_id":2,"delta":1}}
{"src":"c1","dest":"n1","body":{"type":"add","msg_id":3,"delta":-1}}
{"src":"c1","dest":"n1","body":{"type":"read","msg_id":4}}
```

Expected output:

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
{"src": "n1", "dest": "c1", "body": {"type": "add_ok", "in_reply_to": 2, "msg_id": 1}}
{"src": "n1", "dest": "c1", "body": {"type": "add_ok", "in_reply_to": 3, "msg_id": 2}}
{"src": "n1", "dest": "c1", "body": {"type": "read_ok", "in_reply_to": 4, "value": 0, "msg_id": 3}}
```

### 2. Value can go negative

Input:

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"add","msg_id":2,"delta":-5}}
{"src":"c1","dest":"n1","body":{"type":"read","msg_id":3}}
```

Expected output:

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
{"src": "n1", "dest": "c1", "body": {"type": "add_ok", "in_reply_to": 2, "msg_id": 1}}
{"src": "n1", "dest": "c1", "body": {"type": "read_ok", "in_reply_to": 3, "value": -5, "msg_id": 2}}
```

## Resources

- [PN-Counter CRDT](https://en.wikipedia.org/wiki/Conflict-free_replicated_data_type#PN-Counter): Wikipedia article on PN-Counter CRDT

## Java Starter

The matching local starter file is:

```text
src/main/java/Main.java
```
