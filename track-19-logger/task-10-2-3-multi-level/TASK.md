# Implement a Multi-Level LSM Tree

Website: <https://builddistributedsystem.com/tracks/logger/tasks/task-10-2-3-multi-level>

Track: 19. The Logger
Task order: 8
Short title: Multi-Level LSM
Difficulty: advanced
Subtrack: LSM Tree (Log-Structured Merge Tree)

## Problem

A single flat list of SSTables becomes unmanageable as data grows. The multi-level LSM tree organizes SSTables into levels (L0, L1, L2, ...) with carefully maintained invariants.

Level structure:
- **L0 (special)**: receives direct flushes from MemTable. SSTables may have overlapping key ranges. Reads must check ALL L0 files.
- **L1, L2, ... (sorted levels)**: SSTables within the same level have non-overlapping key ranges. A read only needs to check at most ONE SSTable per level.
- **Size ratio**: each level is ~10x larger than the previous. L0: 40MB, L1: 400MB, L2: 4GB, L3: 40GB.

Read path (multi-level):
1. Check MemTable (newest data)
2. Check L0 (all files, newest first)
3. Check L1 (binary search by key range, at most 1 file)
4. Check L2, L3, ... until found or exhausted

```json
Request:  {"type": "lsm_level_info", "msg_id": 1}
Response: {"type": "lsm_level_info_ok", "in_reply_to": 1, "levels": [
    {"level": 0, "sstables": 4, "total_bytes": 16777216, "sorted": false, "max_bytes": 41943040},
    {"level": 1, "sstables": 5, "total_bytes": 52428800, "sorted": true, "max_bytes": 419430400},
    {"level": 2, "sstables": 10, "total_bytes": 524288000, "sorted": true, "max_bytes": 4194304000}
]}

Request:  {"type": "lsm_read", "msg_id": 2, "key": "user:42"}
Response: {"type": "lsm_read_ok", "in_reply_to": 2, "value": "Alice", "found_at": "L1", "levels_checked": 2}
```

## Concepts

- multi-level LSM
- L0
- L1
- sorted runs
- level policy
- size ratio

## Hints

- L0 contains unsorted SSTables (recent flushes). Reads must check ALL L0 files.
- L1+ levels are sorted by key range with NO overlapping SSTables within a level
- Each level is approximately 10x larger than the previous (size ratio = 10)
- Reads check: MemTable -> L0 (all files) -> L1 -> L2 -> ... until the key is found
- The level selection policy chooses which level to compact based on size limits

## Test Cases

### 1. Level info shows multi-level structure

lsm_level_info_ok should show multiple levels. L0 should have sorted: false, L1+ should have sorted: true.

Input:

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"lsm_level_info","msg_id":2}}
```

Expected output:

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

### 2. Read searches levels in order

lsm_read_ok should include found_at level and levels_checked count.

Input:

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"lsm_read","msg_id":2,"key":"user:42"}}
```

Expected output:

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

## Resources

- [LevelDB Implementation Notes](https://github.com/google/leveldb/blob/main/doc/impl.md): Google LevelDB implementation details explaining multi-level LSM structure

## Java Starter

The matching local starter file is:

```text
src/main/java/Main.java
```
