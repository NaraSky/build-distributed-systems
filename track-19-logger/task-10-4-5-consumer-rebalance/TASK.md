# Implement Consumer Group Rebalancing

Website: <https://builddistributedsystem.com/tracks/logger/tasks/task-10-4-5-consumer-rebalance>

Track: 19. The Logger
Task order: 20
Short title: Consumer Rebalance
Difficulty: advanced
Subtrack: Distributed Log (Kafka Architecture)

## Problem

Consumer group rebalancing ensures that partitions are evenly distributed among consumers. When the group membership changes (a consumer joins, leaves, or crashes), the partitions must be reassigned.

The rebalancing protocol:
1. **Trigger**: a consumer joins the group, leaves the group, or is removed (heartbeat timeout)
2. **Stop**: all consumers in the group stop reading (consumption is paused)
3. **Elect leader**: the group coordinator (a broker) elects one consumer as the group leader
4. **Assign**: the leader runs the assignment strategy and assigns partitions to consumers
5. **Resume**: all consumers receive their new assignments and resume reading

**Range assignment strategy** (the simplest):
- Sort the partition IDs and consumer IDs
- Divide partitions into contiguous ranges
- Example: 6 partitions, 3 consumers -> c1: [0,1], c2: [2,3], c3: [4,5]
- With uneven division: 7 partitions, 3 consumers -> c1: [0,1,2], c2: [3,4], c3: [5,6]

```json
Request:  {"type": "consumer_rebalance", "msg_id": 1, "group": "analytics", "consumers": ["c1", "c2", "c3"], "partitions": [0, 1, 2, 3, 4, 5], "strategy": "range"}
Response: {"type": "consumer_rebalance_ok", "in_reply_to": 1, "assignments": {"c1": [0, 1], "c2": [2, 3], "c3": [4, 5]}}

Request:  {"type": "consumer_rebalance", "msg_id": 2, "group": "analytics", "consumers": ["c1", "c2"], "partitions": [0, 1, 2, 3, 4, 5], "strategy": "range"}
Response: {"type": "consumer_rebalance_ok", "in_reply_to": 2, "assignments": {"c1": [0, 1, 2], "c2": [3, 4, 5]}}
```

## Concepts

- consumer group
- rebalancing
- partition assignment
- range strategy
- group coordinator

## Hints

- When a consumer joins or leaves a group, all partition assignments must be recalculated
- Range strategy: sort consumers and partitions, divide partitions into contiguous ranges per consumer
- During rebalancing, all consumers in the group pause consumption briefly (stop-the-world)
- The group coordinator (a broker) manages the rebalancing protocol
- Uneven distribution: if 6 partitions / 4 consumers, some consumers get 2 and some get 1

## Test Cases

### 1. Even distribution: 6 partitions, 3 consumers

Input:

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"consumer_rebalance","msg_id":2,"group":"g1","consumers":["c1","c2","c3"],"partitions":[0,1,2,3,4,5],"strategy":"range"}}
```

Expected output:

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
{"src": "n1", "dest": "c1", "body": {"type": "consumer_rebalance_ok", "in_reply_to": 2, "assignments": {"c1": [0, 1], "c2": [2, 3], "c3": [4, 5]}, "msg_id": 1}}
```

### 2. Redistribution after consumer leaves: 6 partitions, 2 consumers

Input:

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"consumer_rebalance","msg_id":2,"group":"g1","consumers":["c1","c2"],"partitions":[0,1,2,3,4,5],"strategy":"range"}}
```

Expected output:

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
{"src": "n1", "dest": "c1", "body": {"type": "consumer_rebalance_ok", "in_reply_to": 2, "assignments": {"c1": [0, 1, 2], "c2": [3, 4, 5]}, "msg_id": 1}}
```

## Resources

- [Kafka Consumer Group Protocol](https://kafka.apache.org/documentation/#impl_consumerrebalance): Kafka documentation on consumer group rebalancing protocol and partition assignment strategies

## Java Starter

The matching local starter file is:

```text
src/main/java/Main.java
```
