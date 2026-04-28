# Implement Entry Commitment

Website: <https://builddistributedsystem.com/tracks/consensus/tasks/task-6-3-commitment>

Track: 6. The Consensus
Task order: 3
Short title: Commitment
Difficulty: advanced
Subtrack: Raft Log Replication

## Problem

Implement log entry commitment:

1. Leader tracks matchIndex for each follower
2. For each index N, count how many nodes have matchIndex >= N
3. If majority have entry N, and entry N is from current term, commit N
4. Advance commitIndex to highest committed N
5. Notify followers of new commitIndex in next heartbeat

Important: Only commit entries from current term to satisfy the Raft safety property.

## Concept Notes

### Commitment

An entry is committed when the leader knows a majority have it. Committed entries are durable - they will survive leader changes. The leader advances commitIndex when majority confirms.

### Current Term Requirement

Leaders only directly commit entries from their own term. Entries from previous terms are committed indirectly when a current-term entry is committed after them. This prevents a subtle safety violation.

## Concepts

- commitment
- majority
- quorum

## Hints

- Entry committed when on majority
- Use matchIndex to count replicas
- Only commit entries from current term directly

## Test Cases

### 1. Commit on majority replication

Multi-node test: Leader appends entry, waits for majority acks (2 out of 3 nodes), advances commitIndex. Verify entry from current term is committed.

Input:

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
```

Expected output:

```text
{"src":"n1","dest":"c0","body":{"type":"init_ok","in_reply_to":1,"msg_id":0}}
```

## Resources

- [Raft Commitment](https://www.youtube.com/watch?v=YbZ3zDzDnrw): MIT 6.824 Raft lecture

## Java Starter

The matching local starter file is:

```text
src/main/java/Main.java
```
