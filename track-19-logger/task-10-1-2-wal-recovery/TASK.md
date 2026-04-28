# Implement WAL Recovery on Startup

Website: <https://builddistributedsystem.com/tracks/logger/tasks/task-10-1-2-wal-recovery>

Track: 19. The Logger
Task order: 2
Short title: WAL Recovery
Difficulty: intermediate
Subtrack: The Commit Log (WAL)

## Problem

WAL recovery is the other half of the durability story. When a node restarts after a crash, it must scan the WAL and replay all valid entries to reconstruct its state.

The recovery algorithm:
1. Open the WAL file and read entries sequentially
2. For each entry, validate the checksum (recompute CRC32 and compare)
3. If the checksum matches, replay the entry (apply the operation to the state machine)
4. If the checksum is invalid, this is a **torn write** — the entry was partially written before the crash. Skip it and all subsequent entries.
5. After replay, the state machine reflects the last consistent state

This is how every database recovers from crashes: PostgreSQL replays its WAL, SQLite replays its journal, and Raft replays its log.

```json
Request:  {"type": "wal_recover", "msg_id": 1, "wal_entries": [
    {"offset": 0, "payload": "set x=1", "checksum": "valid"},
    {"offset": 1, "payload": "set y=2", "checksum": "valid"},
    {"offset": 2, "payload": "set z=", "checksum": "invalid"}
]}
Response: {"type": "wal_recover_ok", "in_reply_to": 1, "entries_replayed": 2, "entries_skipped": 1, "state": {"x": "1", "y": "2"}}
```

## Concepts

- crash recovery
- log replay
- checksum validation
- torn writes
- state reconstruction

## Hints

- On startup, scan the WAL sequentially from the beginning
- For each entry, recompute the CRC32 checksum and compare to the stored one
- Valid entries are replayed to reconstruct state; invalid entries are skipped
- A torn write (crash mid-write) produces a partial entry with an invalid checksum
- After recovery, the state machine is identical to the last consistent pre-crash state

## Test Cases

### 1. Recovery replays valid entries and skips corrupted

Input:

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"wal_recover","msg_id":2,"wal_entries":[{"offset":0,"payload":"set x=1","checksum":"valid"},{"offset":1,"payload":"set y=2","checksum":"valid"},{"offset":2,"payload":"set z=","checksum":"invalid"}]}}
```

Expected output:

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
{"src": "n1", "dest": "c1", "body": {"type": "wal_recover_ok", "in_reply_to": 2, "entries_replayed": 2, "entries_skipped": 1, "msg_id": 1}}
```

### 2. Recovery with all valid entries replays everything

Input:

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"wal_recover","msg_id":2,"wal_entries":[{"offset":0,"payload":"set a=10","checksum":"valid"},{"offset":1,"payload":"set b=20","checksum":"valid"},{"offset":2,"payload":"set c=30","checksum":"valid"}]}}
```

Expected output:

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
{"src": "n1", "dest": "c1", "body": {"type": "wal_recover_ok", "in_reply_to": 2, "entries_replayed": 3, "entries_skipped": 0, "msg_id": 1}}
```

## Resources

- [ARIES Recovery Algorithm](https://en.wikipedia.org/wiki/Algorithms_for_Recovery_and_Isolation_Exploiting_Semantics): The classic ARIES algorithm for WAL-based crash recovery in databases

## Java Starter

The matching local starter file is:

```text
src/main/java/Main.java
```
