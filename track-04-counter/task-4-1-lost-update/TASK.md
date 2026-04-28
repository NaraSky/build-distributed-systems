# Implement Basic Counter with Lost Update Problem

Website: <https://builddistributedsystem.com/tracks/counter/tasks/task-4-1-lost-update>

Track: 4. The Counter
Task order: 1
Short title: Lost Updates
Difficulty: beginner
Subtrack: The Lost Update Problem

## Problem

Implement a basic grow-only counter that handles add and read operations. Multiple nodes share counter state, but your initial implementation will lose updates under concurrency.

This task intentionally demonstrates the lost update problem. Your counter will work for sequential operations but fail verification under concurrent updates from multiple nodes.

## Concept Notes

### The Lost Update Problem

When multiple nodes read, modify, and write state, updates can be lost. Node A reads 5, Node B reads 5, both increment to 6, both write 6. One increment is lost. This is why distributed counters need special handling.

## Concepts

- lost updates
- race conditions
- naive replication

## Hints

- Start with a simple counter
- Notice what happens with concurrent updates
- This task is meant to fail

## Test Cases

### 1. Basic counter add

Input:

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"add","msg_id":2,"delta":5}}
{"src":"c1","dest":"n1","body":{"type":"read","msg_id":3}}
```

Expected output:

```text
{"src":"n1","dest":"c0","body":{"type":"init_ok","in_reply_to":1,"msg_id":0}}
{"src":"n1","dest":"c1","body":{"type":"add_ok","in_reply_to":2,"msg_id":1}}
{"src":"n1","dest":"c1","body":{"type":"read_ok","in_reply_to":3,"msg_id":2,"value":5}}
```

### 2. Sequential increments work

Input:

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"add","msg_id":2,"delta":3}}
{"src":"c2","dest":"n1","body":{"type":"add","msg_id":3,"delta":2}}
{"src":"c3","dest":"n1","body":{"type":"read","msg_id":4}}
```

Expected output:

```text
{"src":"n1","dest":"c0","body":{"type":"init_ok","in_reply_to":1,"msg_id":0}}
{"src":"n1","dest":"c1","body":{"type":"add_ok","in_reply_to":2,"msg_id":1}}
{"src":"n1","dest":"c2","body":{"type":"add_ok","in_reply_to":3,"msg_id":2}}
{"src":"n1","dest":"c3","body":{"type":"read_ok","in_reply_to":4,"msg_id":3,"value":5}}
```

## Resources

- [G-Counter Challenge](https://fly.io/dist-sys/4/): Fly.io grow-only counter challenge

## Java Starter

The matching local starter file is:

```text
src/main/java/Main.java
```
