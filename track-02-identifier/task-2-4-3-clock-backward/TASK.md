# HLC Handles Backward Clock Gracefully

Website: <https://builddistributedsystem.com/tracks/identifier/tasks/task-2-4-3-clock-backward>

Track: 2. The Identifier
Task order: 18
Short title: Clock Backward
Difficulty: advanced
Subtrack: Hybrid Logical Clocks (HLC)

## Problem

NTP can adjust the system clock backward. Physical timestamps break. Lamport clocks keep working but lose time correlation. HLC handles it gracefully by keeping its physical component and incrementing the logical counter.

Implement a simulation that demonstrates this:

1. `simulate_clock_backward` sets the HLC's internal notion of "now" backward by a given amount
2. After the backward jump, HLC.tick() should still produce advancing timestamps
3. Report the drift between HLC.pt and actual physical time

```json
Request:  {"type": "simulate_backward", "msg_id": 1, "offset_ms": -5000}
Response: {"type": "simulate_backward_ok", "in_reply_to": 1}
```

Then tick and observe HLC advances despite backward clock:
```json
Request:  {"type": "hlc_tick", "msg_id": 2}
Response: {"type": "hlc_tick_ok", "in_reply_to": 2, "pt": 1234567, "lc": 1, "drift_ms": 5000}
```

The `drift_ms` field shows how far HLC.pt is ahead of the (simulated) physical clock.

## Concepts

- NTP adjustment
- clock backward
- monotonic guarantee
- HLC resilience

## Hints

- When system clock goes backward, HLC keeps its pt and increments lc
- This means HLC never goes backward, preserving ordering
- Lamport clocks also handle this, but lose physical time correlation
- Physical clocks break entirely on backward adjustments
- Track the drift between HLC.pt and actual physical time

## Test Cases

### 1. Simulate backward responds ok

Input:

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"simulate_backward","msg_id":2,"offset_ms":-5000}}
```

Expected output:

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
{"src": "n1", "dest": "c1", "body": {"type": "simulate_backward_ok", "in_reply_to": 2, "msg_id": 1}}
```

### 2. Tick after backward still advances

After first tick (pt=now), simulate -10s backward. Second tick should keep same pt and increment lc, with drift_ms > 0.

Input:

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"hlc_tick","msg_id":2}}
{"src":"c1","dest":"n1","body":{"type":"simulate_backward","msg_id":3,"offset_ms":-10000}}
{"src":"c1","dest":"n1","body":{"type":"hlc_tick","msg_id":4}}
```

Expected output:

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

## Resources

- [NTP and Clock Synchronization](https://en.wikipedia.org/wiki/Network_Time_Protocol): Overview of NTP and why clock backward jumps happen

## Java Starter

The matching local starter file is:

```text
src/main/java/Main.java
```
