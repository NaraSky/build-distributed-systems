# Read System Clock and Detect Backward Jumps

Website: <https://builddistributedsystem.com/tracks/timekeeper/tasks/task-4-1-1-clock-read>

Track: 16. The Timekeeper
Task order: 1
Short title: Clock Read
Difficulty: intermediate
Subtrack: Physical Time and Its Failures

## Problem

System clocks can go backward due to NTP adjustments. Your task is to read the clock repeatedly and detect backward jumps.

Implement a `clock_sample` handler that reads the clock N times:
```json
Request:  {"type": "clock_sample", "msg_id": 1, "count": 100, "offset_ms": 0}
Response: {"type": "clock_sample_ok", "in_reply_to": 1, "samples": 100, "backward_jumps": 0, "max_delta_us": 15, "min_delta_us": 1}
```

Also implement `simulate_ntp` to inject a backward offset:
```json
Request:  {"type": "simulate_ntp", "msg_id": 2, "offset_ms": -50}
Response: {"type": "simulate_ntp_ok", "in_reply_to": 2}
```

## Concepts

- system clock
- clock monotonicity
- NTP
- backward jump

## Hints

- Use time.time() for wall clock and time.monotonic() for monotonic clock
- Compare consecutive readings to detect backward jumps
- NTP adjustments can cause the wall clock to jump backward
- Track minimum and maximum deltas between readings
- Store readings in a buffer for analysis

## Test Cases

### 1. Clock sample returns stats

clock_sample_ok should have samples=10 and backward_jumps=0.

Input:

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"clock_sample","msg_id":2,"count":10}}
```

Expected output:

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

### 2. Simulate NTP responds ok

Input:

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"simulate_ntp","msg_id":2,"offset_ms":-50}}
```

Expected output:

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
{"src": "n1", "dest": "c1", "body": {"type": "simulate_ntp_ok", "in_reply_to": 2, "msg_id": 1}}
```

## Resources

- [Falsehoods Programmers Believe About Time](https://infiniteundo.com/post/25326999628/falsehoods-programmers-believe-about-time): Common misconceptions about timekeeping in software

## Java Starter

The matching local starter file is:

```text
src/main/java/Main.java
```
