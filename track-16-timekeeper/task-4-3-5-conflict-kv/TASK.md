# Build a Conflict-Detecting Key-Value Store

Website: <https://builddistributedsystem.com/tracks/timekeeper/tasks/task-4-3-5-conflict-kv>

Track: 16. The Timekeeper
Task order: 15
Short title: Conflict KV
Difficulty: advanced
Subtrack: Vector Clocks

## Problem

Use vector clocks to detect write-write conflicts in a key-value store. When two nodes write to the same key concurrently (neither write causally depends on the other), the store keeps both values as **siblings** (like Amazon DynamoDB).

Conflict rules:
- If write's VC dominates stored VC: simple overwrite
- If stored VC dominates write's VC: reject (stale write)
- If neither dominates (concurrent): store both as siblings

Implement handlers:

```json
Request:  {"type": "kv_put", "msg_id": 1, "key": "user:1", "value": "Alice", "clock": [1, 0]}
Response: {"type": "kv_put_ok", "in_reply_to": 1, "status": "written"}

Request:  {"type": "kv_put", "msg_id": 2, "key": "user:1", "value": "Bob", "clock": [0, 1]}
Response: {"type": "kv_put_ok", "in_reply_to": 2, "status": "conflict", "siblings": 2}

Request:  {"type": "kv_get", "msg_id": 3, "key": "user:1"}
Response: {"type": "kv_get_ok", "in_reply_to": 3, "values": [
    {"value": "Alice", "clock": [1, 0]},
    {"value": "Bob", "clock": [0, 1]}
]}

Request:  {"type": "kv_resolve", "msg_id": 4, "key": "user:1", "value": "Alice+Bob", "clock": [1, 1]}
Response: {"type": "kv_resolve_ok", "in_reply_to": 4, "status": "resolved"}
```

## Concepts

- conflict detection
- write-write conflict
- multi-value register
- DynamoDB style

## Hints

- Each key stores a value along with its vector clock
- On write, compare the incoming vector clock with the stored one
- If the incoming clock dominates the stored clock, overwrite (no conflict)
- If neither dominates, store both values as siblings (write-write conflict)
- On read, return all sibling values so the client can resolve the conflict

## Test Cases

### 1. Simple write to empty key

kv_get_ok should return a single value "hello" with clock [1, 0].

Input:

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"kv_put","msg_id":2,"key":"x","value":"hello","clock":[1,0]}}
{"src":"c1","dest":"n1","body":{"type":"kv_get","msg_id":3,"key":"x"}}
```

Expected output:

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
{"src": "n1", "dest": "c1", "body": {"type": "kv_put_ok", "in_reply_to": 2, "status": "written", "msg_id": 1}}
```

### 2. Concurrent writes create siblings

Second put should return status "conflict" with siblings: 2. Get should return 2 values.

Input:

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"kv_put","msg_id":2,"key":"x","value":"v1","clock":[1,0]}}
{"src":"c1","dest":"n1","body":{"type":"kv_put","msg_id":3,"key":"x","value":"v2","clock":[0,1]}}
{"src":"c1","dest":"n1","body":{"type":"kv_get","msg_id":4,"key":"x"}}
```

Expected output:

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
{"src": "n1", "dest": "c1", "body": {"type": "kv_put_ok", "in_reply_to": 2, "status": "written", "msg_id": 1}}
```

## Resources

- [Dynamo: Amazon Highly Available Key-Value Store](https://www.allthingsdistributed.com/files/amazon-dynamo-sosp2007.pdf): The original Dynamo paper describing vector clock conflict detection

## Java Starter

The matching local starter file is:

```text
src/main/java/Main.java
```
