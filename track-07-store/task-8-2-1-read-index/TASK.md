# Implement Read Index for Linearizable Reads

Website: <https://builddistributedsystem.com/tracks/store/tasks/task-8-2-1-read-index>

Track: 7. The Store
Task order: 6
Short title: Read Index
Difficulty: advanced
Subtrack: Read Optimization

## Problem

Implement the "read index" optimization: the leader records the current commit index, confirms it still leads via heartbeats, then serves the read. Linearizable but no log write needed.

```json
Request:  {"type": "read_index", "msg_id": 1, "key": "x"}
Response: {"type": "read_index_ok", "in_reply_to": 1, "value": "42", "read_at_index": 5, "heartbeat_confirmed": true, "linearizable": true}

Request:  {"type": "read_via_log", "msg_id": 2, "key": "x"}
Response: {"type": "read_via_log_ok", "in_reply_to": 2, "value": "42", "log_index_used": 6, "latency_ms": 15}

Request:  {"type": "compare_read_methods", "msg_id": 3, "num_reads": 100}
Response: {"type": "compare_read_methods_ok", "in_reply_to": 3, "read_index_avg_ms": 2, "read_via_log_avg_ms": 15, "both_linearizable": true}
```

## Concepts

- read index
- linearizable reads
- heartbeat confirmation
- leader lease

## Hints

- Leader records current commitIndex before serving the read
- Leader confirms it still has majority support via a round of heartbeats
- Only after majority responds does the leader serve the read at that commitIndex
- This is linearizable but cheaper than writing the read to the log
- Compare to the naive approach: put every read through the Raft log

## Test Cases

### 1. Read index returns correct value

read_index_ok should show heartbeat_confirmed: true and linearizable: true.

Input:

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1","n2","n3"]}}
{"src":"c1","dest":"n1","body":{"type":"read_index","msg_id":2,"key":"x"}}
```

Expected output:

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

### 2. Compare read methods shows performance difference

read_index_avg_ms should be < read_via_log_avg_ms. both_linearizable: true.

Input:

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1","n2","n3"]}}
{"src":"c1","dest":"n1","body":{"type":"compare_read_methods","msg_id":2,"num_reads":50}}
```

Expected output:

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

## Resources

- [etcd - Linearizable Read](https://etcd.io/docs/v3.5/learning/api_guarantees/): How etcd implements linearizable reads via read index

## Java Starter

The matching local starter file is:

```text
src/main/java/Main.java
```
