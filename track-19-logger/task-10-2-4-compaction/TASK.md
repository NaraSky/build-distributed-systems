# Implement LSM Compaction with Merge Sort

Website: <https://builddistributedsystem.com/tracks/logger/tasks/task-10-2-4-compaction>

Track: 19. The Logger
Task order: 9
Short title: LSM Compaction
Difficulty: advanced
Subtrack: LSM Tree (Log-Structured Merge Tree)

## Problem

Compaction is the background process that keeps the LSM tree healthy. Without it, reads degrade because more and more SSTables accumulate, each requiring a disk seek.

The compaction algorithm (leveled compaction):
1. **Trigger**: when L0 exceeds 4 SSTables, or when a level exceeds its size limit
2. **Select**: choose SSTables from the source level whose key ranges overlap with the target level
3. **Merge**: read all selected SSTables, merge-sort by key, deduplicate (keep newest version of each key)
4. **Write**: write new sorted, non-overlapping SSTables to the target level
5. **Cleanup**: delete the old source SSTables

Key metric - **write amplification**: a single user write may be rewritten 10-30x across levels as data is compacted. This is the fundamental cost of LSM trees. RocksDB's leveled compaction has write amplification of approximately `10 * (number_of_levels - 1)`.

```json
Request:  {"type": "lsm_compact", "msg_id": 1, "source_level": 0, "target_level": 1}
Response: {"type": "lsm_compact_ok", "in_reply_to": 1, "sstables_merged": 4, "new_sstables": 2, "keys_deduplicated": 500, "bytes_read": 16000000, "bytes_written": 14000000, "write_amplification": 2.3}

Request:  {"type": "lsm_compact_status", "msg_id": 2}
Response: {"type": "lsm_compact_status_ok", "in_reply_to": 2, "pending_compactions": 0, "total_compactions": 5, "total_bytes_compacted": 100000000}
```

## Concepts

- compaction
- merge sort
- deduplication
- write amplification
- space reclamation

## Hints

- When L0 has >4 SSTables, merge them into L1 (compaction trigger)
- Compaction = merge sort: read overlapping SSTables from both levels, merge by key, write new SSTables to the target level
- Deduplication: if the same key appears in multiple SSTables, keep only the newest version
- Write amplification = total bytes written to disk / total bytes of new data. LSM trees have high write amp (10-30x)
- After compaction, delete the old SSTables that were merged

## Test Cases

### 1. Compact L0 into L1

lsm_compact_ok should show sstables_merged > 0 and write_amplification > 0.

Input:

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"lsm_compact","msg_id":2,"source_level":0,"target_level":1}}
```

Expected output:

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

### 2. Compaction deduplicates keys

keys_deduplicated should be >= 0. bytes_written should be <= bytes_read (deduplication reduces size).

Input:

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"lsm_compact","msg_id":2,"source_level":0,"target_level":1}}
```

Expected output:

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

## Resources

- [RocksDB Compaction](https://github.com/facebook/rocksdb/wiki/Compaction): RocksDB documentation on leveled and universal compaction strategies

## Java Starter

The matching local starter file is:

```text
src/main/java/Main.java
```
