# Ensure Log Matching Property

Website: <https://builddistributedsystem.com/tracks/consensus/tasks/task-6-2-log-matching>

Track: 6. The Consensus
Task order: 2
Short title: Log Matching
Difficulty: advanced
Subtrack: Raft Log Replication

## Problem

Implement the Log Matching safety property:

On the follower side:
1. Receive AppendEntries with prevLogIndex, prevLogTerm
2. If entry at prevLogIndex has different term, reject
3. If entries conflict with existing, delete from conflict point
4. Append new entries
5. Update commitIndex if leader's is higher

This ensures all committed entries are identical across nodes.

## Concept Notes

### Log Matching Invariant

If two nodes have entries with the same index and term, their logs are identical up to that point. This is achieved by rejecting AppendEntries when prev doesn't match, then backtracking until match is found.

### Conflict Resolution

When logs diverge (after leader changes), the new leader's log wins. Followers truncate conflicting entries and accept the leader's. Committed entries are never truncated - that's the Election Restriction safety.

## Concepts

- log matching
- consistency check
- conflict resolution

## Hints

- Check prevLogIndex and prevLogTerm match
- If conflict, truncate and replace
- Never overwrite committed entries

## Test Cases

### 1. Accept matching entries

Input:

```json
{"src":"c0","dest":"n2","body":{"type":"init","msg_id":1,"node_id":"n2","node_ids":["n1","n2","n3"]}}
{"src":"n1","dest":"n2","body":{"type":"append_entries","msg_id":2,"term":1,"leader_id":"n1","prev_log_index":0,"prev_log_term":0,"entries":[{"term":1,"index":1,"command":{"op":"put","key":"x","value":1}}],"leader_commit":0}}
```

Expected output:

```text
{"src":"n2","dest":"c0","body":{"type":"init_ok","in_reply_to":1,"msg_id":0}}
{"src":"n2","dest":"n1","body":{"type":"append_entries_ok","in_reply_to":2,"msg_id":1,"success":true,"match_index":1}}
```

## Java Starter

The matching local starter file is:

```text
src/main/java/Main.java
```
