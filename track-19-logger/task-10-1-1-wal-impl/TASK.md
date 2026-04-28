# Implement a Write-Ahead Log

Website: <https://builddistributedsystem.com/tracks/logger/tasks/task-10-1-1-wal-impl>

Track: 19. The Logger
Task order: 1
Short title: WAL Implementation
Difficulty: intermediate
Subtrack: The Commit Log (WAL)

## Problem

The Write-Ahead Log (WAL) is the most fundamental durability primitive in distributed systems. Every database (PostgreSQL, MySQL, SQLite), every consensus algorithm (Raft, Paxos), and every message broker (Kafka) uses a WAL at its core.

The key insight: **log the change BEFORE applying it to state**. If the system crashes at any point, the WAL can be replayed to recover the exact pre-crash state.

Implement a WAL with these properties:
1. **Append-only**: entries are never modified, only appended
2. **Checksummed**: each entry includes a CRC32 checksum to detect corruption
3. **Durable**: entries are fsynced to disk before acknowledging

Entry format: `[4-byte length][4-byte CRC32 checksum][payload bytes]`

```json
Request:  {"type": "wal_append", "msg_id": 1, "payload": "set x=42"}
Response: {"type": "wal_append_ok", "in_reply_to": 1, "offset": 0, "length": 8, "checksum": "abc123"}

Request:  {"type": "wal_read", "msg_id": 2, "offset": 0}
Response: {"type": "wal_read_ok", "in_reply_to": 2, "payload": "set x=42", "checksum_valid": true}

Request:  {"type": "wal_info", "msg_id": 3}
Response: {"type": "wal_info_ok", "in_reply_to": 3, "entries": 1, "total_bytes": 16, "fsynced": true}
```

## Concepts

- write-ahead log
- append-only
- checksum
- durability
- fsync

## Hints

- Each entry format: [4-byte length][4-byte CRC32 checksum][payload bytes]
- Write to disk and fsync BEFORE acknowledging the caller — this is the "write-ahead" guarantee
- The checksum detects torn writes: if a crash happens mid-write, the partial entry will have an invalid checksum
- Use CRC32 for checksums — fast and sufficient for detecting corruption
- The WAL is append-only: never modify existing entries, only add new ones at the end

## Test Cases

### 1. Append a single entry and read it back

Input:

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"wal_append","msg_id":2,"payload":"set x=42"}}
{"src":"c1","dest":"n1","body":{"type":"wal_read","msg_id":3,"offset":0}}
```

Expected output:

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
{"src": "n1", "dest": "c1", "body": {"type": "wal_append_ok", "in_reply_to": 2, "offset": 0, "msg_id": 1}}
{"src": "n1", "dest": "c1", "body": {"type": "wal_read_ok", "in_reply_to": 3, "payload": "set x=42", "checksum_valid": true, "msg_id": 2}}
```

### 2. Multiple appends increment offset

Input:

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"wal_append","msg_id":2,"payload":"op1"}}
{"src":"c1","dest":"n1","body":{"type":"wal_append","msg_id":3,"payload":"op2"}}
{"src":"c1","dest":"n1","body":{"type":"wal_append","msg_id":4,"payload":"op3"}}
{"src":"c1","dest":"n1","body":{"type":"wal_info","msg_id":5}}
```

Expected output:

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
{"src": "n1", "dest": "c1", "body": {"type": "wal_append_ok", "in_reply_to": 2, "offset": 0, "msg_id": 1}}
{"src": "n1", "dest": "c1", "body": {"type": "wal_append_ok", "in_reply_to": 3, "offset": 1, "msg_id": 2}}
{"src": "n1", "dest": "c1", "body": {"type": "wal_append_ok", "in_reply_to": 4, "offset": 2, "msg_id": 3}}
{"src": "n1", "dest": "c1", "body": {"type": "wal_info_ok", "in_reply_to": 5, "entries": 3, "msg_id": 4}}
```

## Resources

- [Write-Ahead Logging - PostgreSQL](https://www.postgresql.org/docs/current/wal-intro.html): PostgreSQL WAL documentation explaining write-ahead logging fundamentals

## Java Starter

The matching local starter file is:

```text
src/main/java/Main.java
```
