# Implement a Multi-Value Register (MV-Register)

Website: <https://builddistributedsystem.com/tracks/counter/tasks/task-17-3-2-mv-register>

Track: 4. The Counter
Task order: 12
Short title: MV-Register
Difficulty: advanced
Subtrack: More CRDTs

## Problem

A Multi-Value Register (MV-Register) handles concurrent writes by keeping ALL concurrent values as siblings. The client resolves conflicts on read.

**How it works**:
- Each value is tagged with a vector clock
- `write("v1")` at vector clock {A:1} -> stores ("v1", {A:1})
- `write("v2")` at vector clock {B:1} (concurrent) -> stores ("v2", {B:1})
- `read()` returns ["v1", "v2"] (both siblings, client picks)
- `write("v3")` at vector clock {A:1, B:1} (causally after both) -> replaces both

This is the approach used by Amazon DynamoDB and Riak. It maximizes availability (never rejects a write) at the cost of forcing the client to handle conflicts.

```json
Request:  {"type": "mv_write", "msg_id": 1, "key": "cart", "value": ["item1", "item2"]}
Response: {"type": "mv_write_ok", "in_reply_to": 1, "vclock": {"n1": 1}}

Request:  {"type": "mv_read", "msg_id": 2, "key": "cart"}
Response: {"type": "mv_read_ok", "in_reply_to": 2, "values": [{"value": ["item1", "item2"], "vclock": {"n1": 1}}, {"value": ["item1", "item3"], "vclock": {"n2": 1}}]}
```

## Concepts

- MV-Register
- concurrent writes
- sibling values
- vector clock
- conflict resolution

## Hints

- Each write is tagged with a vector clock timestamp
- Concurrent writes produce multiple sibling values (like DynamoDB)
- On read, return ALL concurrent values — the client resolves the conflict
- A write that causally follows another replaces it (not concurrent)
- Merge: keep all values from concurrent writes, discard causally dominated ones

## Test Cases

### 1. Write and read single value

mv_read_ok values should contain exactly one entry with value "v1".

Input:

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"mv_write","msg_id":2,"key":"k","value":"v1"}}
{"src":"c1","dest":"n1","body":{"type":"mv_read","msg_id":3,"key":"k"}}
```

Expected output:

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

### 2. Concurrent writes produce siblings

mv_read_ok values should contain two siblings: "v1" and "v2".

Input:

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1","n2"]}}
{"src":"c1","dest":"n1","body":{"type":"mv_write","msg_id":2,"key":"k","value":"v1"}}
{"src":"n2","dest":"n1","body":{"type":"mv_merge","msg_id":3,"key":"k","entry":{"value":"v2","vclock":{"n2":1}}}}
{"src":"c1","dest":"n1","body":{"type":"mv_read","msg_id":4,"key":"k"}}
```

Expected output:

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

## Resources

- [DynamoDB Conflict Resolution](https://www.allthingsdistributed.com/files/amazon-dynamo-sosp2007.pdf): DeCandia et al. - Dynamo: Amazon Highly Available Key-value Store

## Java Starter

The matching local starter file is:

```text
src/main/java/Main.java
```
