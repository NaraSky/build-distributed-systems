# Benchmark Node Throughput and Latency

Website: <https://builddistributedsystem.com/tracks/messenger/tasks/task-1-3-4-throughput-bench>

Track: 1. The Messenger
Task order: 14
Short title: Throughput Bench
Difficulty: intermediate
Subtrack: The Protocol Beneath

## Problem

How fast is your node? In production systems, you need to measure **throughput** (messages per second) and **latency** (time to process each message). Profiling reveals whether the bottleneck is in parsing, dispatch, or serialization.

Your task is to add benchmarking to your node:

1. Track the timestamp of each incoming message and each outgoing response
2. Compute per-message latency (time from receive to send)
3. Compute overall throughput (messages processed per second)
4. Report statistics via a `bench_stats` message type

```json
Request:  {"type": "bench_stats", "msg_id": 1}
Response: {"type": "bench_stats_ok", "in_reply_to": 1, 
           "total_messages": 100, 
           "elapsed_ms": 523,
           "throughput_per_sec": 191.2,
           "avg_latency_us": 45,
           "p99_latency_us": 120}
```

Additionally implement a `bench_echo` type that is identical to echo but records timing:
```json
Request:  {"type": "bench_echo", "msg_id": 1, "echo": "perf"}
Response: {"type": "bench_echo_ok", "in_reply_to": 1, "echo": "perf", "latency_us": 42}
```

## Concepts

- benchmarking
- throughput
- latency
- profiling
- performance

## Hints

- Track timestamps for each message received and each response sent
- Throughput = total messages / elapsed time
- Latency = time between receiving a message and sending the response
- Use time.monotonic() for accurate elapsed time measurements
- Store latency samples to compute percentiles (p50, p99)

## Test Cases

### 1. Init and echo still work

Input:

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"echo","msg_id":2,"echo":"bench"}}
```

Expected output:

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
{"src": "n1", "dest": "c1", "body": {"type": "echo_ok", "echo": "bench", "in_reply_to": 2, "msg_id": 1}}
```

### 2. Bench echo includes latency_us field

The second output line is a bench_echo_ok with echo="perf" and a latency_us integer field. Exact latency varies so only structure is validated.

Input:

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"bench_echo","msg_id":2,"echo":"perf"}}
```

Expected output:

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

## Resources

- [Latency Numbers Every Programmer Should Know](https://colin-scott.github.io/personal_website/research/interactive_latency.html): Interactive visualization of latency at different system levels

## Java Starter

The matching local starter file is:

```text
src/main/java/Main.java
```
