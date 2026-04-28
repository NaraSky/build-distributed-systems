# Integrate Sequentially Consistent Key-Value Store

Website: <https://builddistributedsystem.com/tracks/counter/tasks/task-4-2-kv-integration>

Track: 4. The Counter
Task order: 2
Short title: KV Integration
Difficulty: intermediate
Subtrack: The Lost Update Problem

## Problem

Use Maelstrom's built-in seq-kv service to store your counter value. This provides sequential consistency but introduces new challenges around availability during network partitions.

## Concept Notes

### Sequential Consistency

Sequential consistency guarantees that all operations appear to happen in some total order consistent with each process's local order. This is stronger than eventual consistency but weaker than linearizability.

## Concepts

- sequential consistency
- external storage
- linearizability

## Hints

- Use Maelstrom seq-kv service
- Store counter in external KV
- This still has issues under partitions

## Test Cases

### 1. KV-based counter

Input:

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"add","msg_id":2,"delta":10}}
{"src":"c2","dest":"n1","body":{"type":"read","msg_id":3}}
```

Expected output:

```text
{"src":"n1","dest":"c0","body":{"type":"init_ok","in_reply_to":1,"msg_id":0}}
{"src":"n1","dest":"c1","body":{"type":"add_ok","in_reply_to":2,"msg_id":1}}
{"src":"n1","dest":"c2","body":{"type":"read_ok","in_reply_to":3,"msg_id":2,"value":10}}
```

## Resources

- [Maelstrom Services](https://github.com/jepsen-io/maelstrom/blob/main/doc/services.md): Documentation for Maelstrom built-in services

## Java Starter

The matching local starter file is:

```text
src/main/java/Main.java
```
