# Benchmark LSM Tree vs B-Tree Performance

Website: <https://builddistributedsystem.com/tracks/logger/tasks/task-10-2-5-lsm-bench>

Track: 19. The Logger
Task order: 10
Short title: LSM Benchmark
Difficulty: intermediate
Subtrack: LSM Tree (Log-Structured Merge Tree)

## Problem

The choice between LSM tree and B-Tree is one of the most important storage engine decisions. They represent fundamentally different tradeoffs:

**LSM Tree** (RocksDB, Cassandra, LevelDB):
- Writes are sequential (append to MemTable, flush to SSTable) -> very high write throughput
- Reads may need to check multiple levels -> higher read latency
- Space amplification > 1.0 (old versions exist until compaction)
- Write amplification is high (data rewritten during compaction)

**B-Tree** (PostgreSQL, MySQL InnoDB, SQLite):
- Writes are random I/O (in-place updates) -> lower write throughput
- Reads traverse a balanced tree (O(log N) disk reads) -> lower read latency
- Space amplification ~1.0 (in-place updates, no dead versions)
- Write amplification is lower

Benchmark both engines and measure: write ops/sec, read p50 latency, and space amplification.

```json
Request:  {"type": "lsm_benchmark", "msg_id": 1, "entries": 100000}
Response: {"type": "lsm_benchmark_ok", "in_reply_to": 1, "lsm": {"write_ops_sec": 200000, "read_p50_us": 50, "read_without_bloom_p50_us": 500, "space_amplification": 1.3}, "btree": {"write_ops_sec": 50000, "read_p50_us": 20, "space_amplification": 1.0}}
```

## Concepts

- write throughput
- read latency
- space amplification
- Bloom filter impact
- engine comparison

## Hints

- Measure write throughput: LSM trees excel at sequential inserts (append-only writes)
- Measure read latency with and without Bloom filter — the filter should dramatically reduce disk reads
- Space amplification = total bytes on disk / total bytes of unique data (LSM > 1.0 due to duplicate versions)
- Compare to a naive B-Tree: B-Trees have lower read latency but higher write latency (in-place updates)
- LSM wins for write-heavy workloads; B-Tree wins for read-heavy workloads

## Test Cases

### 1. Full benchmark comparison

lsm_benchmark_ok should include both lsm and btree results. LSM should have higher write_ops_sec, B-Tree should have lower read_p50_us.

Input:

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"lsm_benchmark","msg_id":2,"entries":1000}}
```

Expected output:

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

### 2. Bloom filter impact on reads

LSM read_p50_us should be significantly less than read_without_bloom_p50_us.

Input:

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"lsm_benchmark","msg_id":2,"entries":5000}}
```

Expected output:

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

## Resources

- [Designing Data-Intensive Applications](https://dataintensive.net/): Martin Kleppmann Chapter 3: deep comparison of LSM vs B-Tree storage engine tradeoffs

## Java Starter

The matching local starter file is:

```text
src/main/java/Main.java
```
