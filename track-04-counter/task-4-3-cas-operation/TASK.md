# Implement Compare-And-Swap (CAS) Operation

Website: <https://builddistributedsystem.com/tracks/counter/tasks/task-4-3-cas-operation>

Track: 4. The Counter
Task order: 3
Short title: Compare-And-Swap
Difficulty: intermediate
Subtrack: The Lost Update Problem

## Problem

Implement your counter using Compare-And-Swap (CAS) operations. CAS atomically updates a value only if it matches an expected value, preventing lost updates.

## Concept Notes

### Compare-And-Swap

CAS is the foundation of lock-free algorithms. It atomically checks if a value equals an expected value and, if so, updates it. If the check fails, someone else modified the value and you must retry.

## Concepts

- CAS
- optimistic concurrency
- atomic operations

## Hints

- Read current value, compute new, CAS to update
- Retry on CAS failure
- Handle the race between read and CAS

## Test Cases

### 1. CAS-based counter

Input:

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"add","msg_id":2,"delta":5}}
{"src":"c2","dest":"n1","body":{"type":"read","msg_id":3}}
```

Expected output:

```text
{"src":"n1","dest":"c0","body":{"type":"init_ok","in_reply_to":1,"msg_id":0}}
{"src":"n1","dest":"c1","body":{"type":"add_ok","in_reply_to":2,"msg_id":1}}
{"src":"n1","dest":"c2","body":{"type":"read_ok","in_reply_to":3,"msg_id":2,"value":5}}
```

## Java Starter

The matching local starter file is:

```text
src/main/java/Main.java
```
