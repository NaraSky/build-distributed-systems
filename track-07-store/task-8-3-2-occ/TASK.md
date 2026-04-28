# Implement Optimistic Concurrency Control

Website: <https://builddistributedsystem.com/tracks/store/tasks/task-8-3-2-occ>

Track: 7. The Store
Task order: 12
Short title: OCC
Difficulty: advanced
Subtrack: Transactions on Raft

## Problem

Implement optimistic concurrency control (OCC). Read keys with version tracking, then commit only if no versions changed since the read.

```json
Request:  {"type": "occ_begin", "msg_id": 1}
Response: {"type": "occ_begin_ok", "in_reply_to": 1, "txn_id": "t1"}

Request:  {"type": "occ_read", "msg_id": 2, "txn_id": "t1", "key": "x"}
Response: {"type": "occ_read_ok", "in_reply_to": 2, "value": "42", "version": 5}

Request:  {"type": "occ_commit", "msg_id": 3, "txn_id": "t1", "writes": [{"key": "x", "value": "43"}], "read_versions": [{"key": "x", "version": 5}]}
Response: {"type": "occ_commit_ok", "in_reply_to": 3, "committed": true, "new_version": 6}
```

## Concepts

- OCC
- version check
- conflict detection
- abort and retry

## Hints

- Read a set of keys and record their versions
- At commit time, check that none of the versions have changed
- If versions match, the transaction commits. Otherwise, abort and retry
- OCC works well when conflicts are rare (optimistic assumption)
- High contention leads to many aborts and retries

## Test Cases

### 1. OCC commit succeeds with matching versions

occ_commit_ok should show committed: true.

Input:

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"occ_begin","msg_id":2}}
{"src":"c1","dest":"n1","body":{"type":"occ_commit","msg_id":3,"txn_id":"t1","writes":[{"key":"x","value":"1"}],"read_versions":[]}}
```

Expected output:

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

### 2. OCC aborts on version mismatch

occ_commit_ok should show committed: false because version 999 does not match actual.

Input:

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"occ_commit","msg_id":2,"txn_id":"t1","writes":[{"key":"x","value":"new"}],"read_versions":[{"key":"x","version":999}]}}
```

Expected output:

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

## Resources

- [Optimistic Concurrency Control](https://en.wikipedia.org/wiki/Optimistic_concurrency_control): OCC overview: read, validate, write phases

## Java Starter

The matching local starter file is:

```text
src/main/java/Main.java
```
