# Handle Out-of-Order Events with Watermarks

Website: <https://builddistributedsystem.com/tracks/mapreducer/tasks/task-28-2-4-watermarks>

Track: 30. The MapReducer
Task order: 9
Short title: Watermarks
Difficulty: advanced
Subtrack: Stream Processing

## Problem

Events in a distributed stream do not always arrive in the order they occurred. A click at 10:00:00 may arrive after a click at 10:00:05 due to network delays. Without handling this, the 10:00:00 event gets dropped when its window has already closed.

**Watermarks** solve this: the watermark represents the point in event time up to which the processor believes it has seen all data. It advances as newer events arrive, and a window only closes once the watermark passes its end boundary.

```
allowed_lateness = 30s

Events arriving:
  10:00:10  -> watermark = 10:00:10 - 30s = 09:59:40
  10:00:30  -> watermark = 10:00:30 - 30s = 10:00:00
  10:00:00  -> LATE (event_time < watermark), window still open -> accepted
  10:01:00  -> watermark = 10:01:00 - 30s = 10:00:30
```

Your node handles two message types:

```json
// Compute the watermark given the max timestamp seen
{ "type": "watermark", "msg_id": 1,
  "max_timestamp": "2024-01-15T10:00:00Z",
  "allowed_lateness_ms": 30000 }
-> { "type": "watermark", "in_reply_to": 1,
    "watermark": "2024-01-15T09:59:30Z" }

// Process an event — determine if it is late or on-time
{ "type": "process", "msg_id": 2,
  "event": {"id": 1},
  "event_time": "2024-01-15T10:00:00Z",
  "watermark":  "2024-01-15T10:00:30Z" }
-> { "type": "late_event", "in_reply_to": 2,
    "event_id": 1, "handled": "dropped" }
```

An event is late when event_time < watermark. Late events are dropped.

## Concepts

- watermarks
- out-of-order events
- event time
- allowed lateness
- late event handling

## Hints

- Watermark = max event timestamp seen so far - allowed_lateness_ms
- An event is late if its event_time < current watermark
- A window closes when the watermark passes window_end
- Late events that fall within a still-open window are accepted; others are dropped
- The watermark only moves forward — it never decreases

## Test Cases

### 1. Generate watermark

Watermark = max_timestamp - allowed_lateness_ms (30s before).

Input:

```json
{"src":"generator","dest":"processor","body":{"type":"watermark","msg_id":1,"max_timestamp":"2024-01-15T10:00:00Z","allowed_lateness_ms":30000}}
```

Expected output:

```text
{"type": "watermark", "in_reply_to": 1, "watermark": "2024-01-15T09:59:30Z"}
```

### 2. Handle late event

event_time 10:00:00 < watermark 10:00:30, so event is late and dropped.

Input:

```json
{"src":"stream","dest":"processor","body":{"type":"process","msg_id":1,"event":{"id":1},"event_time":"2024-01-15T10:00:00Z","watermark":"2024-01-15T10:00:30Z"}}
```

Expected output:

```text
{"type": "late_event", "in_reply_to": 1, "event_id": 1, "handled": "dropped"}
```

## Resources

- [Watermarks in Stream Processing](https://www.oreilly.com/ideas/the-world-beyond-batch-streaming-102): How watermarks enable correct out-of-order event handling

## Java Starter

The matching local starter file is:

```text
src/main/java/Main.java
```
