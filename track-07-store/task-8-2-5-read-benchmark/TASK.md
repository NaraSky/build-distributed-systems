# Benchmark Read Strategies Under Mixed Workload

Website: <https://builddistributedsystem.com/tracks/store/tasks/task-8-2-5-read-benchmark>

Track: 7. The Store
Task order: 10
Short title: Read Benchmark
Difficulty: intermediate
Subtrack: Read Optimization

## Problem

Benchmark three read strategies under an 80% read / 20% write workload. Measure throughput and latency for each.

```json
Request:  {"type": "read_benchmark", "msg_id": 1, "read_pct": 80, "write_pct": 20, "total_ops": 1000, "strategies": ["linearizable", "lease", "follower"]}
Response: {"type": "read_benchmark_ok", "in_reply_to": 1, "results": [
    {"strategy": "linearizable", "throughput_ops": 2000, "p50_ms": 5, "p99_ms": 20, "consistency": "linearizable"},
    {"strategy": "lease", "throughput_ops": 8000, "p50_ms": 1, "p99_ms": 5, "consistency": "linearizable_if_clocks_correct"},
    {"strategy": "follower", "throughput_ops": 15000, "p50_ms": 0.5, "p99_ms": 2, "consistency": "bounded_staleness"}
]}
```

## Concepts

- throughput benchmark
- read/write ratio
- latency comparison
- scalability

## Hints

- Test with 80% reads, 20% writes workload (common in production)
- Compare: strict linearizable reads vs lease reads vs follower reads
- Linearizable reads have highest latency but strongest guarantees
- Follower reads have lowest latency but weaker guarantees
- Measure throughput (ops/sec) and latency (p50, p99) for each strategy

## Test Cases

### 1. Benchmark all three strategies

Results should show 3 entries. Follower reads should have highest throughput and lowest latency.

Input:

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1","n2","n3"]}}
{"src":"c1","dest":"n1","body":{"type":"read_benchmark","msg_id":2,"read_pct":80,"write_pct":20,"total_ops":100,"strategies":["linearizable","lease","follower"]}}
```

Expected output:

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

## Resources

- [YCSB Benchmark](https://github.com/brianfrankcooper/YCSB): Yahoo Cloud Serving Benchmark for database performance evaluation

## Java Starter

The matching local starter file is:

```text
src/main/java/Main.java
```
