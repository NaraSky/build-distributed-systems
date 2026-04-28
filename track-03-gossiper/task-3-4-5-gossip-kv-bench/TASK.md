# Benchmark Gossip KV Store Performance

Website: <https://builddistributedsystem.com/tracks/gossiper/tasks/task-3-4-5-gossip-kv-bench>

Track: 3. The Gossiper
Task order: 20
Short title: Gossip KV Bench
Difficulty: advanced
Subtrack: Epidemic Algorithms and CRDT Gossip

## Problem

Benchmark your gossip KV store to measure real-world performance characteristics:

1. **Convergence time**: How long until all replicas have the same value?
2. **Message overhead**: How many gossip messages per write operation?
3. **Consistency violations**: How often does a read return stale data?

Implement a `bench_write` that tracks timing:
```json
Request:  {"type": "bench_write", "msg_id": 1, "key": "x", "value": "v1"}
Response: {"type": "bench_write_ok", "in_reply_to": 1, "write_id": 1}
```

And a `bench_report` endpoint:
```json
Request:  {"type": "bench_report", "msg_id": 2}
Response: {"type": "bench_report_ok", "in_reply_to": 2,
           "total_writes": 10, "total_gossip_msgs": 45,
           "msgs_per_write": 4.5, "keys_stored": 5}
```

## Concepts

- benchmarking
- convergence time
- message overhead
- consistency

## Hints

- Track total messages exchanged for gossip sync
- Measure time from write to full convergence (all replicas agree)
- Count consistency violations: reads that return stale data
- Compare metrics under normal vs partition conditions
- Expose metrics via a bench_stats endpoint

## Test Cases

### 1. Bench write returns write_id

Input:

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"bench_write","msg_id":2,"key":"x","value":"v1"}}
```

Expected output:

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
{"src": "n1", "dest": "c1", "body": {"type": "bench_write_ok", "write_id": 1, "in_reply_to": 2, "msg_id": 1}}
```

### 2. Bench report with zero writes

Input:

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"bench_report","msg_id":2}}
```

Expected output:

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
{"src": "n1", "dest": "c1", "body": {"type": "bench_report_ok", "total_writes": 0, "total_gossip_msgs": 0, "msgs_per_write": 0, "keys_stored": 0, "in_reply_to": 2, "msg_id": 1}}
```

## Resources

- [Maelstrom Broadcast Workload](https://github.com/jepsen-io/maelstrom/blob/main/doc/workloads.md#broadcast): Maelstrom broadcast workload specification

## Java Starter

The matching local starter file is:

```text
src/main/java/Main.java
```
