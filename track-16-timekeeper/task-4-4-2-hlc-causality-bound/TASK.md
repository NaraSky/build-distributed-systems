# Prove HLC Preserves Causality Within Epsilon

Website: <https://builddistributedsystem.com/tracks/timekeeper/tasks/task-4-4-2-hlc-causality-bound>

Track: 16. The Timekeeper
Task order: 17
Short title: HLC Causality Bound
Difficulty: advanced
Subtrack: Hybrid Logical Clocks

## Problem

HLC has a critical property: it preserves causality AND stays within a bounded distance (epsilon) of physical time. This is what makes it practical for systems like CockroachDB.

Properties to verify:
1. **Causality**: if event A happened-before event B, then `hlc(A) < hlc(B)`
2. **Bounded drift**: `|hlc.pt - wall_clock| <= epsilon` (use epsilon = 250ms)
3. **NTP resilience**: even if wall clock jumps backward, HLC moves forward

Implement a `hlc_verify_bound` handler that checks the epsilon invariant:

```json
Request:  {"type": "hlc_verify_bound", "msg_id": 1, "epsilon_ms": 250}
Response: {"type": "hlc_verify_bound_ok", "in_reply_to": 1, "within_bound": true, "max_drift_ms": 0}
```

Also implement a `hlc_ntp_correction` handler that simulates a backward clock jump:

```json
Request:  {"type": "hlc_ntp_correction", "msg_id": 2, "old_wall_ms": 2000, "new_wall_ms": 1900}
Response: {"type": "hlc_ntp_correction_ok", "in_reply_to": 2, "hlc_pt": 2000, "hlc_c": 1, "moved_backward": false}
```

## Concepts

- causality preservation
- clock skew bound
- NTP correction
- epsilon bound

## Hints

- HLC always advances: it never goes backward even if physical clock does
- The logical counter c is bounded because pt will eventually catch up
- Epsilon (clock skew bound) limits how far HLC can drift from real time
- Simulate NTP corrections by sending wall_clock_ms values that jump backward
- Verify that HLC timestamp always stays within epsilon of the real wall clock

## Test Cases

### 1. HLC stays within epsilon after normal ticks

hlc_verify_bound_ok should show within_bound: true and max_drift_ms: 0.

Input:

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"hlc_tick","msg_id":2,"wall_clock_ms":1000}}
{"src":"c1","dest":"n1","body":{"type":"hlc_tick","msg_id":3,"wall_clock_ms":1100}}
{"src":"c1","dest":"n1","body":{"type":"hlc_verify_bound","msg_id":4,"epsilon_ms":250}}
```

Expected output:

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

### 2. NTP backward correction does not move HLC backward

Input:

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"hlc_tick","msg_id":2,"wall_clock_ms":2000}}
{"src":"c1","dest":"n1","body":{"type":"hlc_ntp_correction","msg_id":3,"old_wall_ms":2000,"new_wall_ms":1900}}
```

Expected output:

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
{"src": "n1", "dest": "c1", "body": {"type": "hlc_tick_ok", "in_reply_to": 2, "pt": 2000, "c": 0, "msg_id": 1}}
{"src": "n1", "dest": "c1", "body": {"type": "hlc_ntp_correction_ok", "in_reply_to": 3, "hlc_pt": 2000, "hlc_c": 1, "moved_backward": false, "msg_id": 2}}
```

## Resources

- [CockroachDB Architecture - Clock Synchronization](https://www.cockroachlabs.com/docs/stable/architecture/transaction-layer.html): How CockroachDB uses HLC for distributed transaction ordering

## Java Starter

The matching local starter file is:

```text
src/main/java/Main.java
```
