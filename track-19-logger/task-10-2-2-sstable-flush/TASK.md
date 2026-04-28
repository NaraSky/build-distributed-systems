# Implement SSTable Flush with Bloom Filter

Website: <https://builddistributedsystem.com/tracks/logger/tasks/task-10-2-2-sstable-flush>

Track: 19. The Logger
Task order: 7
Short title: SSTable Flush
Difficulty: advanced
Subtrack: LSM Tree (Log-Structured Merge Tree)

## Problem

When the in-memory MemTable exceeds its size threshold, it must be persisted to disk as an SSTable (Sorted String Table). The SSTable is a fundamental building block of LSM trees, used in RocksDB, Cassandra, LevelDB, and HBase.

SSTable properties:
1. **Sorted**: keys are stored in lexicographic order, enabling efficient range scans and merge operations
2. **Immutable**: once written, an SSTable is never modified (append-only philosophy)
3. **Bloom filter**: a probabilistic data structure attached to each SSTable that answers "is this key possibly in this file?" with no false negatives
4. **Sparse index**: samples every Nth key to enable fast binary search within the file

The flush process:
1. Freeze the current MemTable (stop writes to it, create a new MemTable for incoming writes)
2. Sort the frozen MemTable entries by key
3. Write them sequentially to a new SSTable file
4. Build the Bloom filter and sparse index
5. Write the footer (Bloom filter + index) and close the file

```json
Request:  {"type": "sstable_flush", "msg_id": 1, "memtable_size_bytes": 4194304}
Response: {"type": "sstable_flush_ok", "in_reply_to": 1, "sstable_file": "L0_001.sst", "entries": 50000, "bloom_filter_bits": 480000, "size_bytes": 4000000}

Request:  {"type": "sstable_lookup", "msg_id": 2, "sstable": "L0_001.sst", "key": "user:42"}
Response: {"type": "sstable_lookup_ok", "in_reply_to": 2, "found": true, "value": "Alice", "bloom_checked": true, "disk_reads": 2}
```

## Concepts

- SSTable
- flush
- Bloom filter
- immutable file
- sorted strings

## Hints

- When the MemTable exceeds 4MB, sort its entries and flush to an immutable SSTable file on disk
- SSTable format: sorted key-value pairs followed by an index block and a Bloom filter footer
- The Bloom filter enables O(1) negative lookups: "this key is definitely NOT in this SSTable"
- SSTables are immutable once written — they are never modified, only eventually merged in compaction
- Each SSTable also has a sparse index: sample every Nth key for fast binary search within the file

## Test Cases

### 1. Flush creates SSTable with metadata

sstable_flush_ok should include sstable_file name, entries count, and bloom_filter_bits > 0.

Input:

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"sstable_flush","msg_id":2,"memtable_size_bytes":4194304}}
```

Expected output:

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

### 2. Lookup existing key in SSTable

sstable_lookup_ok should show bloom_checked: true.

Input:

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"sstable_flush","msg_id":2,"memtable_size_bytes":1024}}
{"src":"c1","dest":"n1","body":{"type":"sstable_lookup","msg_id":3,"sstable":"L0_001.sst","key":"user:42"}}
```

Expected output:

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

## Resources

- [SSTable and Log Structured Storage](https://www.igvita.com/2012/02/06/sstable-and-log-structured-storage-leveldb/): How SSTables work in LevelDB and LSM tree storage engines

## Java Starter

The matching local starter file is:

```text
src/main/java/Main.java
```
