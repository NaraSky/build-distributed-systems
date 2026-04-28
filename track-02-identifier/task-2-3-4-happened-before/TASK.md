# Implement Happened-Before Detector with Vector Clocks

Website: <https://builddistributedsystem.com/tracks/identifier/tasks/task-2-3-4-happened-before>

Track: 2. The Identifier
Task order: 14
Short title: Happened-Before
Difficulty: advanced
Subtrack: Logical Clocks as IDs

## Problem

With vector clocks, you can determine the **exact causal relationship** between any two events:

- **A -> B** (A happened before B): A[i] <= B[i] for all i, and strict < for at least one
- **B -> A** (B happened before A): B[i] <= A[i] for all i, and strict < for at least one
- **A || B** (concurrent): neither dominates

Implement a `compare` handler:
```json
Request:  {"type": "compare", "msg_id": 1, 
           "vc_a": {"n1": 2, "n2": 1}, 
           "vc_b": {"n1": 1, "n2": 3}}
Response: {"type": "compare_ok", "in_reply_to": 1, "relation": "concurrent"}
```

Possible relations: `"a_before_b"`, `"b_before_a"`, `"concurrent"`, `"equal"`.

## Concepts

- happened-before
- concurrent events
- vector comparison
- conflict detection

## Hints

- A -> B if A[i] <= B[i] for all i, and A[j] < B[j] for at least one j
- A || B (concurrent) if neither A -> B nor B -> A
- Compare vectors element-wise across all nodes
- Store events with their vector clock snapshots for later comparison
- This is the foundation for conflict detection in databases like Riak

## Test Cases

### 1. A before B

Input:

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"compare","msg_id":2,"vc_a":{"n1":1,"n2":0},"vc_b":{"n1":2,"n2":1}}}
```

Expected output:

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
{"src": "n1", "dest": "c1", "body": {"type": "compare_ok", "relation": "a_before_b", "in_reply_to": 2, "msg_id": 1}}
```

### 2. Concurrent events

Input:

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"compare","msg_id":2,"vc_a":{"n1":2,"n2":1},"vc_b":{"n1":1,"n2":3}}}
```

Expected output:

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
{"src": "n1", "dest": "c1", "body": {"type": "compare_ok", "relation": "concurrent", "in_reply_to": 2, "msg_id": 1}}
```

## Resources

- [Why Vector Clocks Are Hard](https://riak.com/posts/technical/why-vector-clocks-are-hard/): Basho on practical challenges with vector clocks in Riak

## Java Starter

The matching local starter file is:

```text
src/main/java/Main.java
```
