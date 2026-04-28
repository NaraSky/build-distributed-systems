# Implement LSM Tree

Website: <https://builddistributedsystem.com/tracks/indexes/tasks/task-13-3-lsm-tree>

Track: 13. Indexes
Task order: 3
Short title: LSM Tree
Difficulty: advanced

## Problem

Build a Log-Structured Merge Tree (LSM Tree):

1. Writes go to in-memory memtable (sorted structure)
2. When memtable is full, flush to SSTable on disk
3. SSTables are immutable and sorted
4. Read checks memtable, then each SSTable (newest first)
5. Background compaction merges SSTables

LSM Trees optimize for write throughput by using sequential I/O.

## Concept Notes

### LSM Tree Architecture

LSM Trees batch writes in memory (memtable), then flush sorted runs to disk (SSTables). This converts random writes to sequential writes, dramatically improving write throughput. Systems like Cassandra and RocksDB use LSM Trees.

### Compaction

As SSTables accumulate, reads slow down (must check each file). Compaction merges SSTables, removing deleted keys and combining overlapping ranges. Size-tiered and leveled compaction are common strategies.

## Concepts

- LSM tree
- memtable
- SSTable
- compaction

## Hints

- Write to in-memory memtable first
- Flush to sorted SSTable when full
- Compact SSTables in background

## Test Cases

### 1. LSM write and read

Input:

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"lsm_put","msg_id":2,"key":"x","value":100}}
{"src":"c2","dest":"n1","body":{"type":"lsm_get","msg_id":3,"key":"x"}}
```

Expected output:

```text
{"src":"n1","dest":"c0","body":{"type":"init_ok","in_reply_to":1,"msg_id":0}}
{"src":"n1","dest":"c1","body":{"type":"lsm_put_ok","in_reply_to":2,"msg_id":1}}
{"src":"n1","dest":"c2","body":{"type":"lsm_get_ok","in_reply_to":3,"msg_id":2,"value":100}}
```

## Resources

- [LSM Tree Paper](https://www.cs.umb.edu/~poneil/lsmtree.pdf): The Log-Structured Merge-Tree

## Java Starter

The matching local starter file is:

```text
src/main/java/Main.java
```
