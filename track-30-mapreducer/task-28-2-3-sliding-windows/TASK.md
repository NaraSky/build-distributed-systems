# Implement Sliding Windows

Website: <https://builddistributedsystem.com/tracks/mapreducer/tasks/task-28-2-3-sliding-windows>

Track: 30. The MapReducer
Task order: 8
Short title: Sliding Windows
Difficulty: advanced
Subtrack: Stream Processing

## Problem

Tumbling windows are non-overlapping — an event belongs to exactly one window. Sliding windows **overlap**: each event belongs to multiple windows, enabling smooth rolling aggregations like "average latency over the last 5 minutes, updated every minute".

```
window_size=5min, slide=1min

Events at 10:02: ---e1---

Windows containing e1:
  [10:00 - 10:05]  <- window starting at 10:00
  [10:01 - 10:06]  <- window starting at 10:01
  [10:02 - 10:07]  <- window starting at 10:02
```

Your node handles two message types:

```json
// Assign one event to all sliding windows it belongs to
{ "type": "assign", "msg_id": 1,
  "event_timestamp": "2024-01-15T10:02:00Z",
  "current_time":    "2024-01-15T10:03:00Z",
  "window_size_ms":  300000,
  "slide_ms":        60000 }
→ { "type": "assigned", "in_reply_to": 1,
    "windows": [
      {"window_id": "...", "window_start": "2024-01-15T10:00:00Z", "window_end": "2024-01-15T10:05:00Z"},
      {"window_id": "...", "window_start": "2024-01-15T10:01:00Z", "window_end": "2024-01-15T10:06:00Z"},
      {"window_id": "...", "window_start": "2024-01-15T10:02:00Z", "window_end": "2024-01-15T10:07:00Z"}
    ]}

// List all windows active at the given time
{ "type": "active_windows", "msg_id": 2,
  "current_time": "2024-01-15T10:03:00Z",
  "window_size_ms": 300000,
  "slide_ms": 60000 }
→ { "type": "active_windows_result", "in_reply_to": 2, "count": 5 }
```

The key difference from tumbling windows: `window_size_ms / slide_ms` windows are active at any point in time.

## Concepts

- sliding windows
- overlapping windows
- window size
- slide interval
- moving average

## Hints

- An event at time T belongs to every window whose [start, end) contains T
- Window starts: all multiples of slide_ms from (T - window_size_ms) up to T
- Number of windows per event = window_size_ms / slide_ms
- For active_windows, list all windows that overlap with current_time
- Moving average: sum event values across the window, divide by count

## Test Cases

### 1. Assign to sliding windows

Event at 10:02 should belong to 3 overlapping 5-min windows.

Input:

```json
{"src":"stream","dest":"windower","body":{"type":"assign","msg_id":1,"event_timestamp":"2024-01-15T10:02:00Z","current_time":"2024-01-15T10:03:00Z","window_size_ms":300000,"slide_ms":60000}}
```

Expected output:

```text
{"type": "assigned", "in_reply_to": 1, "windows": [{"window_id": "window-1705305600000-1705307400000", "window_start": "2024-01-15T10:00:00Z", "window_end": "2024-01-15T10:05:00Z"}, {"window_id": "window-1705305660000-1705307460000", "window_start": "2024-01-15T10:01:00Z", "window_end": "2024-01-15T10:06:00Z"}, {"window_id": "window-1705305720000-1705307520000", "window_start": "2024-01-15T10:02:00Z", "window_end": "2024-01-15T10:07:00Z"}]}
```

### 2. Count active windows

window_size/slide = 300000/60000 = 5 active windows at any moment.

Input:

```json
{"src":"stream","dest":"windower","body":{"type":"active_windows","msg_id":1,"current_time":"2024-01-15T10:03:00Z","window_size_ms":300000,"slide_ms":60000}}
```

Expected output:

```text
{"type": "active_windows_result", "in_reply_to": 1, "count": 5}
```

## Resources

- [Streaming 102 — The World Beyond Batch](https://www.oreilly.com/ideas/the-world-beyond-batch-streaming-102): Windowing models: tumbling, sliding, and session windows

## Java Starter

The matching local starter file is:

```text
src/main/java/Main.java
```
