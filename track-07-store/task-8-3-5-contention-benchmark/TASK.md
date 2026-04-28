# Benchmark Contended Key Under OCC vs MVCC

Website: <https://builddistributedsystem.com/tracks/store/tasks/task-8-3-5-contention-benchmark>

Track: 7. The Store
Task order: 15
Short title: Contention Benchmark
Difficulty: advanced
Subtrack: Transactions on Raft

## Problem

Benchmark a contended-key scenario: 100 clients all updating the same key simultaneously. Compare OCC vs MVCC in terms of abort rate and throughput.

```json
Request:  {"type": "contention_benchmark", "msg_id": 1, "clients": 100, "key": "hot_key", "ops_per_client": 10, "strategies": ["occ", "mvcc_snapshot", "serializable"]}
Response: {"type": "contention_benchmark_ok", "in_reply_to": 1, "results": [
    {"strategy": "occ", "total_commits": 1000, "total_aborts": 4500, "abort_rate_pct": 81.8, "avg_retries": 4.5, "throughput_commits_sec": 200},
    {"strategy": "mvcc_snapshot", "total_commits": 1000, "total_aborts": 0, "abort_rate_pct": 0, "avg_retries": 0, "throughput_commits_sec": 5000},
    {"strategy": "serializable", "total_commits": 1000, "total_aborts": 900, "abort_rate_pct": 47.4, "avg_retries": 0.9, "throughput_commits_sec": 800}
]}
```

## Concepts

- contention
- abort rate
- throughput
- OCC vs MVCC
- hot key

## Hints

- With 100 clients all updating the same key, OCC will have high abort rates
- MVCC + snapshot isolation allows readers to proceed without blocking
- Serializable isolation aborts conflicting writes
- Measure abort rate, throughput (commits/sec), and average retries
- The hot key scenario is worst-case for OCC

## Test Cases

### 1. Benchmark contended key

contention_benchmark_ok should show OCC with higher abort_rate_pct than MVCC.

Input:

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"contention_benchmark","msg_id":2,"clients":10,"key":"hot_key","ops_per_client":5,"strategies":["occ","mvcc_snapshot"]}}
```

Expected output:

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

## Resources

- [Concurrency Control in Databases](https://15445.courses.cs.cmu.edu/fall2023/slides/16-concurrencycontrol.pdf): CMU 15-445 lecture on concurrency control mechanisms

## Java Starter

The matching local starter file is:

```text
src/main/java/Main.java
```
