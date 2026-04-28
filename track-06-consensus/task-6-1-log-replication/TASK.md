# Implement Log Replication

Website: <https://builddistributedsystem.com/tracks/consensus/tasks/task-6-1-log-replication>

Track: 6. The Consensus
Task order: 1
Short title: Log Replication
Difficulty: advanced
Subtrack: Raft Log Replication

## Problem

Implement Raft log replication from leader to followers:

1. Leader receives client commands, appends to local log
2. Leader sends AppendEntries to all followers
3. AppendEntries includes: prevLogIndex, prevLogTerm, entries[]
4. Follower checks if log matches at prevLogIndex
5. If match, append entries; if not, reject

Track nextIndex and matchIndex per follower to manage replication progress.

## Concept Notes

### The Replicated Log

Raft replicates a log of commands. Each entry has an index and term. The leader appends entries and replicates them. Once a majority have an entry, it is committed and can be applied.

### Log Matching Property

If two logs have an entry with the same index and term, they are identical up to that index. This is guaranteed by: (1) a leader creates at most one entry per index, and (2) AppendEntries consistency check.

## Concepts

- log
- replication
- AppendEntries

## Hints

- Leader maintains log and nextIndex per follower
- AppendEntries carries log entries
- Followers append if log matches

## Test Cases

### 1. Leader appends entry to log

Leader appends entry to log at index 1 with correct term. Replies with raft_append_ok.

Input:

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1","n2","n3"]}}
{"src":"c1","dest":"n1","body":{"type":"raft_append","msg_id":2,"entry":{"term":1,"command":{"op":"put","key":"x","value":1}}}}
```

Expected output:

```text
{"src":"n1","dest":"c0","body":{"type":"init_ok","in_reply_to":1,"msg_id":0}}
{"src":"n1","dest":"c1","body":{"type":"raft_append_ok","in_reply_to":2,"msg_id":1,"index":1}}
```

## Resources

- [Raft Paper Section 5.3](https://raft.github.io/raft.pdf): Log replication in Raft

## Java Starter

The matching local starter file is:

```text
src/main/java/Main.java
```
