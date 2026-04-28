# Implement Message Deduplication with LRU Cache

Website: <https://builddistributedsystem.com/tracks/messenger/tasks/task-1-3-3-deduplication>

Track: 1. The Messenger
Task order: 13
Short title: Deduplication
Difficulty: intermediate
Subtrack: The Protocol Beneath

## Problem

Networks can duplicate messages. If a sender retries because it did not receive an acknowledgment (but the original was actually delivered), the receiver sees the same request twice. Without **deduplication**, the receiver processes it twice, which can cause incorrect state.

Your task is to implement message deduplication:

1. Maintain a bounded **LRU cache** of recently seen message IDs (capacity: 1000)
2. The deduplication key is `(src, msg_id)` — msg_id alone is not globally unique
3. When a duplicate is detected, skip processing but still reply (to ensure the sender's retry gets acknowledged)
4. Track and report deduplication statistics

Implement a `dedup_echo` message type that behaves like echo but applies deduplication:

```json
Request:  {"type": "dedup_echo", "msg_id": 5, "echo": "hello"}
Response: {"type": "dedup_echo_ok", "in_reply_to": 5, "echo": "hello", "was_duplicate": false}
```

If the same `(src, msg_id)` pair is seen again:
```json
Response: {"type": "dedup_echo_ok", "in_reply_to": 5, "echo": "hello", "was_duplicate": true}
```

Implement a `dedup_stats` message to report statistics:
```json
Response: {"type": "dedup_stats_ok", "total": 10, "duplicates": 2, "cache_size": 8}
```

## Concepts

- idempotency
- deduplication
- LRU cache
- at-most-once delivery

## Hints

- Use (src, msg_id) as the deduplication key since msg_id is only unique per sender
- An OrderedDict works well as a bounded LRU cache in Python
- When the cache exceeds its capacity, remove the oldest entry
- Skip processing for duplicate messages but still acknowledge receipt
- Log duplicates to stderr for debugging

## Test Cases

### 1. First dedup_echo is not a duplicate

Input:

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"dedup_echo","msg_id":10,"echo":"first"}}
```

Expected output:

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
{"src": "n1", "dest": "c1", "body": {"type": "dedup_echo_ok", "echo": "first", "was_duplicate": false, "in_reply_to": 10, "msg_id": 1}}
```

### 2. Duplicate msg_id from same source detected

Input:

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"dedup_echo","msg_id":10,"echo":"hello"}}
{"src":"c1","dest":"n1","body":{"type":"dedup_echo","msg_id":10,"echo":"hello"}}
```

Expected output:

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
{"src": "n1", "dest": "c1", "body": {"type": "dedup_echo_ok", "echo": "hello", "was_duplicate": false, "in_reply_to": 10, "msg_id": 1}}
{"src": "n1", "dest": "c1", "body": {"type": "dedup_echo_ok", "echo": "hello", "was_duplicate": true, "in_reply_to": 10, "msg_id": 2}}
```

## Resources

- [Exactly-Once Delivery in Distributed Systems](https://www.confluent.io/blog/exactly-once-semantics-are-possible-heres-how-apache-kafka-does-it/): Confluent blog on deduplication and exactly-once semantics in Kafka

## Java Starter

The matching local starter file is:

```text
src/main/java/Main.java
```
