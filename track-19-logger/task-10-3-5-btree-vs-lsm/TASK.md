# Compare B-Tree vs LSM Tree with Amplification Metrics

Website: <https://builddistributedsystem.com/tracks/logger/tasks/task-10-3-5-btree-vs-lsm>

Track: 19. The Logger
Task order: 15
Short title: B-Tree vs LSM
Difficulty: intermediate
Subtrack: B-Tree on Disk

## Problem

Choosing between B-Tree and LSM Tree is one of the most important storage engine decisions. They optimize for opposite ends of the read/write spectrum. Understanding the three amplification factors is key:

**Read Amplification** (disk reads per logical read):
- B-Tree: O(log_B(N)) where B is branching factor. Typically 2-4 reads.
- LSM: must check MemTable + L0 (all files) + L1 + L2... Bloom filters help, but worst case checks every level.

**Write Amplification** (bytes written per byte of user data):
- B-Tree: ~2x (read page, modify, write back). With WAL: ~3x.
- LSM: 10-30x. Data is written to MemTable, flushed to L0, then compacted through L1, L2, L3...

**Space Amplification** (disk used / logical data):
- B-Tree: ~1.0 (in-place updates, no dead versions). Some fragmentation from splits.
- LSM: 1.1-1.5 (old versions exist until compacted away).

When to choose each:
- B-Tree: PostgreSQL, MySQL (OLTP, mixed read/write)
- LSM: RocksDB, Cassandra (write-heavy, time series, logging)

```json
Request:  {"type": "btree_vs_lsm", "msg_id": 1, "entries": 100000, "workload": {"read_pct": 50, "write_pct": 50}}
Response: {"type": "btree_vs_lsm_ok", "in_reply_to": 1, "btree": {"write_ops_sec": 50000, "read_ops_sec": 200000, "space_amp": 1.0, "write_amp": 3.0, "read_amp": 1.0}, "lsm": {"write_ops_sec": 200000, "read_ops_sec": 80000, "space_amp": 1.3, "write_amp": 10.0, "read_amp": 3.0}}
```

## Concepts

- performance comparison
- read amplification
- write amplification
- space amplification
- engine selection

## Hints

- Read amplification: how many disk reads per logical read. B-Tree: O(log N). LSM: O(levels * fanout).
- Write amplification: how many bytes written to disk per byte of user data. B-Tree: ~2x. LSM: 10-30x.
- Space amplification: disk space used / logical data size. B-Tree: ~1.0. LSM: 1.1-1.5 (dead versions).
- B-Tree excels for: read-heavy OLTP, point lookups, range scans with buffer pool
- LSM excels for: write-heavy workloads, logging, time series, Kafka-style append-only

## Test Cases

### 1. Compare both engines under mixed workload

LSM should have higher write_ops_sec. B-Tree should have higher read_ops_sec and lower space_amp.

Input:

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"btree_vs_lsm","msg_id":2,"entries":1000,"workload":{"read_pct":50,"write_pct":50}}}
```

Expected output:

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

### 2. Read-heavy workload favors B-Tree

Under read-heavy workload, B-Tree should significantly outperform LSM on read_ops_sec.

Input:

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"btree_vs_lsm","msg_id":2,"entries":1000,"workload":{"read_pct":90,"write_pct":10}}}
```

Expected output:

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

## Resources

- [B-Tree vs LSM Tree Analysis](https://www.usenix.org/system/files/login/articles/login_oct15_05_bender.pdf): Detailed academic analysis of write amplification, read amplification, and space amplification tradeoffs

## Java Starter

The matching local starter file is:

```text
src/main/java/Main.java
```
