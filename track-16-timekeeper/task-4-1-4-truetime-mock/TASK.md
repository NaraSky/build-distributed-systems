# Implement Mock TrueTime API

Website: <https://builddistributedsystem.com/tracks/timekeeper/tasks/task-4-1-4-truetime-mock>

Track: 16. The Timekeeper
Task order: 4
Short title: TrueTime Mock
Difficulty: advanced
Subtrack: Physical Time and Its Failures

## Problem

Google Spanner's TrueTime API returns a time interval instead of a point: `now() -> [earliest, latest]`. The true time is guaranteed to be within this interval.

Implement a mock TrueTime with configurable uncertainty:
```json
Request:  {"type": "truetime_now", "msg_id": 1}
Response: {"type": "truetime_now_ok", "in_reply_to": 1, "earliest": 1234560, "latest": 1234574, "uncertainty_ms": 7}

Request:  {"type": "set_uncertainty", "msg_id": 2, "uncertainty_ms": 10}
Response: {"type": "set_uncertainty_ok", "in_reply_to": 2}
```

## Concepts

- TrueTime
- Google Spanner
- uncertainty interval
- bounded error

## Hints

- TrueTime returns [earliest, latest] instead of a single timestamp
- The uncertainty window is typically ~7ms with GPS/atomic clocks
- earliest = now - uncertainty, latest = now + uncertainty
- Any event that happened at real time T has T within [earliest, latest]
- This is what Google Spanner uses for external consistency

## Test Cases

### 1. TrueTime now returns interval

truetime_now_ok with earliest < latest and uncertainty_ms=7.

Input:

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"truetime_now","msg_id":2}}
```

Expected output:

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

### 2. Set uncertainty

Input:

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"set_uncertainty","msg_id":2,"uncertainty_ms":20}}
```

Expected output:

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
{"src": "n1", "dest": "c1", "body": {"type": "set_uncertainty_ok", "in_reply_to": 2, "msg_id": 1}}
```

## Resources

- [Spanner: Google Globally-Distributed Database](https://research.google/pubs/pub39966/): Original Spanner paper describing TrueTime

## Java Starter

The matching local starter file is:

```text
src/main/java/Main.java
```
