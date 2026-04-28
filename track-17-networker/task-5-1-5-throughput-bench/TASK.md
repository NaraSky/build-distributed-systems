# Benchmark Server Throughput and Latency

Website: <https://builddistributedsystem.com/tracks/networker/tasks/task-5-1-5-throughput-bench>

Track: 17. The Networker
Task order: 5
Short title: Throughput Benchmark
Difficulty: intermediate
Subtrack: TCP From Scratch

## Problem

Measure your TCP server's throughput (requests/sec) and latency (p50, p95, p99). Profile where the bottleneck is.

Implement a benchmark framework:

```json
Request:  {"type": "bench_run", "msg_id": 1, "num_requests": 1000, "payload_size_bytes": 64, "concurrency": 10}
Response: {"type": "bench_run_ok", "in_reply_to": 1, "throughput_rps": 5000, "latency_p50_us": 200, "latency_p95_us": 800, "latency_p99_us": 1500, "elapsed_ms": 200}

Request:  {"type": "bench_profile", "msg_id": 2, "num_requests": 100}
Response: {"type": "bench_profile_ok", "in_reply_to": 2, "breakdown": {
    "accept_pct": 5.2,
    "read_pct": 35.1,
    "process_pct": 12.3,
    "write_pct": 32.4,
    "overhead_pct": 15.0
}, "bottleneck": "read"}

Request:  {"type": "bench_sweep", "msg_id": 3, "concurrency_levels": [1, 5, 10, 50, 100]}
Response: {"type": "bench_sweep_ok", "in_reply_to": 3, "results": [
    {"concurrency": 1, "throughput_rps": 1000, "latency_p50_us": 1000},
    {"concurrency": 10, "throughput_rps": 5000, "latency_p50_us": 200}
]}
```

## Concepts

- throughput
- latency percentiles
- p50
- p95
- p99
- profiling
- bottleneck

## Hints

- Throughput = total requests / elapsed time (requests/sec)
- Measure latency for each request, then sort to compute percentiles
- p50 = median, p95 = the latency at the 95th percentile, p99 = at 99th percentile
- Profile where the bottleneck is: accept(), read(), or processing
- Run with varying number of concurrent connections to find saturation point

## Test Cases

### 1. Run basic benchmark

bench_run_ok should include throughput_rps > 0, and latency fields p50 <= p95 <= p99.

Input:

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"bench_run","msg_id":2,"num_requests":100,"payload_size_bytes":64,"concurrency":1}}
```

Expected output:

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

### 2. Profile breakdown sums to 100%

bench_profile_ok breakdown percentages should sum to approximately 100. bottleneck should be one of: accept, read, process, write.

Input:

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"bench_profile","msg_id":2,"num_requests":50}}
```

Expected output:

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

## Resources

- [Latency Numbers Every Programmer Should Know](https://colin-scott.github.io/personal_website/research/interactive_latency.html): Interactive visualization of latency numbers across different system operations

## Java Starter

The matching local starter file is:

```text
src/main/java/Main.java
```
