# Add Consumer Groups with Partitions

Website: <https://builddistributedsystem.com/tracks/queues/tasks/task-15-2-consumer-groups>

Track: 15. Queues
Task order: 2
Short title: Consumer Groups
Difficulty: intermediate
Subtrack: At-Most-Once and At-Least-Once Delivery

## Problem

Implement Kafka-style consumer groups:

1. Topic has multiple partitions
2. Messages with same key go to same partition
3. Consumer group: each partition assigned to one consumer
4. Multiple groups each see all messages
5. Rebalance partitions when consumers change

This enables parallel consumption while maintaining per-key ordering.

## Concept Notes

### Consumer Groups

Kafka pioneered consumer groups. Within a group, partitions are divided among consumers for parallelism. Different groups independently consume all messages (pub-sub pattern with scaling).

### Partition Assignment

When consumers join/leave, partitions must be reassigned. Cooperative rebalancing minimizes disruption. Partition count limits max parallelism - plan accordingly.

## Concepts

- consumer groups
- partitioning
- parallel processing

## Hints

- Partition messages by key
- Each partition assigned to one consumer per group
- Rebalance on consumer join/leave

## Test Cases

### 1. Parallel consumption

Topic with 4 partitions. Consumer group with 2 consumers (c1, c2). Each consumer should be assigned 2 partitions. Messages with same key go to same partition. Verify consumers process partitions in parallel and maintain per-key ordering.

Input:

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
```

Expected output:

```text
{"src":"n1","dest":"c0","body":{"type":"init_ok","in_reply_to":1,"msg_id":0}}
```

## Resources

- [Kafka Consumer Groups](https://kafka.apache.org/documentation/#intro_consumers): Kafka consumer documentation

## Java Starter

The matching local starter file is:

```text
src/main/java/Main.java
```
