# Implement Tumbling Windows

Website: <https://builddistributedsystem.com/tracks/mapreducer/tasks/task-28-2-2-tumbling-windows>

Track: 30. The MapReducer
Task order: 7
Short title: Tumbling Windows
Difficulty: intermediate
Subtrack: Stream Processing

## Problem

Tumbling windows divide an infinite stream into fixed-size, **non-overlapping** time buckets. Each event belongs to exactly one window. When the window period ends, you emit the aggregate and start a fresh window.

```
Events:  e1(10:00:10)  e2(10:00:40)  e3(10:01:15)  e4(10:01:50)
Windows: [---- 10:00 - 10:01 ----]   [---- 10:01 - 10:02 ----]
         e1, e2  →  count=2           e3, e4  →  count=2
```

Your node handles three message types:

```json
// Assign a single event to its window (window_size_ms = 60000 → 1-minute windows)
{ "type": "assign", "msg_id": 1,
  "events": [{"id":1,"timestamp":"2024-01-15T10:00:10Z"}],
  "window_size_ms": 60000 }
→ { "type": "assigned", "in_reply_to": 1,
    "window_id": "window-1705305600000",
    "window_start": "2024-01-15T10:00:00Z",
    "window_end":   "2024-01-15T10:01:00Z" }

// Process a stream of events and return window aggregates
{ "type": "process_window", "msg_id": 2,
  "events": [
    {"id":1,"timestamp":"2024-01-15T10:00:10Z"},
    {"id":2,"timestamp":"2024-01-15T10:00:40Z"},
    {"id":3,"timestamp":"2024-01-15T10:01:15Z"}
  ],
  "window_size_ms": 60000 }
→ { "type": "window_result", "in_reply_to": 2,
    "windows": [
      {"window_id":"window-1705305600000","count":2,"events":[1,2]},
      {"window_id":"window-1705305660000","count":1,"events":[3]}
    ]}
```

Window ID formula: `floor(timestamp_ms / window_size_ms) * window_size_ms`

## Concepts

- tumbling windows
- time-based windows
- window aggregation
- non-overlapping windows
- event time

## Hints

- Window ID = floor(event_timestamp_ms / window_size_ms) * window_size_ms
- Each event belongs to exactly one window — windows never overlap
- Window end = window_start + window_size_ms
- Aggregate events per window_id: keep a count and list of events
- close emits the result for a window and removes it from active state

## Test Cases

### 1. Assign events to windows

Should assign event to correct 1-minute tumbling window.

Input:

```json
{"src":"stream","dest":"windower","body":{"type":"assign","msg_id":1,"events":[{"id":1,"timestamp":"2024-01-15T10:00:10Z"}],"window_size_ms":60000}}
```

Expected output:

```text
{"type": "assigned", "in_reply_to": 1, "window_id": "window-1705305600000", "window_start": "2024-01-15T10:00:00Z", "window_end": "2024-01-15T10:01:00Z"}
```

### 2. Process multiple windows

Should group events into two separate 1-minute windows.

Input:

```json
{"src":"stream","dest":"windower","body":{"type":"process_window","msg_id":1,"events":[{"id":1,"timestamp":"2024-01-15T10:00:10Z"},{"id":2,"timestamp":"2024-01-15T10:00:40Z"},{"id":3,"timestamp":"2024-01-15T10:01:15Z"}],"window_size_ms":60000}}
```

Expected output:

```text
{"type": "window_result", "in_reply_to": 1, "windows": [{"window_id": "window-1705305600000", "count": 2, "events": [1, 2]}, {"window_id": "window-1705305660000", "count": 1, "events": [3]}]}
```

## Resources

- [Streaming 102 — The World Beyond Batch](https://www.oreilly.com/ideas/the-world-beyond-batch-streaming-102): Covers windowing models including tumbling windows

## Java Starter

The matching local starter file is:

```text
src/main/java/Main.java
```
