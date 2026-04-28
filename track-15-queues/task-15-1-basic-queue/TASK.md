# Implement Basic Message Queue

Website: <https://builddistributedsystem.com/tracks/queues/tasks/task-15-1-basic-queue>

Track: 15. Queues
Task order: 1
Short title: Basic Queue
Difficulty: intermediate
Subtrack: At-Most-Once and At-Least-Once Delivery

## Problem

Build a basic in-memory message queue:

1. Producers enqueue messages
2. Consumers dequeue messages
3. Messages delivered in FIFO order
4. Thread-safe for concurrent access
5. Support blocking and non-blocking receive

This decouples producers and consumers in time.

## Concept Notes

### Message Queues

Queues decouple components: producers emit messages without waiting, consumers process at their own pace. This enables asynchronous processing, load leveling, and resilient architectures.

### FIFO Ordering

First-in-first-out ensures messages are processed in send order. This matters for ordered event streams. Strict FIFO limits parallelism - a trade-off to consider.

## Concepts

- queue
- producer-consumer
- FIFO

## Hints

- Use thread-safe data structure
- Block on empty queue or return None
- Handle multiple producers/consumers

## Test Cases

### 1. FIFO order

Enqueue messages in order: m1, m2, m3. Dequeue should return messages in same order: m1, then m2, then m3. Verify FIFO ordering is preserved.

Input:

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
```

Expected output:

```text
{"src":"n1","dest":"c0","body":{"type":"init_ok","in_reply_to":1,"msg_id":0}}
```

### 2. Concurrent access

Multiple producers enqueue concurrently. Multiple consumers dequeue concurrently. Verify queue handles concurrent access safely (no lost messages, no duplicate delivery, thread-safe operations).

Input:

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
```

Expected output:

```text
{"src":"n1","dest":"c0","body":{"type":"init_ok","in_reply_to":1,"msg_id":0}}
```

## Resources

- [Message Queue Patterns](https://www.enterpriseintegrationpatterns.com/patterns/messaging/): Enterprise Integration Patterns

## Java Starter

The matching local starter file is:

```text
src/main/java/Main.java
```
