# Vector Clock Conflict Detection in Key-Value Store

Website: <https://builddistributedsystem.com/tracks/identifier/tasks/task-2-3-5-vc-conflict-kv>

Track: 2. The Identifier
Task order: 15
Short title: VC Conflict KV
Difficulty: advanced
Subtrack: Logical Clocks as IDs

## Problem

In databases like Riak, vector clocks detect **write conflicts**. When two clients write to the same key concurrently (neither saw the other's write), the database stores both values as **siblings** instead of silently losing one.

Implement a key-value store with vector clock-based conflict detection:

```json
Write: {"type": "vc_write", "msg_id": 1, "key": "x", "value": "a", "context": {"n1": 0}}
Read:  {"type": "vc_read", "msg_id": 2, "key": "x"}
```

Read response with single value:
```json
{"type": "vc_read_ok", "values": [{"value": "a", "vc": {"n1": 1}}], "siblings": 1}
```

Read response after concurrent writes (conflict):
```json
{"type": "vc_read_ok", "values": [
    {"value": "a", "vc": {"n1": 1}},
    {"value": "b", "vc": {"n2": 1}}
], "siblings": 2}
```

## Concepts

- conflict detection
- key-value store
- sibling values
- last-writer-wins

## Hints

- Each key stores a value paired with the vector clock at write time
- On write, the client provides the vector clock it read (context)
- If the write VC dominates the stored VC, it is a simple update
- If the VCs are concurrent, store both values as siblings
- A read returns all sibling values and their VCs

## Test Cases

### 1. Write and read a single value

Input:

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"vc_write","msg_id":2,"key":"x","value":"hello","context":{}}}
{"src":"c1","dest":"n1","body":{"type":"vc_read","msg_id":3,"key":"x"}}
```

Expected output:

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
{"src": "n1", "dest": "c1", "body": {"type": "vc_write_ok", "key": "x", "vc": {"c1": 1}, "in_reply_to": 2, "msg_id": 1}}
{"src": "n1", "dest": "c1", "body": {"type": "vc_read_ok", "values": [{"value": "hello", "vc": {"c1": 1}}], "siblings": 1, "in_reply_to": 3, "msg_id": 2}}
```

### 2. Read nonexistent key returns empty

Input:

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"vc_read","msg_id":2,"key":"missing"}}
```

Expected output:

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
{"src": "n1", "dest": "c1", "body": {"type": "vc_read_ok", "values": [], "siblings": 0, "in_reply_to": 2, "msg_id": 1}}
```

## Resources

- [Dynamo: Amazon Highly Available Key-Value Store](https://www.allthingsdistributed.com/files/amazon-dynamo-sosp2007.pdf): Amazon Dynamo paper describing vector clock conflict resolution

## Java Starter

The matching local starter file is:

```text
src/main/java/Main.java
```
