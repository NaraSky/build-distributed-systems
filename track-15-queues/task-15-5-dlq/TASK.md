# Add Dead Letter Queues

Website: <https://builddistributedsystem.com/tracks/queues/tasks/task-15-5-dlq>

Track: 15. Queues
Task order: 5
Short title: Dead Letter Queue
Difficulty: intermediate
Subtrack: At-Most-Once and At-Least-Once Delivery

## Problem

Implement dead letter queues for failed messages:

1. Track retry count for each message
2. On processing failure, increment retry count
3. After N failures, move to dead letter queue
4. Preserve: original message, error details, timestamps
5. Provide interface to inspect and replay DLQ messages

DLQs prevent poison messages from blocking the queue.

## Concept Notes

### Dead Letter Queues

Some messages may never succeed: invalid format, missing data, bugs. Instead of retrying forever or losing them, move failures to a DLQ for investigation. Operators can fix issues and replay messages.

### Poison Messages

A poison message is one that consistently fails processing. Without DLQ, it blocks the queue (if ordered) or wastes resources (if retried forever). DLQ isolates the poison so healthy messages flow.

## Concepts

- DLQ
- poison message
- error handling

## Hints

- Track retry count per message
- Move to DLQ after max retries
- Preserve error information

## Test Cases

### 1. Move to DLQ after retries

Message m1 fails processing 3 times (max_retries=3). After 3rd failure, message should be moved to dead letter queue with error details and retry count. Verify poison message does not block main queue.

Input:

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
```

Expected output:

```text
{"src":"n1","dest":"c0","body":{"type":"init_ok","in_reply_to":1,"msg_id":0}}
```

### 2. Replay from DLQ

Message in DLQ can be inspected and replayed. Operator fixes issue, triggers replay. Message moves from DLQ back to main queue for reprocessing. Verify DLQ provides inspection and replay capabilities.

Input:

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
```

Expected output:

```text
{"src":"n1","dest":"c0","body":{"type":"init_ok","in_reply_to":1,"msg_id":0}}
```

## Resources

- [DLQ Best Practices](https://aws.amazon.com/blogs/compute/designing-durable-serverless-apps-with-dlqs-for-amazon-sns-amazon-sqs-aws-lambda/): AWS guide to dead letter queues

## Java Starter

The matching local starter file is:

```text
src/main/java/Main.java
```
