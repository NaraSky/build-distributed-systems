# Implement Exactly-Once Semantics

Website: <https://builddistributedsystem.com/tracks/queues/tasks/task-15-4-exactly-once>

Track: 15. Queues
Task order: 4
Short title: Exactly-Once
Difficulty: advanced
Subtrack: At-Most-Once and At-Least-Once Delivery

## Problem

Achieve exactly-once processing semantics:

Producer side:
1. Assign unique ID to each message
2. Queue deduplicates by ID

Consumer side:
1. Track processed message IDs
2. Skip messages already processed
3. Atomically: process + commit offset + record as processed

This requires cooperation between producer, queue, and consumer.

## Concept Notes

### Exactly-Once Semantics

True exactly-once is end-to-end: exactly-once production + exactly-once consumption + idempotent processing. Kafka achieves this through idempotent producers, transactional consumers, and offset commits within transactions.

### Idempotency Keys

Using unique message IDs, producers retry safely (queue rejects duplicates) and consumers skip already-processed messages. The challenge is tracking and garbage-collecting these IDs efficiently.

## Concepts

- exactly-once
- idempotency
- deduplication

## Hints

- Dedup on producer side with message ID
- Track processed IDs on consumer side
- Use transactions for consume-produce

## Test Cases

### 1. Producer deduplication

Producer sends message with id="msg1" twice (due to retry). Queue should detect duplicate based on message ID and only store once. Verify consumer receives message exactly once, not twice.

Input:

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
```

Expected output:

```text
{"src":"n1","dest":"c0","body":{"type":"init_ok","in_reply_to":1,"msg_id":0}}
```

### 2. Consumer skip duplicate

Consumer processes message id="msg2", stores processed ID. Message is redelivered (due to timeout or crash). Consumer should detect already processed this ID and skip it. Verify idempotent processing on consumer side.

Input:

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
```

Expected output:

```text
{"src":"n1","dest":"c0","body":{"type":"init_ok","in_reply_to":1,"msg_id":0}}
```

## Resources

- [Kafka Exactly-Once](https://www.confluent.io/blog/exactly-once-semantics-are-possible-heres-how-apache-kafka-does-it/): How Kafka achieves exactly-once

## Java Starter

The matching local starter file is:

```text
src/main/java/Main.java
```
