# Implement Hybrid Logical Clocks

Website: <https://builddistributedsystem.com/tracks/timekeeper/tasks/task-4-4-1-hlc-impl>

Track: 16. The Timekeeper
Task order: 16
Short title: HLC Implementation
Difficulty: intermediate
Subtrack: Hybrid Logical Clocks

## Problem

A Hybrid Logical Clock (HLC) combines the best of physical clocks (real-time proximity) and logical clocks (causal ordering). Used in CockroachDB and Spanner.

HLC format: `(pt, c)` where:
- `pt`: physical time in milliseconds
- `c`: logical counter (bounded, resets when pt advances)

Rules:
- **Local/Send event**: `pt_new = max(pt_local, pt_now)`. If `pt_new == pt_local`, `c += 1`. Else `c = 0`. Set `pt_local = pt_new`.
- **Receive event**: `pt_new = max(pt_local, pt_msg, pt_now)`. Adjust c based on which pt values tied.

Implement handlers:

```json
Request:  {"type": "hlc_tick", "msg_id": 1, "wall_clock_ms": 1000}
Response: {"type": "hlc_tick_ok", "in_reply_to": 1, "pt": 1000, "c": 0}

Request:  {"type": "hlc_tick", "msg_id": 2, "wall_clock_ms": 1000}
Response: {"type": "hlc_tick_ok", "in_reply_to": 2, "pt": 1000, "c": 1}

Request:  {"type": "hlc_tick", "msg_id": 3, "wall_clock_ms": 1005}
Response: {"type": "hlc_tick_ok", "in_reply_to": 3, "pt": 1005, "c": 0}

Request:  {"type": "hlc_recv", "msg_id": 4, "wall_clock_ms": 1003, "remote_pt": 1010, "remote_c": 3}
Response: {"type": "hlc_recv_ok", "in_reply_to": 4, "pt": 1010, "c": 4}
```

## Concepts

- hybrid logical clock
- physical time
- logical counter
- CockroachDB

## Hints

- HLC is a pair: (pt, c) where pt = physical time in ms, c = logical counter
- On local/send event: if pt_now > pt_local, set pt_local = pt_now, c = 0. Else increment c.
- On receive: pt_local = max(pt_local, pt_msg, pt_now). If pt_local stayed the same, increment appropriate c.
- HLC always moves forward, even if the physical clock goes backward
- The logical counter c resets to 0 whenever the physical component advances

## Test Cases

### 1. First tick uses wall clock

Input:

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"hlc_tick","msg_id":2,"wall_clock_ms":1000}}
```

Expected output:

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
{"src": "n1", "dest": "c1", "body": {"type": "hlc_tick_ok", "in_reply_to": 2, "pt": 1000, "c": 0, "msg_id": 1}}
```

### 2. Same wall clock ms increments logical counter

Input:

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"hlc_tick","msg_id":2,"wall_clock_ms":1000}}
{"src":"c1","dest":"n1","body":{"type":"hlc_tick","msg_id":3,"wall_clock_ms":1000}}
{"src":"c1","dest":"n1","body":{"type":"hlc_tick","msg_id":4,"wall_clock_ms":1000}}
```

Expected output:

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
{"src": "n1", "dest": "c1", "body": {"type": "hlc_tick_ok", "in_reply_to": 2, "pt": 1000, "c": 0, "msg_id": 1}}
{"src": "n1", "dest": "c1", "body": {"type": "hlc_tick_ok", "in_reply_to": 3, "pt": 1000, "c": 1, "msg_id": 2}}
{"src": "n1", "dest": "c1", "body": {"type": "hlc_tick_ok", "in_reply_to": 4, "pt": 1000, "c": 2, "msg_id": 3}}
```

## Resources

- [Logical Physical Clocks and Consistent Snapshots](https://cse.buffalo.edu/tech-reports/2014-04.pdf): The original HLC paper by Kulkarni et al.

## Java Starter

The matching local starter file is:

```text
src/main/java/Main.java
```
