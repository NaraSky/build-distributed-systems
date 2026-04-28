# Compare Mutex Algorithms: Lamport vs Token Ring vs Centralized

Website: <https://builddistributedsystem.com/tracks/timekeeper/tasks/task-4-2-5-mutex-comparison>

Track: 16. The Timekeeper
Task order: 10
Short title: Mutex Comparison
Difficulty: advanced
Subtrack: Lamport Clocks

## Problem

Different distributed mutex algorithms have different tradeoffs. Compare three approaches:

1. **Lamport's algorithm**: 3(N-1) messages per CS entry, fully distributed, fair
2. **Token ring**: 0 to N-1 messages, no starvation, but token can be lost
3. **Centralized**: 3 messages, simple, but coordinator is a single point of failure

Implement a `compare_mutex` handler:
```json
Request:  {"type": "compare_mutex", "msg_id": 1, "nodes": 5}
Response: {"type": "compare_mutex_ok", "in_reply_to": 1, "comparison": [
    {"algorithm": "lamport", "messages_per_cs": 12, "fault_tolerant": true, "fair": true},
    {"algorithm": "token_ring", "messages_per_cs_avg": 2.5, "fault_tolerant": false, "fair": true},
    {"algorithm": "centralized", "messages_per_cs": 3, "fault_tolerant": false, "fair": true}
]}
```

Also implement a `simulate_token_ring` handler:
```json
Request:  {"type": "simulate_token_ring", "msg_id": 2, "nodes": 5, "requests": ["n3", "n1"]}
Response: {"type": "simulate_token_ring_ok", "in_reply_to": 2, "total_messages": 5, "grant_order": ["n3", "n1"]}
```

## Concepts

- message complexity
- token ring
- centralized mutex
- algorithm comparison

## Hints

- Lamport mutex: 3(N-1) messages per critical section entry (request + reply + release)
- Token ring: 0 to N-1 messages per entry (depends on token position)
- Centralized: 3 messages per entry (request + grant + release) but single point of failure
- Compare on: message count, fault tolerance, fairness, and latency
- Build a comparison table with all metrics

## Test Cases

### 1. Compare mutex for 5 nodes

compare_mutex_ok with 3 algorithm entries. Lamport messages_per_cs = 3*(5-1) = 12.

Input:

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"compare_mutex","msg_id":2,"nodes":5}}
```

Expected output:

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

### 2. Compare mutex for 10 nodes

Lamport messages_per_cs = 3*(10-1) = 27. Centralized stays at 3.

Input:

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"compare_mutex","msg_id":2,"nodes":10}}
```

Expected output:

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

## Resources

- [Comparison of Mutual Exclusion Algorithms](https://www.geeksforgeeks.org/mutual-exclusion-in-distributed-system/): Comparison table of distributed mutex algorithms

## Java Starter

The matching local starter file is:

```text
src/main/java/Main.java
```
