# Implement an etcd-Compatible API Layer

Website: <https://builddistributedsystem.com/tracks/watcher/tasks/task-15-3-4-etcd-api>

Track: 22. The Watcher
Task order: 14
Short title: etcd API
Difficulty: advanced
Subtrack: Consistency and the ZAB Protocol

## Problem

etcd provides a modern key-value API on top of a Raft-based consensus layer. Implementing an etcd-compatible API on your ZAB-based system demonstrates how the same coordination primitives can support different interfaces.

**Core API**:
- `Put(key, value)`: store a key-value pair
- `Get(key)`: retrieve the latest value and its revision
- `Delete(key)`: delete a key
- `Txn(compare, success, failure)`: atomic transaction — if compare succeeds, apply success operations; otherwise, apply failure operations
- `Watch(key)`: persistent watch (unlike ZooKeeper's one-shot)

**Txn example** (compare-and-swap):
```
Txn: if value("/leader") == "n1", then Put("/leader", "n2"), else fail
```

```json
Request:  {"type": "etcd_put", "msg_id": 1, "key": "/config/db_host", "value": "10.0.0.5"}
Response: {"type": "etcd_put_ok", "in_reply_to": 1, "revision": 42}

Request:  {"type": "etcd_txn", "msg_id": 2, "compare": {"key": "/leader", "value": "n1"}, "success": [{"op": "put", "key": "/leader", "value": "n2"}], "failure": []}
Response: {"type": "etcd_txn_ok", "in_reply_to": 2, "succeeded": true, "revision": 43}
```

## Concepts

- etcd API
- Get
- Put
- Delete
- Txn
- compare-and-swap

## Hints

- etcd provides a flat key-value API (no hierarchy like ZooKeeper)
- Txn enables atomic compare-and-swap: if condition, then operations, else operations
- Watch is persistent (unlike ZooKeeper one-shot watches)
- Every modification increments a global revision counter
- Implement on top of your existing consensus layer

## Test Cases

### 1. Put and Get roundtrip

etcd_get_ok should return value "v1" and a revision > 0.

Input:

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"etcd_put","msg_id":2,"key":"/k1","value":"v1"}}
{"src":"c1","dest":"n1","body":{"type":"etcd_get","msg_id":3,"key":"/k1"}}
```

Expected output:

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

### 2. Txn succeeds when compare matches

etcd_txn_ok should show succeeded: true.

Input:

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"etcd_put","msg_id":2,"key":"/l","value":"n1"}}
{"src":"c1","dest":"n1","body":{"type":"etcd_txn","msg_id":3,"compare":{"key":"/l","value":"n1"},"success":[{"op":"put","key":"/l","value":"n2"}],"failure":[]}}
```

Expected output:

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

## Resources

- [etcd API](https://etcd.io/docs/v3.5/learning/api/): etcd documentation on the key-value API and transactions

## Java Starter

The matching local starter file is:

```text
src/main/java/Main.java
```
