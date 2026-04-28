# Benchmark WAL fsync Strategies

Website: <https://builddistributedsystem.com/tracks/logger/tasks/task-10-1-5-fsync-bench>

Track: 19. The Logger
Task order: 5
Short title: fsync Benchmark
Difficulty: intermediate
Subtrack: The Commit Log (WAL)

## Problem

The `fsync` system call forces the OS to flush data from kernel buffers to the physical disk. Without it, data that appears "written" may only exist in volatile RAM buffers and will be lost on power failure.

The fundamental tradeoff: **durability vs. throughput**.

Three strategies, from safest to fastest:
1. **Always fsync**: call fsync after every write. Every acknowledged entry is durable. Throughput limited by disk IOPS.
2. **Batch fsync**: buffer writes and fsync every 10ms. Up to 10ms of writes can be lost on crash. 10-30x higher throughput.
3. **No fsync**: let the OS decide when to flush. Crashes can lose seconds of data. 100x+ higher throughput.

Benchmark all three and measure ops/sec, then plot the durability vs. throughput curve.

```json
Request:  {"type": "fsync_benchmark", "msg_id": 1, "entries": 10000, "strategies": ["always", "batch_10ms", "none"]}
Response: {"type": "fsync_benchmark_ok", "in_reply_to": 1, "results": [
    {"strategy": "always", "ops_per_sec": 500, "durability": "every_write", "data_loss_window": "0ms"},
    {"strategy": "batch_10ms", "ops_per_sec": 15000, "durability": "every_10ms", "data_loss_window": "10ms"},
    {"strategy": "none", "ops_per_sec": 100000, "durability": "os_dependent", "data_loss_window": "seconds"}
]}
```

## Concepts

- fsync
- durability
- throughput tradeoff
- batch sync
- OS buffering

## Hints

- Always fsync: every write is durable on disk. Throughput is limited by disk IOPS (~500 ops/sec on HDD)
- Batch fsync every 10ms: group writes and sync once per batch. Good balance — can lose up to 10ms of data
- No fsync: let the OS buffer and flush when it wants. Highest throughput, but crashes can lose seconds of data
- SSDs have much higher fsync throughput than HDDs (~10,000+ ops/sec)
- Production systems like PostgreSQL offer wal_sync_method config to choose the strategy

## Test Cases

### 1. Benchmark all three strategies

Results should show 3 entries with ops_per_sec increasing: always < batch_10ms < none.

Input:

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"fsync_benchmark","msg_id":2,"entries":100,"strategies":["always","batch_10ms","none"]}}
```

Expected output:

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

### 2. Single strategy benchmark

Results should show 1 entry with strategy: "always" and data_loss_window: "0ms".

Input:

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"fsync_benchmark","msg_id":2,"entries":50,"strategies":["always"]}}
```

Expected output:

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

## Resources

- [PostgreSQL WAL Reliability](https://www.postgresql.org/docs/current/wal-reliability.html): PostgreSQL documentation on WAL reliability, fsync, and data integrity

## Java Starter

The matching local starter file is:

```text
src/main/java/Main.java
```
