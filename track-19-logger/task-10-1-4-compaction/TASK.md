# Implement WAL Compaction with Atomic Snapshot

Website: <https://builddistributedsystem.com/tracks/logger/tasks/task-10-1-4-compaction>

Track: 19. The Logger
Task order: 4
Short title: WAL Compaction
Difficulty: advanced
Subtrack: The Commit Log (WAL)

## Problem

Without compaction, the WAL grows forever. Every database solves this with the same pattern: periodically take a **snapshot** of the state machine, then **truncate** all WAL entries before the snapshot.

The compaction algorithm:
1. Serialize the current state machine to a snapshot file
2. Record the WAL offset at which the snapshot was taken
3. Delete all WAL entries (segments) before that offset
4. On recovery: load the snapshot, then replay only entries after the snapshot offset

The critical requirement: **atomicity**. If the system crashes between taking the snapshot and truncating the WAL, there must be no data loss. The standard approach:
- Write snapshot to a temp file
- Atomically rename the temp file to the final snapshot path
- Only then delete old WAL segments

```json
Request:  {"type": "wal_snapshot", "msg_id": 1}
Response: {"type": "wal_snapshot_ok", "in_reply_to": 1, "snapshot_offset": 500, "snapshot_size_bytes": 2048}

Request:  {"type": "wal_compact", "msg_id": 2, "snapshot_at_offset": 500}
Response: {"type": "wal_compact_ok", "in_reply_to": 2, "snapshot_offset": 500, "entries_before": 1000, "entries_after": 500, "bytes_freed": 32000}
```

## Concepts

- log compaction
- snapshot
- truncation
- atomic operation
- space reclamation

## Hints

- Once a snapshot of the state machine is taken, old WAL entries become unnecessary
- The process: take snapshot -> record snapshot offset -> delete WAL entries before that offset
- The snapshot + truncation MUST be atomic: a crash between them means data loss
- Write the snapshot to a temp file, then atomically rename it into place
- On recovery: load snapshot first, then replay only WAL entries after the snapshot offset

## Test Cases

### 1. Take a snapshot of current state

wal_snapshot_ok should contain snapshot_offset >= 2 and snapshot_size_bytes > 0.

Input:

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"wal_append","msg_id":2,"payload":"set x=1"}}
{"src":"c1","dest":"n1","body":{"type":"wal_append","msg_id":3,"payload":"set y=2"}}
{"src":"c1","dest":"n1","body":{"type":"wal_snapshot","msg_id":4}}
```

Expected output:

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

### 2. Compaction frees old entries

wal_compact_ok should show entries_after < entries_before and bytes_freed > 0.

Input:

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"wal_compact","msg_id":2,"snapshot_at_offset":500}}
```

Expected output:

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

## Resources

- [Log Compaction in Kafka](https://kafka.apache.org/documentation/#compaction): How Kafka implements log compaction to reclaim disk space while keeping latest values

## Java Starter

The matching local starter file is:

```text
src/main/java/Main.java
```
