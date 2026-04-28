# Implement Happens-Before and Concurrency Detection

Website: <https://builddistributedsystem.com/tracks/timekeeper/tasks/task-4-3-2-happens-before>

Track: 16. The Timekeeper
Task order: 12
Short title: Happens-Before
Difficulty: intermediate
Subtrack: Vector Clocks

## Problem

Vector clocks let you determine the causal relationship between any two events. Given two vector clock stamps `a` and `b`:

- **a happens-before b** (`a -> b`): every element of `a <= b` AND at least one element of `a < b`
- **b happens-before a** (`b -> a`): every element of `b <= a` AND at least one element of `b < a`
- **concurrent** (`a || b`): neither happens-before the other (some elements of a are greater, some of b are greater)

Implement a `compare` handler:

```json
Request:  {"type": "compare", "msg_id": 1, "clock_a": [2, 3, 1], "clock_b": [2, 4, 2]}
Response: {"type": "compare_ok", "in_reply_to": 1, "result": "A_BEFORE_B"}

Request:  {"type": "compare", "msg_id": 2, "clock_a": [3, 1, 0], "clock_b": [1, 3, 0]}
Response: {"type": "compare_ok", "in_reply_to": 2, "result": "CONCURRENT"}

Request:  {"type": "compare", "msg_id": 3, "clock_a": [5, 3, 2], "clock_b": [2, 1, 1]}
Response: {"type": "compare_ok", "in_reply_to": 3, "result": "B_BEFORE_A"}
```

## Concepts

- happens-before
- concurrency detection
- partial order
- causality

## Hints

- A happens-before B if every element of A <= B and at least one is strictly less
- Two events are concurrent if neither happens-before the other
- Implement comparisons as element-wise vector comparison
- Equal vectors mean the same event (not concurrent)
- This is a partial order, not a total order

## Test Cases

### 1. A happens-before B

Input:

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"compare","msg_id":2,"clock_a":[2,3,1],"clock_b":[2,4,2]}}
```

Expected output:

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
{"src": "n1", "dest": "c1", "body": {"type": "compare_ok", "in_reply_to": 2, "result": "A_BEFORE_B", "msg_id": 1}}
```

### 2. Concurrent events detected

Input:

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"compare","msg_id":2,"clock_a":[3,1,0],"clock_b":[1,3,0]}}
```

Expected output:

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
{"src": "n1", "dest": "c1", "body": {"type": "compare_ok", "in_reply_to": 2, "result": "CONCURRENT", "msg_id": 1}}
```

## Resources

- [Detecting Causal Relationships Using Vector Clocks](https://en.wikipedia.org/wiki/Vector_clock): Wikipedia overview of vector clocks and the happens-before relation

## Java Starter

The matching local starter file is:

```text
src/main/java/Main.java
```
