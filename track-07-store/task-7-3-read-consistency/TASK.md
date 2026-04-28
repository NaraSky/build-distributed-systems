# Ensure Read Consistency

Website: <https://builddistributedsystem.com/tracks/store/tasks/task-7-3-read-consistency>

Track: 7. The Store
Task order: 3
Short title: Read Consistency
Difficulty: advanced
Subtrack: Linearizable Key-Value Store

## Problem

Implement linearizable reads:

Option 1: Log reads (simple but slow)
- Treat reads as log entries, wait for commit

Option 2: ReadIndex (Raft optimization)
- Record current commit index
- Confirm still leader (heartbeat round)
- Wait for commit index to be applied
- Execute read

Option 3: Lease (fast but clock-dependent)

## Concept Notes

### The Stale Read Problem

A leader might be partitioned and not know it. If it serves reads from local state, it returns stale data. Linearizability requires that reads reflect all prior writes.

### ReadIndex

Before serving a read, confirm you are still leader by getting acknowledgment from a majority. Then wait for the commit index at that moment to be applied. This ensures linearizability without logging reads.

## Concepts

- linearizable reads
- read index
- lease

## Hints

- Simple: reads also go through log
- Optimized: confirm leadership before read
- Lease-based: use time bounds

## Test Cases

### 1. Read via log is linearizable

Multi-node test: Write x=1, commit, then read x. Verify read returns 1 and only returns after write is committed (linearizability).

Input:

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
```

Expected output:

```text
{"src":"n1","dest":"c0","body":{"type":"init_ok","in_reply_to":1,"msg_id":0}}
```

## Resources

- [Raft Section 8](https://raft.github.io/raft.pdf): Client interaction in Raft

## Java Starter

The matching local starter file is:

```text
src/main/java/Main.java
```
