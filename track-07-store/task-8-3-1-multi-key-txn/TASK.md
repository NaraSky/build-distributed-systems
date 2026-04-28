# Implement Multi-Key Transactions as Atomic Log Entries

Website: <https://builddistributedsystem.com/tracks/store/tasks/task-8-3-1-multi-key-txn>

Track: 7. The Store
Task order: 11
Short title: Multi-Key Transactions
Difficulty: advanced
Subtrack: Transactions on Raft

## Problem

Implement multi-key transactions. A transaction is a batch of operations committed as a single log entry for atomicity.

```json
Request:  {"type": "txn_execute", "msg_id": 1, "operations": [
    {"op": "put", "key": "balance_a", "value": "900"},
    {"op": "put", "key": "balance_b", "value": "1100"}
]}
Response: {"type": "txn_execute_ok", "in_reply_to": 1, "committed": true, "log_index": 5, "ops_applied": 2}

Request:  {"type": "txn_execute", "msg_id": 2, "operations": [
    {"op": "get", "key": "balance_a"},
    {"op": "get", "key": "balance_b"}
]}
Response: {"type": "txn_execute_ok", "in_reply_to": 2, "committed": true, "results": [
    {"op": "get", "key": "balance_a", "value": "900"},
    {"op": "get", "key": "balance_b", "value": "1100"}
]}
```

## Concepts

- multi-key transaction
- atomic batch
- log entry
- all-or-nothing

## Hints

- A transaction is a batch of Get/Put/Delete operations committed as a single log entry
- All operations in the batch succeed or fail together (atomicity)
- The batch is serialized as a single command in the Raft log
- The state machine applies all operations in the batch atomically
- If any operation fails validation, the entire batch is rejected

## Test Cases

### 1. Atomic multi-key write

First txn should commit both puts. Second txn should read a: "1" and b: "2".

Input:

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"txn_execute","msg_id":2,"operations":[{"op":"put","key":"a","value":"1"},{"op":"put","key":"b","value":"2"}]}}
{"src":"c1","dest":"n1","body":{"type":"txn_execute","msg_id":3,"operations":[{"op":"get","key":"a"},{"op":"get","key":"b"}]}}
```

Expected output:

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

## Resources

- [TiKV - Distributed Transactions](https://tikv.org/docs/deep-dive/distributed-transaction/introduction/): How TiKV implements distributed transactions on top of Raft

## Java Starter

The matching local starter file is:

```text
src/main/java/Main.java
```
