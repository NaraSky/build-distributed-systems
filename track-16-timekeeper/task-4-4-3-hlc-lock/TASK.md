# Implement a Distributed Lock Using HLC Timestamps

Website: <https://builddistributedsystem.com/tracks/timekeeper/tasks/task-4-4-3-hlc-lock>

Track: 16. The Timekeeper
Task order: 18
Short title: HLC Lock
Difficulty: advanced
Subtrack: Hybrid Logical Clocks

## Problem

Build a distributed lock where the lock is granted based on HLC timestamps. The process with the lowest HLC timestamp in the request queue gets the lock. This gives a total ordering that respects causality.

Tie-breaking: compare `(pt, c, node_id)` lexicographically.

Implement handlers:

```json
Request:  {"type": "lock_request", "msg_id": 1, "resource": "db_write", "requester": "n1", "hlc_pt": 1000, "hlc_c": 0}
Response: {"type": "lock_request_ok", "in_reply_to": 1, "position": 1, "granted": true}

Request:  {"type": "lock_request", "msg_id": 2, "resource": "db_write", "requester": "n2", "hlc_pt": 999, "hlc_c": 0}
Response: {"type": "lock_request_ok", "in_reply_to": 2, "position": 1, "granted": false, "reason": "lock_held_by_n1"}

Request:  {"type": "lock_release", "msg_id": 3, "resource": "db_write", "requester": "n1"}
Response: {"type": "lock_release_ok", "in_reply_to": 3, "next_holder": "n2"}

Request:  {"type": "lock_status", "msg_id": 4, "resource": "db_write"}
Response: {"type": "lock_status_ok", "in_reply_to": 4, "holder": "n2", "queue_size": 0}
```

## Concepts

- distributed lock
- HLC timestamp
- request queue
- priority ordering

## Hints

- Each lock request is stamped with the requester HLC timestamp
- The lock is granted to the request with the lowest HLC timestamp
- Use (pt, c, node_id) as a total order to break ties
- Maintain a sorted queue of pending lock requests
- Release removes from the queue and grants to the next lowest

## Test Cases

### 1. First request grants the lock

Input:

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"lock_request","msg_id":2,"resource":"r1","requester":"n1","hlc_pt":1000,"hlc_c":0}}
```

Expected output:

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
{"src": "n1", "dest": "c1", "body": {"type": "lock_request_ok", "in_reply_to": 2, "position": 1, "granted": true, "msg_id": 1}}
```

### 2. Second request queues behind held lock

Second lock_request_ok should show granted: false. lock_status_ok should show holder: n1, queue_size: 1.

Input:

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"lock_request","msg_id":2,"resource":"r1","requester":"n1","hlc_pt":1000,"hlc_c":0}}
{"src":"c1","dest":"n1","body":{"type":"lock_request","msg_id":3,"resource":"r1","requester":"n2","hlc_pt":999,"hlc_c":0}}
{"src":"c1","dest":"n1","body":{"type":"lock_status","msg_id":4,"resource":"r1"}}
```

Expected output:

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
{"src": "n1", "dest": "c1", "body": {"type": "lock_request_ok", "in_reply_to": 2, "position": 1, "granted": true, "msg_id": 1}}
```

## Resources

- [Distributed Locking with Timestamps](https://martin.kleppmann.com/2016/02/08/how-to-do-distributed-locking.html): Martin Kleppmann on correctness of distributed lock implementations

## Java Starter

The matching local starter file is:

```text
src/main/java/Main.java
```
