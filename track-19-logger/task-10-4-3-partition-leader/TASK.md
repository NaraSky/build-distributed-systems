# Implement Partition Leader Election via Raft

Website: <https://builddistributedsystem.com/tracks/logger/tasks/task-10-4-3-partition-leader>

Track: 19. The Logger
Task order: 18
Short title: Partition Leader
Difficulty: advanced
Subtrack: Distributed Log (Kafka Architecture)

## Problem

In a distributed log like Kafka, each partition must have exactly one leader broker that handles all reads and writes. Followers replicate data from the leader for fault tolerance.

Architecture:
- **Leader**: the broker responsible for a partition. All producers and consumers interact with the leader.
- **Followers**: replicate the partition log from the leader. They do not serve reads (in standard Kafka).
- **Leader election**: when the leader crashes, one of the in-sync followers is elected as the new leader.

The metadata flow:
1. Producer calls `metadata_request` to discover which broker is the leader for a partition
2. Producer sends `ProduceRequest` directly to the leader broker
3. Leader writes the message to its local log
4. Leader replicates to followers
5. After replication, leader acknowledges the producer

This ensures total order within a partition — all messages pass through a single leader.

```json
Request:  {"type": "partition_leader", "msg_id": 1, "topic": "orders", "partition": 0}
Response: {"type": "partition_leader_ok", "in_reply_to": 1, "leader": "broker-1", "followers": ["broker-2", "broker-3"], "term": 3}

Request:  {"type": "partition_failover", "msg_id": 2, "topic": "orders", "partition": 0, "failed_leader": "broker-1"}
Response: {"type": "partition_failover_ok", "in_reply_to": 2, "new_leader": "broker-2", "new_term": 4, "failover_ms": 250}
```

## Concepts

- partition leader
- Raft per partition
- leader broker
- follower replication
- metadata

## Hints

- Each Kafka partition has a leader broker that handles all reads and writes
- N-1 follower brokers replicate from the leader for fault tolerance
- Use Raft for leader election within each partition group
- Producers discover the leader via a metadata request and send writes directly to it
- On leader failure, Raft automatically elects a new leader from the followers

## Test Cases

### 1. Query partition leader

partition_leader_ok should include leader node, followers list, and Raft term.

Input:

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1","n2","n3"]}}
{"src":"c1","dest":"n1","body":{"type":"partition_leader","msg_id":2,"topic":"orders","partition":0}}
```

Expected output:

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

### 2. Leader failover elects new leader

partition_failover_ok should show a new_leader different from failed_leader, and new_term > previous term.

Input:

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1","n2","n3"]}}
{"src":"c1","dest":"n1","body":{"type":"partition_failover","msg_id":2,"topic":"orders","partition":0,"failed_leader":"n1"}}
```

Expected output:

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

## Resources

- [Kafka Replication Design](https://kafka.apache.org/documentation/#replication): Kafka documentation on partition replication, leader election, and failover

## Java Starter

The matching local starter file is:

```text
src/main/java/Main.java
```
