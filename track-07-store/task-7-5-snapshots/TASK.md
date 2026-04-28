# Implement Log Compaction with Snapshots

Website: <https://builddistributedsystem.com/tracks/store/tasks/task-7-5-snapshots>

Track: 7. The Store
Task order: 5
Short title: Snapshots
Difficulty: advanced
Subtrack: Linearizable Key-Value Store

## Problem

Implement log compaction with snapshots:

1. Periodically snapshot state machine state
2. Record snapshot index and term
3. Discard log entries before snapshot
4. On recovery, restore from snapshot then replay log
5. Send InstallSnapshot to followers that are too far behind

This prevents unbounded log growth.

## Concept Notes

### Log Compaction

The Raft log grows forever as commands arrive. Snapshots compress applied log entries into a compact state representation. Only the snapshot and subsequent log are needed for recovery.

### InstallSnapshot RPC

When a follower is so far behind that leader discarded needed entries, send the snapshot instead. The follower replaces its state with the snapshot and resumes from there.

## Concepts

- snapshot
- log compaction
- recovery

## Hints

- Snapshot state machine periodically
- Discard log entries before snapshot
- Send snapshot to slow followers

## Test Cases

### 1. Create snapshot

Snapshot created with lastIncludedIndex=5, lastIncludedTerm=2, contains state {"x":1,"y":2}

Input:

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c0","dest":"n1","body":{"type":"seed_state","msg_id":2,"state":{"x":1,"y":2},"commit_index":5,"term":2}}
{"src":"c0","dest":"n1","body":{"type":"take_snapshot","msg_id":3,"up_to_index":5}}
```

Expected output:

```text
{"src":"n1","dest":"c0","body":{"type":"init_ok","in_reply_to":1,"msg_id":0}}
{"src":"n1","dest":"c0","body":{"type":"seed_state_ok","in_reply_to":2,"msg_id":1}}
{"src":"n1","dest":"c0","body":{"type":"snapshot_ok","in_reply_to":3,"msg_id":2,"last_included_index":5,"last_included_term":2}}
```

## Resources

- [Raft Section 7](https://raft.github.io/raft.pdf): Log compaction in Raft

## Java Starter

The matching local starter file is:

```text
src/main/java/Main.java
```
