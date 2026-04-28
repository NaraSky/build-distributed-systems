# Implement an In-Memory MemTable

Website: <https://builddistributedsystem.com/tracks/logger/tasks/task-10-2-1-memtable>

Track: 19. The Logger
Task order: 6
Short title: MemTable
Difficulty: intermediate
Subtrack: LSM Tree (Log-Structured Merge Tree)

## Problem

The MemTable is the entry point for all writes in an LSM tree. It is an in-memory sorted data structure (typically a skip list or red-black tree) that acts as a write buffer.

How it works in the LSM write path:
1. **Write**: insert the key-value pair into the MemTable (O(log N))
2. **Read**: check the MemTable first. If the key is found, return it immediately (freshest data). If not, check SSTables on disk.
3. **Flush**: when the MemTable exceeds a size threshold (e.g. 4MB), freeze it, create a new empty MemTable for new writes, and flush the frozen one to disk as an immutable SSTable.

The MemTable must support:
- `put(key, value)` — insert or update
- `get(key)` — point lookup
- `scan(start, end)` — range scan (sorted iteration)

```json
Request:  {"type": "memtable_put", "msg_id": 1, "key": "user:1", "value": "Alice"}
Response: {"type": "memtable_put_ok", "in_reply_to": 1, "size_bytes": 64}

Request:  {"type": "memtable_get", "msg_id": 2, "key": "user:1"}
Response: {"type": "memtable_get_ok", "in_reply_to": 2, "value": "Alice", "source": "memtable"}

Request:  {"type": "memtable_scan", "msg_id": 3, "start": "user:1", "end": "user:5"}
Response: {"type": "memtable_scan_ok", "in_reply_to": 3, "entries": [
    {"key": "user:1", "value": "Alice"},
    {"key": "user:3", "value": "Bob"}
]}
```

## Concepts

- MemTable
- sorted tree
- skip list
- write path
- in-memory buffer

## Hints

- All writes go to the MemTable first — it is the "write buffer" of the LSM tree
- Use a sorted data structure (skip list or red-black tree) for O(log N) inserts and sorted iteration
- Reads check the MemTable BEFORE checking any on-disk SSTables (freshest data wins)
- When the MemTable exceeds a threshold (e.g. 4MB), it is frozen and flushed to disk as an SSTable
- The MemTable supports range scans because it is sorted — unlike a hash map

## Test Cases

### 1. Put and get from memtable

Input:

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"memtable_put","msg_id":2,"key":"k1","value":"v1"}}
{"src":"c1","dest":"n1","body":{"type":"memtable_get","msg_id":3,"key":"k1"}}
```

Expected output:

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
{"src": "n1", "dest": "c1", "body": {"type": "memtable_put_ok", "in_reply_to": 2, "msg_id": 1}}
{"src": "n1", "dest": "c1", "body": {"type": "memtable_get_ok", "in_reply_to": 3, "value": "v1", "source": "memtable", "msg_id": 2}}
```

### 2. Get for missing key returns null

Input:

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"memtable_get","msg_id":2,"key":"nonexistent"}}
```

Expected output:

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
{"src": "n1", "dest": "c1", "body": {"type": "memtable_get_ok", "in_reply_to": 2, "value": null, "source": "memtable", "msg_id": 1}}
```

## Resources

- [LSM Tree MemTable](https://www.scylladb.com/glossary/memtable/): How memtables work as the in-memory write buffer in LSM-based storage engines

## Java Starter

The matching local starter file is:

```text
src/main/java/Main.java
```
