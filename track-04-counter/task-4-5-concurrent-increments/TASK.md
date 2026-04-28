# Handle Concurrent Increments Across Multiple Nodes

Website: <https://builddistributedsystem.com/tracks/counter/tasks/task-4-5-concurrent-increments>

Track: 4. The Counter
Task order: 5
Short title: Concurrent Updates
Difficulty: advanced
Subtrack: The Lost Update Problem

## Problem

Test your G-Counter under heavy concurrent load. Multiple nodes will simultaneously increment and the final value must equal the sum of all increments.

## Concept Notes

### Eventual Consistency

With proper CRDT implementation, all nodes will eventually converge to the same value. The G-Counter guarantees this even under network partitions and arbitrary message delays.

## Concepts

- concurrent operations
- distributed testing
- verification

## Hints

- Periodically gossip your G-Counter state
- Merge received states into yours
- All nodes should converge to same value

## Test Cases

### 1. Local increments accumulate correctly

Input:

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1","n2","n3"]}}
{"src":"c1","dest":"n1","body":{"type":"add","msg_id":2,"delta":10}}
{"src":"c2","dest":"n1","body":{"type":"add","msg_id":3,"delta":20}}
{"src":"c3","dest":"n1","body":{"type":"add","msg_id":4,"delta":30}}
{"src":"c4","dest":"n1","body":{"type":"read","msg_id":5}}
```

Expected output:

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
{"src": "n1", "dest": "c1", "body": {"type": "add_ok", "in_reply_to": 2, "msg_id": 1}}
{"src": "n1", "dest": "c2", "body": {"type": "add_ok", "in_reply_to": 3, "msg_id": 2}}
{"src": "n1", "dest": "c3", "body": {"type": "add_ok", "in_reply_to": 4, "msg_id": 3}}
{"src": "n1", "dest": "c4", "body": {"type": "read_ok", "value": 60, "in_reply_to": 5, "msg_id": 4}}
```

## Java Starter

The matching local starter file is:

```text
src/main/java/Main.java
```
