# Build Transactional Key-Value Store

Website: <https://builddistributedsystem.com/tracks/coordinator/tasks/task-9-5-txn-kv>

Track: 9. The Coordinator
Task order: 5
Short title: Txn KV
Difficulty: advanced
Subtrack: Two-Phase Commit

## Problem

Transactional KV: begin, read, write, commit/abort. Use 2PC for cross-shard transactions.

## Concept Notes

### ACID

Atomic, Consistent, Isolated, Durable. Distributed transactions harder due to network partitions.

## Concepts

- transactions
- ACID
- isolation

## Hints

- Multi-key transactions
- Use 2PC for cross-shard
- Read-your-writes

## Test Cases

### 1. Begin transaction

Response contains txn_begin_ok with a unique transaction ID. Transaction should be in active state.

Input:

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"txn_begin","msg_id":2}}
```

Expected output:

```text
{"src":"n1","dest":"c0","body":{"type":"init_ok","in_reply_to":1,"msg_id":0}}
{"src":"n1","dest":"c1","body":{"type":"txn_begin_ok","in_reply_to":2,"msg_id":1,"tx_id":"tx1"}}
```

## Java Starter

The matching local starter file is:

```text
src/main/java/Main.java
```
