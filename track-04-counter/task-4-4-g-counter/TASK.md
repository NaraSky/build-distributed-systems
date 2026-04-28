# Build Grow-Only Counter (G-Counter) CRDT

Website: <https://builddistributedsystem.com/tracks/counter/tasks/task-4-4-g-counter>

Track: 4. The Counter
Task order: 4
Short title: G-Counter CRDT
Difficulty: intermediate
Subtrack: The Lost Update Problem

## Problem

Implement a G-Counter CRDT where each node maintains its own counter. The total is the sum of all per-node counters. Merging is done by taking the maximum of each nodes counter.

## Concept Notes

### CRDTs

Conflict-free Replicated Data Types are data structures designed for distributed systems. They guarantee convergence: all replicas that have seen the same updates will have the same state, regardless of update order.

### G-Counter

A G-Counter maintains a vector of counts, one per node. To increment, a node increments only its own entry. The total value is the sum of all entries. Merge takes the component-wise maximum.

## Concepts

- CRDT
- G-Counter
- convergence

## Hints

- Each node maintains its own counter
- Merge by taking max of each nodes counter
- Sum all counters for total

## Test Cases

### 1. G-Counter basic

Input:

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1","n2"]}}
{"src":"c1","dest":"n1","body":{"type":"add","msg_id":2,"delta":3}}
{"src":"c2","dest":"n1","body":{"type":"read","msg_id":3}}
```

Expected output:

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
{"src": "n1", "dest": "c1", "body": {"type": "add_ok", "in_reply_to": 2, "msg_id": 1}}
{"src": "n1", "dest": "c2", "body": {"type": "read_ok", "value": 3, "in_reply_to": 3, "msg_id": 2}}
```

## Resources

- [CRDTs Paper](https://hal.inria.fr/inria-00555588/document): Shapiro et al. comprehensive CRDT paper

## Java Starter

The matching local starter file is:

```text
src/main/java/Main.java
```
