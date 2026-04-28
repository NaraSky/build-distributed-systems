# Simulate Concurrent Mutex Requests from Multiple Nodes

Website: <https://builddistributedsystem.com/tracks/timekeeper/tasks/task-4-2-4-mutex-contention>

Track: 16. The Timekeeper
Task order: 9
Short title: Mutex Contention
Difficulty: advanced
Subtrack: Lamport Clocks

## Problem

Simulate 5 nodes all requesting the mutex simultaneously. With Lamport's algorithm, only one can hold it at a time. The request with the lowest (timestamp, node_id) pair wins.

Your task is to process multiple lock requests and verify mutual exclusion:

```json
Request:  {"type": "multi_request", "msg_id": 1, "requests": [
    {"node": "n1", "ts": 3}, {"node": "n2", "ts": 1}, {"node": "n3", "ts": 3},
    {"node": "n4", "ts": 2}, {"node": "n5", "ts": 1}
]}
Response: {"type": "multi_request_ok", "in_reply_to": 1, "grant_order": ["n2","n5","n4","n1","n3"],
           "violations": 0}
```

Also implement a `release_lock` handler:
```json
Request:  {"type": "release_lock", "msg_id": 2, "node": "n2"}
Response: {"type": "release_lock_ok", "in_reply_to": 2, "next_holder": "n5"}
```

## Concepts

- contention
- fairness
- wait time
- queue ordering

## Hints

- When multiple nodes request simultaneously, the one with the lowest (ts, node_id) wins
- Track how long each node waits before acquiring the lock
- Verify mutual exclusion: only one holder at a time
- After release, the next node in the queue should be able to acquire
- Report average and max wait times across all requests

## Test Cases

### 1. Multi request orders by (ts, node_id)

Input:

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"multi_request","msg_id":2,"requests":[{"node":"n1","ts":3},{"node":"n2","ts":1},{"node":"n3","ts":3},{"node":"n4","ts":2},{"node":"n5","ts":1}]}}
```

Expected output:

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
{"src": "n1", "dest": "c1", "body": {"type": "multi_request_ok", "in_reply_to": 2, "grant_order": ["n2", "n5", "n4", "n1", "n3"], "violations": 0, "msg_id": 1}}
```

### 2. Single request gets immediate grant

Input:

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"multi_request","msg_id":2,"requests":[{"node":"n1","ts":1}]}}
```

Expected output:

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
{"src": "n1", "dest": "c1", "body": {"type": "multi_request_ok", "in_reply_to": 2, "grant_order": ["n1"], "violations": 0, "msg_id": 1}}
```

## Resources

- [Mutual Exclusion in Distributed Systems](https://www.cs.helsinki.fi/group/cosco/Teaching/2012/DS-lect/Lect09.pdf): Lecture on distributed mutual exclusion and contention handling

## Java Starter

The matching local starter file is:

```text
src/main/java/Main.java
```
