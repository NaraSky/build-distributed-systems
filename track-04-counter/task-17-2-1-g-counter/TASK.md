# Implement a G-Counter (Grow-Only CRDT)

Website: <https://builddistributedsystem.com/tracks/counter/tasks/task-17-2-1-g-counter>

Track: 4. The Counter
Task order: 6
Short title: G-Counter
Difficulty: intermediate
Subtrack: G-Counter and PN-Counter

## Problem

A G-Counter (Grow-only Counter) is the simplest CRDT. Each node maintains a vector of N integers, one per node. A node only increments its own slot, and the total value is the sum of all slots.

**Data structure**: vector of N integers, where N = number of nodes.

**Operations**:
- `increment()`: `counters[my_node_id] += 1`
- `value()`: `sum(counters)`
- `merge(other)`: `counters[i] = max(counters[i], other.counters[i])` for all i

**Why it works**: each node independently increments its own slot. The merge function (element-wise max) is commutative, associative, and idempotent — making it a valid CRDT that always converges regardless of message ordering or duplication.

```json
Request:  {"type": "increment", "msg_id": 1}
Response: {"type": "increment_ok", "in_reply_to": 1, "local_value": 1}

Request:  {"type": "read", "msg_id": 2}
Response: {"type": "read_ok", "in_reply_to": 2, "value": 5}
```

## Concepts

- G-Counter
- CRDT
- vector of counters
- element-wise max
- convergence

## Hints

- Each node maintains a vector of N integers (one slot per node)
- Node I only increments its own slot: counters[I] += 1
- Value = sum of all slots across the vector
- Merge = element-wise max of two vectors
- This guarantees convergence: merge is commutative, associative, and idempotent

## Test Cases

### 1. Increment increases local counter

Input:

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1","n2","n3"]}}
{"src":"c1","dest":"n1","body":{"type":"increment","msg_id":2}}
{"src":"c1","dest":"n1","body":{"type":"read","msg_id":3}}
```

Expected output:

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
{"src": "n1", "dest": "c1", "body": {"type": "increment_ok", "in_reply_to": 2, "msg_id": 1}}
{"src": "n1", "dest": "c1", "body": {"type": "read_ok", "in_reply_to": 3, "value": 1, "msg_id": 2}}
```

### 2. Multiple increments accumulate

Input:

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"increment","msg_id":2}}
{"src":"c1","dest":"n1","body":{"type":"increment","msg_id":3}}
{"src":"c1","dest":"n1","body":{"type":"increment","msg_id":4}}
{"src":"c1","dest":"n1","body":{"type":"read","msg_id":5}}
```

Expected output:

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
{"src": "n1", "dest": "c1", "body": {"type": "increment_ok", "in_reply_to": 2, "msg_id": 1}}
{"src": "n1", "dest": "c1", "body": {"type": "increment_ok", "in_reply_to": 3, "msg_id": 2}}
{"src": "n1", "dest": "c1", "body": {"type": "increment_ok", "in_reply_to": 4, "msg_id": 3}}
{"src": "n1", "dest": "c1", "body": {"type": "read_ok", "in_reply_to": 5, "value": 3, "msg_id": 4}}
```

## Resources

- [CRDTs: G-Counter](https://crdt.tech/glossary): CRDT glossary with G-Counter definition and properties

## Java Starter

The matching local starter file is:

```text
src/main/java/Main.java
```
