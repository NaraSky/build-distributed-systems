# Implement Distributed Job Queue

Website: <https://builddistributedsystem.com/tracks/scheduler/tasks/task-22-2-4-distributed-queue>

Track: 24. The Scheduler
Task order: 9
Short title: Distributed Queue
Difficulty: advanced
Subtrack: Distributed Work Allocation

## Problem

A single-broker job queue is both a bottleneck and a single point of failure. A distributed queue partitions jobs across multiple brokers and replicates each partition so no broker failure loses any jobs.

Implement a node that manages a partitioned, replicated job queue:

```json
// Initialize: 3 partitions, replicated to 2 brokers each
{ "type": "init", "msg_id": 1,
  "partitions": 3, "replication_factor": 2 }
-> { "type": "init_ok", "in_reply_to": 1 }

// Push jobs — assigned to partitions by hash(job_id) % 3
{ "type": "push_job", "msg_id": 2,
  "jobs": [{"id":"j1"},{"id":"j2"},{"id":"j3"},
            {"id":"j4"},{"id":"j5"},{"id":"j6"}] }

// Worker pops next job from its assigned partition
{ "type": "pop_job", "msg_id": 3,
  "consumer_id": "w1", "partitions": ["p1","p2","p3"] }
-> { "type": "job_assigned", "in_reply_to": 3,
    "job": {}, "partition": "p1" }

// Add new brokers -> rebalance partitions
{ "type": "rebalance_partitions", "msg_id": 4,
  "new_brokers": ["broker4","broker5"],
  "target_partitions_per_broker": 1 }
-> { "type": "rebalance_complete", "in_reply_to": 4,
    "migrations": [{"partition":"p2","from":"broker1","to":"broker4"}] }
```

## Concepts

- partitioned queue
- replication
- consumer assignment
- partition rebalancing
- broker failover

## Hints

- Assign jobs to partitions using hash(job_id) % num_partitions
- A consumer owns a partition exclusively; only one consumer pops from a partition at a time
- Rebalancing moves partitions from over-loaded brokers to under-loaded ones
- On primary broker failure, a replica promotes to primary and resumes serving without job loss
- Replication factor=2 means every partition has one primary and one replica

## Test Cases

### 1. Partition job distribution

Jobs should be distributed across 3 partitions by hash(job_id) % 3.

Input:

```json
{"src":"producer","dest":"queue","body":{"type":"init","msg_id":1,"partitions":3,"replication_factor":2}}
{"src":"producer","dest":"queue","body":{"type":"push_job","msg_id":2,"jobs":[{"id":"j1"},{"id":"j2"},{"id":"j3"},{"id":"j4"},{"id":"j5"},{"id":"j6"}]}}
```

Expected output:

```text
{"src": "queue", "dest": "producer", "body": {"type": "init_ok", "in_reply_to": 1}}
```

### 2. Consumer pulls from partitions

Worker should receive one job from the first non-empty partition.

Input:

```json
{"src":"worker","dest":"queue","body":{"type":"pop_job","msg_id":1,"consumer_id":"w1","partitions":["p1","p2","p3"]}}
```

Expected output:

```text
{"src": "queue", "dest": "worker", "body": {"type": "job_assigned", "in_reply_to": 1, "job": {}, "partition": "p1"}}
```

## Resources

- [Apache Kafka Design](https://kafka.apache.org/documentation/#design): How Kafka partitions, replicates, and handles failover

## Java Starter

The matching local starter file is:

```text
src/main/java/Main.java
```
