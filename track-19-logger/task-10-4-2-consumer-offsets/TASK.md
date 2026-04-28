# Implement Consumer Group Offset Tracking

Website: <https://builddistributedsystem.com/tracks/logger/tasks/task-10-4-2-consumer-offsets>

Track: 19. The Logger
Task order: 17
Short title: Consumer Offsets
Difficulty: intermediate
Subtrack: Distributed Log (Kafka Architecture)

## Problem

Consumer offset tracking enables consumers to read at their own pace and resume after restarts. Each consumer group independently tracks its position in each partition.

The offset lifecycle:
1. **Consumer starts**: calls `fetch_offset` to find where it last left off
2. **Consumer reads**: fetches messages starting from its offset
3. **Consumer processes**: performs application logic on the messages
4. **Consumer commits**: calls `commit_offset` to save its new position
5. **Consumer crashes**: on restart, calls `fetch_offset` again and resumes from the last committed offset

This gives **at-least-once delivery**: if a consumer crashes after processing but before committing, it will re-process those messages on restart. For **exactly-once**, additional mechanisms are needed.

Multiple consumer groups can read the same partition independently at different speeds — a key Kafka design principle.

```json
Request:  {"type": "commit_offset", "msg_id": 1, "group": "analytics", "topic": "orders", "partition": 0, "offset": 42}
Response: {"type": "commit_offset_ok", "in_reply_to": 1}

Request:  {"type": "fetch_offset", "msg_id": 2, "group": "analytics", "topic": "orders", "partition": 0}
Response: {"type": "fetch_offset_ok", "in_reply_to": 2, "offset": 42}

Request:  {"type": "fetch_offset", "msg_id": 3, "group": "billing", "topic": "orders", "partition": 0}
Response: {"type": "fetch_offset_ok", "in_reply_to": 3, "offset": 0}
```

## Concepts

- consumer offset
- consumer group
- commit offset
- fetch offset
- at-least-once delivery

## Hints

- Each consumer group maintains an independent offset per partition (their "bookmark")
- commit_offset: client saves its current position after processing messages
- fetch_offset: retrieve where the consumer last left off (for resuming after restart)
- If a consumer crashes before committing, it re-reads from the last committed offset (at-least-once)
- In real Kafka, offsets are stored in a special internal topic (__consumer_offsets)

## Test Cases

### 1. Commit and fetch offset roundtrip

Input:

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"commit_offset","msg_id":2,"group":"g1","topic":"t1","partition":0,"offset":10}}
{"src":"c1","dest":"n1","body":{"type":"fetch_offset","msg_id":3,"group":"g1","topic":"t1","partition":0}}
```

Expected output:

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
{"src": "n1", "dest": "c1", "body": {"type": "commit_offset_ok", "in_reply_to": 2, "msg_id": 1}}
{"src": "n1", "dest": "c1", "body": {"type": "fetch_offset_ok", "in_reply_to": 3, "offset": 10, "msg_id": 2}}
```

### 2. Different groups track independent offsets

Input:

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"commit_offset","msg_id":2,"group":"fast","topic":"t1","partition":0,"offset":100}}
{"src":"c1","dest":"n1","body":{"type":"commit_offset","msg_id":3,"group":"slow","topic":"t1","partition":0,"offset":5}}
{"src":"c1","dest":"n1","body":{"type":"fetch_offset","msg_id":4,"group":"fast","topic":"t1","partition":0}}
{"src":"c1","dest":"n1","body":{"type":"fetch_offset","msg_id":5,"group":"slow","topic":"t1","partition":0}}
```

Expected output:

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
{"src": "n1", "dest": "c1", "body": {"type": "commit_offset_ok", "in_reply_to": 2, "msg_id": 1}}
{"src": "n1", "dest": "c1", "body": {"type": "commit_offset_ok", "in_reply_to": 3, "msg_id": 2}}
{"src": "n1", "dest": "c1", "body": {"type": "fetch_offset_ok", "in_reply_to": 4, "offset": 100, "msg_id": 3}}
{"src": "n1", "dest": "c1", "body": {"type": "fetch_offset_ok", "in_reply_to": 5, "offset": 5, "msg_id": 4}}
```

## Resources

- [Kafka Consumer Offset Management](https://kafka.apache.org/documentation/#impl_offsettracking): How Kafka tracks consumer group offsets using the __consumer_offsets internal topic

## Java Starter

The matching local starter file is:

```text
src/main/java/Main.java
```
