# Add WAL Segment Files with Offset Index

Website: <https://builddistributedsystem.com/tracks/logger/tasks/task-10-1-3-segments>

Track: 19. The Logger
Task order: 3
Short title: WAL Segments
Difficulty: advanced
Subtrack: The Commit Log (WAL)

## Problem

A single WAL file has a problem: it grows without bound. Once it reaches gigabytes, seeks become slow and cleanup is impossible without rewriting the entire file.

The solution: **segment files**. When a WAL segment exceeds a size threshold, seal it (make it immutable) and open a new active segment. An offset index enables O(1) lookups by mapping each log offset to the correct segment file and byte position.

This is how Kafka, etcd, and most production systems organize their logs:
1. Segments are named by their starting offset (e.g. `00000000.log`, `00001000.log`)
2. Each segment has a companion `.index` file mapping offset -> byte position
3. Old sealed segments can be deleted, compressed, or archived independently
4. The active segment is the only one receiving new writes

```json
Request:  {"type": "wal_segment_config", "msg_id": 1, "max_segment_bytes": 67108864}
Response: {"type": "wal_segment_config_ok", "in_reply_to": 1, "max_segment_bytes": 67108864}

Request:  {"type": "wal_segment_info", "msg_id": 2}
Response: {"type": "wal_segment_info_ok", "in_reply_to": 2, "segments": [
    {"file": "00000000.log", "start_offset": 0, "end_offset": 999, "size_bytes": 67108000, "sealed": true},
    {"file": "00001000.log", "start_offset": 1000, "end_offset": 1050, "size_bytes": 5120, "sealed": false}
], "active_segment": "00001000.log"}
```

## Concepts

- segment files
- log segmentation
- offset index
- fast seeks
- immutable segments

## Hints

- When the active segment exceeds a size threshold (e.g. 64MB), seal it and open a new one
- Maintain an index mapping (log_offset -> segment_file + byte_offset) for O(1) seeks
- Sealed segments are immutable — they can be safely compressed, archived, or deleted
- Name segments by their starting offset: 00000000.log, 00001000.log, etc.
- This is exactly how Kafka organizes its partition logs on disk

## Test Cases

### 1. Configure segment size threshold

Input:

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"wal_segment_config","msg_id":2,"max_segment_bytes":1024}}
```

Expected output:

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
{"src": "n1", "dest": "c1", "body": {"type": "wal_segment_config_ok", "in_reply_to": 2, "max_segment_bytes": 1024, "msg_id": 1}}
```

### 2. Segment info shows active segment on empty log

wal_segment_info_ok should show at least 1 segment with sealed: false (active).

Input:

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"wal_segment_info","msg_id":2}}
```

Expected output:

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

## Resources

- [Kafka Log Segments](https://kafka.apache.org/documentation/#design_filesystem): How Kafka organizes partition logs into segment files for efficient storage and cleanup

## Java Starter

The matching local starter file is:

```text
src/main/java/Main.java
```
