# Handle Leader Changes with No-Op on Election

Website: <https://builddistributedsystem.com/tracks/consensus/tasks/task-7-2-3-noop-on-election>

Track: 6. The Consensus
Task order: 8
Short title: No-Op on Election
Difficulty: advanced
Subtrack: Commitment and Application

## Problem

When a new leader is elected, it must not apply uncommitted entries from previous terms. The "no-op on election" trick solves this: the new leader immediately appends a no-op entry in its own term. Once this no-op is committed (majority replicated), all prior entries are also committed.

```json
Request:  {"type": "leader_change", "msg_id": 1, "new_leader": "n2", "new_term": 3, "log": [
    {"index": 1, "term": 1, "command": {"op": "put", "key": "x", "value": "1"}},
    {"index": 2, "term": 2, "command": {"op": "put", "key": "y", "value": "2"}},
    {"index": 3, "term": 2, "command": {"op": "put", "key": "z", "value": "3"}}
], "commit_index": 1}
Response: {"type": "leader_change_ok", "in_reply_to": 1, "noop_appended_at": 4, "noop_term": 3, "safe_to_apply_after_commit": true}

Request:  {"type": "simulate_noop_commit", "msg_id": 2, "noop_index": 4}
Response: {"type": "simulate_noop_commit_ok", "in_reply_to": 2, "new_commit_index": 4, "entries_now_committed": [2, 3, 4]}
```

## Concepts

- no-op entry
- leader change
- uncommitted entries
- safety

## Hints

- A new leader cannot know which entries from previous terms are committed
- The no-op trick: new leader appends a no-op entry in its own term
- Once the no-op is committed, all prior entries are also committed
- This avoids the problem of a new leader applying uncommitted old entries
- The no-op is a dummy command that does not modify state

## Test Cases

### 1. New leader appends no-op

leader_change_ok should show noop_appended_at: 2 and noop_term: 3.

Input:

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"leader_change","msg_id":2,"new_leader":"n1","new_term":3,"log":[{"index":1,"term":1,"command":{"op":"put","key":"x","value":"1"}}],"commit_index":0}}
```

Expected output:

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

### 2. No-op commit advances all prior entries

simulate_noop_commit_ok should show new_commit_index: 3, entries_now_committed: [1, 2, 3].

Input:

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"leader_change","msg_id":2,"new_leader":"n1","new_term":2,"log":[{"index":1,"term":1,"command":{"op":"put","key":"x","value":"1"}},{"index":2,"term":1,"command":{"op":"put","key":"y","value":"2"}}],"commit_index":0}}
{"src":"c1","dest":"n1","body":{"type":"simulate_noop_commit","msg_id":3,"noop_index":3}}
```

Expected output:

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

## Resources

- [Raft - Committing entries from previous terms](https://raft.github.io/raft.pdf): Raft paper Section 5.4.2 on the no-op trick for safe commitment

## Java Starter

The matching local starter file is:

```text
src/main/java/Main.java
```
