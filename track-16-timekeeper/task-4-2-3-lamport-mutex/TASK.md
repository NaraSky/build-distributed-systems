# Implement Distributed Mutual Exclusion with Lamport Clocks

Website: <https://builddistributedsystem.com/tracks/timekeeper/tasks/task-4-2-3-lamport-mutex>

Track: 16. The Timekeeper
Task order: 8
Short title: Lamport Mutex
Difficulty: advanced
Subtrack: Lamport Clocks

## Problem

Lamport's mutual exclusion algorithm uses Lamport clocks to totally order lock requests. Each node maintains a request queue sorted by (timestamp, node_id).

**Protocol:**
1. To **request** the lock: broadcast a REQUEST(ts, node_id) to all other nodes, add to local queue
2. On receiving REQUEST: add to queue, send REPLY
3. To **enter critical section**: your request must be at the head of the queue AND you must have received REPLY from every other node
4. To **release**: remove from queue, broadcast RELEASE

Implement:
```json
Request:  {"type": "request_lock", "msg_id": 1}
Response: {"type": "request_lock_ok", "in_reply_to": 1, "position": 1, "ts": 1}

Request:  {"type": "lock_status", "msg_id": 2}
Response: {"type": "lock_status_ok", "in_reply_to": 2, "holding": false, "queue_size": 1, "queue": [{"ts": 1, "node": "n1"}]}
```

## Concepts

- distributed mutex
- Lamport mutex
- request queue
- total ordering

## Hints

- Each node maintains a priority queue of lock requests sorted by Lamport timestamp
- To request: broadcast REQUEST to all nodes, add self to queue
- To release: broadcast RELEASE to all nodes, remove self from queue
- A node can enter CS when: its request is at the head AND it has received replies from all others
- Use (timestamp, node_id) pairs for total ordering to break ties

## Test Cases

### 1. Request lock adds to queue

Input:

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"request_lock","msg_id":2}}
{"src":"c1","dest":"n1","body":{"type":"lock_status","msg_id":3}}
```

Expected output:

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
{"src": "n1", "dest": "c1", "body": {"type": "request_lock_ok", "in_reply_to": 2, "position": 1, "ts": 1, "msg_id": 1}}
{"src": "n1", "dest": "c1", "body": {"type": "lock_status_ok", "in_reply_to": 3, "holding": true, "queue_size": 1, "queue": [{"ts": 1, "node": "n1"}], "msg_id": 2}}
```

### 2. Lock status with empty queue

Input:

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"lock_status","msg_id":2}}
```

Expected output:

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
{"src": "n1", "dest": "c1", "body": {"type": "lock_status_ok", "in_reply_to": 2, "holding": false, "queue_size": 0, "queue": [], "msg_id": 1}}
```

## Resources

- [Distributed Mutual Exclusion Algorithms](https://www.cs.uic.edu/~ajayk/Chapter9.pdf): Overview of distributed mutex algorithms including Lamport

## Java Starter

The matching local starter file is:

```text
src/main/java/Main.java
```
