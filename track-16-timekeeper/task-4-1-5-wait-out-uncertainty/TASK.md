# Wait-Out-Uncertainty for External Consistency

Website: <https://builddistributedsystem.com/tracks/timekeeper/tasks/task-4-1-5-wait-out-uncertainty>

Track: 16. The Timekeeper
Task order: 5
Short title: Wait Uncertainty
Difficulty: advanced
Subtrack: Physical Time and Its Failures

## Problem

Spanner achieves external consistency by waiting out the uncertainty window: before committing a transaction at timestamp T, wait until `TrueTime.now().earliest > T`. This guarantees causally-later transactions see this commit.

Implement a `commit` handler with wait-out-uncertainty:
```json
Request:  {"type": "commit", "msg_id": 1, "key": "x", "value": "v1"}
Response: {"type": "commit_ok", "in_reply_to": 1, "commit_ts": 1234567, "wait_ms": 7}

Request:  {"type": "commit_stats", "msg_id": 2}
Response: {"type": "commit_stats_ok", "in_reply_to": 2, "total_commits": 5, "total_wait_ms": 35, "avg_wait_ms": 7}
```

## Concepts

- external consistency
- commit wait
- Spanner
- linearizability

## Hints

- Before committing, wait until TrueTime.now().earliest > commit_timestamp
- This guarantees that any future read will see this commit
- The wait duration equals the uncertainty window
- This is how Spanner achieves external consistency without locks
- Track total wait time for performance analysis

## Test Cases

### 1. Commit stores value

commit_ok with commit_ts and wait_ms, then kv_read_ok with value=v1.

Input:

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"commit","msg_id":2,"key":"x","value":"v1"}}
{"src":"c1","dest":"n1","body":{"type":"kv_read","msg_id":3,"key":"x"}}
```

Expected output:

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

### 2. Commit stats with no commits

Input:

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"commit_stats","msg_id":2}}
```

Expected output:

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
{"src": "n1", "dest": "c1", "body": {"type": "commit_stats_ok", "total_commits": 0, "total_wait_ms": 0, "avg_wait_ms": 0, "in_reply_to": 2, "msg_id": 1}}
```

## Resources

- [Spanner Commit Wait](https://cloud.google.com/spanner/docs/true-time-external-consistency): Google Cloud documentation on TrueTime commit wait

## Java Starter

The matching local starter file is:

```text
src/main/java/Main.java
```
