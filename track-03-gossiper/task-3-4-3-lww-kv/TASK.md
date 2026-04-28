# Implement Last-Writer-Wins Key-Value Store

Website: <https://builddistributedsystem.com/tracks/gossiper/tasks/task-3-4-3-lww-kv>

Track: 3. The Gossiper
Task order: 18
Short title: LWW KV Store
Difficulty: advanced
Subtrack: Epidemic Algorithms and CRDT Gossip

## Problem

A **Last-Writer-Wins (LWW)** register resolves conflicts by always keeping the value with the latest timestamp. This is simple but can lose concurrent writes.

Implement an LWW key-value store:

```json
Request:  {"type": "write", "msg_id": 1, "key": "x", "value": "hello"}
Response: {"type": "write_ok", "in_reply_to": 1, "ts": 1704067200.123}

Request:  {"type": "kv_read", "msg_id": 2, "key": "x"}
Response: {"type": "kv_read_ok", "in_reply_to": 2, "key": "x", "value": "hello", "ts": 1704067200.123}

Request:  {"type": "kv_merge", "msg_id": 3, "entries": {"x": {"value": "world", "ts": 1704067201.0}}}
Response: {"type": "kv_merge_ok", "in_reply_to": 3, "updated": 1}
```

## Concepts

- LWW register
- conflict resolution
- timestamp ordering
- gossip replication

## Hints

- Each value is paired with a timestamp from when it was written
- On merge, keep the value with the higher timestamp
- If timestamps tie, use a deterministic tiebreaker (e.g., node ID comparison)
- LWW is simple but can silently lose concurrent writes
- Use time.time() for timestamps

## Test Cases

### 1. Write and read back

write_ok with ts, then kv_read_ok with value="hi".

Input:

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"write","msg_id":2,"key":"x","value":"hi"}}
{"src":"c1","dest":"n1","body":{"type":"kv_read","msg_id":3,"key":"x"}}
```

Expected output:

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

### 2. Read missing key returns error

Input:

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"kv_read","msg_id":2,"key":"missing"}}
```

Expected output:

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
{"src": "n1", "dest": "c1", "body": {"type": "error", "code": 20, "text": "Key not found", "in_reply_to": 2, "msg_id": 1}}
```

## Resources

- [Last-Writer-Wins Register](https://en.wikipedia.org/wiki/Conflict-free_replicated_data_type#LWW-Element-Set): Wikipedia on LWW CRDT semantics

## Java Starter

The matching local starter file is:

```text
src/main/java/Main.java
```
