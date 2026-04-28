# Implement At-Least-Once Delivery

Website: <https://builddistributedsystem.com/tracks/queues/tasks/task-15-3-at-least-once>

Track: 15. Queues
Task order: 3
Short title: At-Least-Once
Difficulty: intermediate
Subtrack: At-Most-Once and At-Least-Once Delivery

## Problem

Guarantee at-least-once delivery:

1. Consumer receives message (not removed from queue)
2. Message marked as "in-flight" with timestamp
3. Consumer processes and sends acknowledgment
4. Queue removes message on ack
5. If no ack within timeout, redeliver message

Consumer must be idempotent to handle potential duplicates.

## Concept Notes

### At-Least-Once Delivery

At-least-once means every message is delivered at least once, possibly more. If an ack is lost, the message is redelivered. This requires idempotent consumers that handle duplicates gracefully.

### Visibility Timeout

When a consumer receives a message, it becomes invisible to others for a timeout period. If not acknowledged, it reappears. This prevents multiple consumers processing the same message simultaneously.

## Concepts

- at-least-once
- acknowledgment
- redelivery

## Hints

- Do not remove until acknowledged
- Redeliver after timeout
- Track in-flight messages

## Test Cases

### 1. Redeliver on timeout

Consumer receives message m1 with 1s ack timeout. Consumer does not send ack within timeout. After timeout, message should be redelivered to same or different consumer. Verify message is not lost and redelivered at-least-once.

Input:

```json
{"src":"c0","dest":"queue","body":{"type":"init","msg_id":1,"node_id":"queue","node_ids":["queue"]}}
{"src":"producer","dest":"queue","body":{"type":"enqueue","msg_id":2,"message_id":"m1","value":"hello"}}
{"src":"consumer","dest":"queue","body":{"type":"dequeue","msg_id":3,"ack_timeout":1000}}
```

## Java Starter

The matching local starter file is:

```text
src/main/java/Main.java
```
