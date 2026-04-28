# Implement Multi-Version Concurrency Control

Website: <https://builddistributedsystem.com/tracks/store/tasks/task-8-3-3-mvcc>

Track: 7. The Store
Task order: 13
Short title: MVCC
Difficulty: advanced
Subtrack: Transactions on Raft

## Problem

Implement MVCC: keep multiple versions of each key. Readers get a consistent snapshot without blocking writers.

```json
Request:  {"type": "mvcc_put", "msg_id": 1, "key": "x", "value": "v1", "timestamp": 100}
Response: {"type": "mvcc_put_ok", "in_reply_to": 1, "version": 1, "timestamp": 100}

Request:  {"type": "mvcc_put", "msg_id": 2, "key": "x", "value": "v2", "timestamp": 200}
Response: {"type": "mvcc_put_ok", "in_reply_to": 2, "version": 2, "timestamp": 200}

Request:  {"type": "mvcc_get", "msg_id": 3, "key": "x", "read_timestamp": 150}
Response: {"type": "mvcc_get_ok", "in_reply_to": 3, "value": "v1", "version": 1, "as_of_timestamp": 100}

Request:  {"type": "mvcc_get", "msg_id": 4, "key": "x", "read_timestamp": 250}
Response: {"type": "mvcc_get_ok", "in_reply_to": 4, "value": "v2", "version": 2, "as_of_timestamp": 200}
```

## Concepts

- MVCC
- versioned storage
- snapshot isolation
- readers never block writers

## Hints

- Keep N versions of each key, each tagged with a commit timestamp
- Readers get a consistent snapshot at their start timestamp
- Writers create new versions without blocking readers
- Garbage collect old versions that are no longer needed
- This is how PostgreSQL, MySQL InnoDB, and TiKV work internally

## Test Cases

### 1. Read at old timestamp gets old version

mvcc_get_ok should return value: "old" since read_timestamp 150 < write timestamp 200.

Input:

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"mvcc_put","msg_id":2,"key":"x","value":"old","timestamp":100}}
{"src":"c1","dest":"n1","body":{"type":"mvcc_put","msg_id":3,"key":"x","value":"new","timestamp":200}}
{"src":"c1","dest":"n1","body":{"type":"mvcc_get","msg_id":4,"key":"x","read_timestamp":150}}
```

Expected output:

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

### 2. Read at current timestamp gets latest

mvcc_get_ok should return value: "new" since read_timestamp 300 > write timestamp 200.

Input:

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"mvcc_put","msg_id":2,"key":"x","value":"old","timestamp":100}}
{"src":"c1","dest":"n1","body":{"type":"mvcc_put","msg_id":3,"key":"x","value":"new","timestamp":200}}
{"src":"c1","dest":"n1","body":{"type":"mvcc_get","msg_id":4,"key":"x","read_timestamp":300}}
```

Expected output:

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

## Resources

- [MVCC in PostgreSQL](https://www.postgresql.org/docs/current/mvcc-intro.html): How PostgreSQL implements MVCC for concurrent access

## Java Starter

The matching local starter file is:

```text
src/main/java/Main.java
```
