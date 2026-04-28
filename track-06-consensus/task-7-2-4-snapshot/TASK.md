# Add Snapshot Support for Log Compaction

Website: <https://builddistributedsystem.com/tracks/consensus/tasks/task-7-2-4-snapshot>

Track: 6. The Consensus
Task order: 9
Short title: Snapshots
Difficulty: advanced
Subtrack: Commitment and Application

## Problem

Add snapshot support to compact the Raft log. When the log grows beyond a threshold, take a snapshot of the state machine. Followers that fall behind receive the snapshot instead of individual log entries.

```json
Request:  {"type": "take_snapshot", "msg_id": 1, "threshold": 5}
Response: {"type": "take_snapshot_ok", "in_reply_to": 1, "snapshot_index": 5, "snapshot_term": 2, "state_size_bytes": 256, "log_entries_trimmed": 5}

Request:  {"type": "install_snapshot", "msg_id": 2, "snapshot_index": 5, "snapshot_term": 2, "state": {"x": "1", "y": "2", "z": "3"}}
Response: {"type": "install_snapshot_ok", "in_reply_to": 2, "applied": true, "new_last_applied": 5}

Request:  {"type": "get_log_info", "msg_id": 3}
Response: {"type": "get_log_info_ok", "in_reply_to": 3, "first_index": 6, "last_index": 8, "snapshot_index": 5, "total_entries": 3}
```

## Concepts

- snapshot
- log compaction
- InstallSnapshot RPC
- state transfer

## Hints

- When the log exceeds a threshold (e.g., 1000 entries), take a snapshot of the state machine
- The snapshot captures the full state at a given index and term
- After snapshotting, entries up to that index can be discarded from the log
- Followers that fall too far behind receive the snapshot via InstallSnapshot RPC
- The snapshot replaces the state machine state and log up to snapshot index

## Test Cases

### 1. Take snapshot trims log

take_snapshot_ok should show snapshot_index: 3 and log_entries_trimmed: 3.

Input:

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"apply_entries","msg_id":2,"entries":[{"index":1,"term":1,"command":{"op":"put","key":"x","value":"1"}},{"index":2,"term":1,"command":{"op":"put","key":"y","value":"2"}},{"index":3,"term":1,"command":{"op":"put","key":"z","value":"3"}}]}}
{"src":"c1","dest":"n1","body":{"type":"take_snapshot","msg_id":3,"threshold":2}}
```

Expected output:

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

### 2. Install snapshot restores state

install_snapshot_ok with applied: true. get_state_ok should show state: {"a": "1", "b": "2"}.

Input:

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"install_snapshot","msg_id":2,"snapshot_index":5,"snapshot_term":2,"state":{"a":"1","b":"2"}}}
{"src":"c1","dest":"n1","body":{"type":"get_state","msg_id":3}}
```

Expected output:

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

## Resources

- [Raft - Log Compaction](https://raft.github.io/raft.pdf): Raft paper Section 7 on log compaction and snapshots

## Java Starter

The matching local starter file is:

```text
src/main/java/Main.java
```
