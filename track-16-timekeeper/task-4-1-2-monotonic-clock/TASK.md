# Implement Monotonic Clock Wrapper

Website: <https://builddistributedsystem.com/tracks/timekeeper/tasks/task-4-1-2-monotonic-clock>

Track: 16. The Timekeeper
Task order: 2
Short title: Monotonic Clock
Difficulty: intermediate
Subtrack: Physical Time and Its Failures

## Problem

A MonotonicClock wraps the system clock and guarantees the returned value never decreases. Implement this wrapper and track what information is lost.

```json
Request:  {"type": "mono_read", "msg_id": 1}
Response: {"type": "mono_read_ok", "in_reply_to": 1, "time_ms": 1234567, "corrections": 0}
```

## Concepts

- monotonic clock
- clock wrapper
- information loss
- ordering guarantee

## Hints

- Wrap the system clock to always return >= previous value
- Use max(current, last_returned) as the strategy
- Track how many times the wrapper prevented a backward jump
- Information lost: you cannot detect when time actually went backward
- time.monotonic() in Python provides this natively

## Test Cases

### 1. Mono read returns time

mono_read_ok with time_ms > 0 and corrections=0.

Input:

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"mono_read","msg_id":2}}
```

Expected output:

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

### 2. Two reads are non-decreasing

Second time_ms >= first time_ms.

Input:

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"mono_read","msg_id":2}}
{"src":"c1","dest":"n1","body":{"type":"mono_read","msg_id":3}}
```

Expected output:

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

## Resources

- [Monotonic Clocks](https://docs.python.org/3/library/time.html#time.monotonic): Python docs on monotonic clock guarantees

## Java Starter

The matching local starter file is:

```text
src/main/java/Main.java
```
