# Implement Sequence Counter with Overflow Handling

Website: <https://builddistributedsystem.com/tracks/identifier/tasks/task-2-2-3-sequence-counter>

Track: 2. The Identifier
Task order: 8
Short title: Sequence Counter
Difficulty: intermediate
Subtrack: Snowflake IDs (Twitter's Approach)

## Problem

Within a single millisecond, each Snowflake node can generate up to 4096 unique IDs (12-bit sequence counter). When traffic bursts exceed this limit, the generator must handle **sequence overflow** gracefully.

Your task is to implement the sequence counter:

1. Initialize to 0 at the start of each new millisecond
2. Increment by 1 for each ID generated in the same millisecond
3. On overflow (sequence > 4095), spin-wait until the next millisecond, then reset
4. Track maximum sequence reached per millisecond for throughput analysis

Implement a `generate_batch` message that generates N IDs at once:

```json
Request:  {"type": "generate_batch", "msg_id": 1, "count": 10}
Response: {"type": "generate_batch_ok", "in_reply_to": 1, "ids": [1, 2, 3, ...], "max_sequence": 9}
```

All generated IDs must be unique and monotonically increasing.

## Concepts

- sequence number
- overflow handling
- spin wait
- throughput limits

## Hints

- The sequence counter increments for each ID generated in the same millisecond
- Reset the sequence to 0 when moving to a new millisecond
- If the sequence overflows (>4095), wait until the next millisecond
- Spin-waiting is acceptable here since millisecond transitions are fast
- Track the max sequence reached for throughput analysis

## Test Cases

### 1. Single generate works

Should produce a generate_ok with a numeric id.

Input:

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"generate","msg_id":2}}
```

Expected output:

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

### 2. Batch of 5 produces 5 unique IDs

Response should have type generate_batch_ok with ids array of length 5, all unique, and a max_sequence field.

Input:

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"generate_batch","msg_id":2,"count":5}}
```

Expected output:

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

## Resources

- [Globally Unique ID Generation](https://instagram-engineering.com/sharding-ids-at-instagram-1cf5a71e5a5c): Instagram engineering on ID generation at scale

## Java Starter

The matching local starter file is:

```text
src/main/java/Main.java
```
