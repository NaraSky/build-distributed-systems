# Implement Exactly-Once Processing

Website: <https://builddistributedsystem.com/tracks/mapreducer/tasks/task-28-2-5-exactly-once>

Track: 30. The MapReducer
Task order: 10
Short title: Exactly-Once
Difficulty: advanced
Subtrack: Stream Processing

## Problem

Exactly-once processing means each event affects the output exactly once, even when the system retries failed operations. It combines three mechanisms: **deduplication** (skip events already seen), **checkpointing** (save state so recovery can resume), and **transactional output** (commit results atomically).

```
Without exactly-once:
  process "hello"  -> count=1
  (crash, retry)
  process "hello"  -> count=2  <- WRONG, counted twice

With exactly-once (deduplication):
  process "hello" (id=e1)  -> count=1, mark e1 seen
  (crash, retry)
  process "hello" (id=e1)  -> skip (e1 already seen) -> count=1 still correct
```

Your node handles four message types:

```json
// Process an event; skip if event_id was already seen
{ "type": "process", "msg_id": 1,
  "event_id": "e1", "word": "hello" }
-> { "type": "processed", "in_reply_to": 1,
    "word": "hello", "count": 1, "was_duplicate": false }

// Save current state as a named checkpoint
{ "type": "checkpoint", "msg_id": 2, "checkpoint_id": "cp1" }
-> { "type": "checkpoint_saved", "in_reply_to": 2, "checkpoint_id": "cp1" }

// Restore state from a checkpoint
{ "type": "restore", "msg_id": 3, "checkpoint_id": "cp1" }
-> { "type": "restored", "in_reply_to": 3,
    "counts": {"hello": 1} }

// Commit pending outputs atomically
{ "type": "commit", "msg_id": 4 }
-> { "type": "committed", "in_reply_to": 4, "output_count": 1 }
```

## Concepts

- exactly-once
- idempotency
- deduplication
- checkpointing
- transactional commits

## Hints

- Track processed event IDs in a set; skip duplicates silently
- Checkpoint saves the current count state so recovery can resume from it
- restore loads the checkpoint and replaces current state
- commit moves pending outputs to committed atomically; rollback discards them
- At-least-once + idempotency = effectively exactly-once

## Test Cases

### 1. Idempotent processing

Second message with same event_id must be a no-op (count stays at 1).

Input:

```json
{"src":"stream","dest":"processor","body":{"type":"process","msg_id":1,"event_id":"e1","word":"hello"}}
{"src":"stream","dest":"processor","body":{"type":"process","msg_id":2,"event_id":"e1","word":"hello"}}
```

Expected output:

```text
{"type": "processed", "in_reply_to": 1, "word": "hello", "count": 1, "was_duplicate": false}
{"type": "processed", "in_reply_to": 2, "word": "hello", "count": 1, "was_duplicate": true}
```

### 2. Checkpoint and restore

Restore should return the state that was saved at checkpoint time.

Input:

```json
{"src":"stream","dest":"processor","body":{"type":"process","msg_id":1,"event_id":"e1","word":"hello"}}
{"src":"client","dest":"processor","body":{"type":"checkpoint","msg_id":2,"checkpoint_id":"cp1"}}
{"src":"client","dest":"processor","body":{"type":"restore","msg_id":3,"checkpoint_id":"cp1"}}
```

Expected output:

```text
{"type": "processed", "in_reply_to": 1, "word": "hello", "count": 1, "was_duplicate": false}
{"type": "checkpoint_saved", "in_reply_to": 2, "checkpoint_id": "cp1"}
{"type": "restored", "in_reply_to": 3, "counts": {"hello": 1}}
```

## Resources

- [Exactly-Once Semantics in Apache Kafka](https://www.confluent.io/blog/exactly-once-semantics-are-possible-heres-how-apache-kafka-does-it/): How Kafka achieves exactly-once delivery end-to-end

## Java Starter

The matching local starter file is:

```text
src/main/java/Main.java
```
