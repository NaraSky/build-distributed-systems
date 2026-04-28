# Implement Key-Value Interface

Website: <https://builddistributedsystem.com/tracks/store/tasks/task-7-1-kv-interface>

Track: 7. The Store
Task order: 1
Short title: KV Interface
Difficulty: intermediate
Subtrack: Linearizable Key-Value Store

## Problem

Implement the key-value store interface on top of Raft:

1. GET(key) - Return current value or null
2. PUT(key, value) - Set key to value
3. CAS(key, expected, new) - Compare-and-swap

Each write operation:
1. Leader receives request
2. Append to Raft log
3. Wait for commitment
4. Apply to state machine
5. Return result to client

## Concept Notes

### Building on Consensus

Raft provides ordered, replicated log. We build a KV store by interpreting log entries as operations. All nodes apply the same operations in order, producing the same state.

### Maelstrom KV Workloads

Maelstrom tests lin-kv (linearizable KV) and lww-kv (last-write-wins). Linearizable requires waiting for Raft commit. LWW can accept local writes immediately.

## Concepts

- key-value
- API
- operations

## Hints

- Support get, put, cas operations
- Each operation becomes a log entry
- Wait for commit before responding

## Test Cases

### 1. Put and get key

Input:

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"write","msg_id":2,"key":"x","value":1}}
{"src":"c1","dest":"n1","body":{"type":"read","msg_id":3,"key":"x"}}
```

Expected output:

```text
{"src":"n1","dest":"c0","body":{"type":"init_ok","in_reply_to":1,"msg_id":0}}
{"src":"n1","dest":"c1","body":{"type":"write_ok","in_reply_to":2,"msg_id":1}}
{"src":"n1","dest":"c1","body":{"type":"read_ok","in_reply_to":3,"msg_id":2,"value":1}}
```

## Resources

- [Maelstrom KV](https://fly.io/dist-sys/6a/): Fly.io lin-kv challenge

## Java Starter

The matching local starter file is:

```text
src/main/java/Main.java
```
