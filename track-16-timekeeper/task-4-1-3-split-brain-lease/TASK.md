# Simulate Split-Brain Caused by Clock Drift

Website: <https://builddistributedsystem.com/tracks/timekeeper/tasks/task-4-1-3-split-brain-lease>

Track: 16. The Timekeeper
Task order: 3
Short title: Split-Brain Lease
Difficulty: advanced
Subtrack: Physical Time and Its Failures

## Problem

Time-based leases break when clocks drift. Two nodes can both believe they hold a valid lease simultaneously, causing **split-brain**.

Implement lease management with clock drift simulation:

```json
Request:  {"type": "acquire_lease", "msg_id": 1, "duration_ms": 5000}
Response: {"type": "acquire_lease_ok", "in_reply_to": 1, "expires_at": 1234572000}

Request:  {"type": "check_lease", "msg_id": 2}
Response: {"type": "check_lease_ok", "in_reply_to": 2, "valid": true, "remaining_ms": 3000}
```

## Concepts

- split-brain
- lease
- clock drift
- leader election

## Hints

- A lease grants leadership for a duration based on local clock
- If two nodes clocks drift apart, both may think their lease is valid
- This is the fundamental problem with time-based distributed locks
- Track lease state and detect overlapping valid leases
- Simulate by giving each node a different clock offset

## Test Cases

### 1. Acquire lease returns expires_at

acquire_lease_ok with expires_at > 0.

Input:

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"acquire_lease","msg_id":2,"duration_ms":5000}}
```

Expected output:

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

### 2. Check lease shows valid

check_lease_ok should have valid=true and remaining_ms > 0.

Input:

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"acquire_lease","msg_id":2,"duration_ms":60000}}
{"src":"c1","dest":"n1","body":{"type":"check_lease","msg_id":3}}
```

Expected output:

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

## Resources

- [How to do distributed locking](https://martin.kleppmann.com/2016/02/08/how-to-do-distributed-locking.html): Kleppmann on time-based distributed locks and their failure modes

## Java Starter

The matching local starter file is:

```text
src/main/java/Main.java
```
