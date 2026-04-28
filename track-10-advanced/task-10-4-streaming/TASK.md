# Build Stream Processing Pipeline

Website: <https://builddistributedsystem.com/tracks/advanced/tasks/task-10-4-streaming>

Track: 10. Advanced
Task order: 4
Short title: Streaming
Difficulty: intermediate
Subtrack: Advanced Paradigms

## Problem

Build stream processor with windowing. Support tumbling and sliding windows with event-time processing.

## Concept Notes

### Stream Processing

Unlike batch, stream processes data continuously. Windows aggregate over time. Watermarks handle late data in event-time processing.

## Concepts

- streaming
- windowing
- exactly-once

## Hints

- Tumbling vs sliding windows
- Handle late arrivals
- Watermarks for event-time

## Test Cases

### 1. Add event to window

Input:

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"stream_event","msg_id":2,"event":{"data":"click","value":1},"timestamp":5,"window_size":10}}
```

Expected output:

```text
{"src":"n1","dest":"c0","body":{"type":"init_ok","in_reply_to":1,"msg_id":0}}
{"src":"n1","dest":"c1","body":{"type":"stream_event_ok","in_reply_to":2,"msg_id":1,"window_key":0,"window_events":1}}
```

## Resources

- [Streaming 101](https://www.oreilly.com/ideas/the-world-beyond-batch-streaming-101): Streaming concepts

## Java Starter

The matching local starter file is:

```text
src/main/java/Main.java
```
