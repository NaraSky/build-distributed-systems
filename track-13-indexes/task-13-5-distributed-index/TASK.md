# Distribute Index Across Nodes

Website: <https://builddistributedsystem.com/tracks/indexes/tasks/task-13-5-distributed-index>

Track: 13. Indexes
Task order: 5
Short title: Distributed Index
Difficulty: advanced

## Problem

Distribute your index across multiple nodes:

1. Partition index entries by key (hash or range)
2. Point lookups go to single partition
3. Range queries scatter to all partitions, gather results
4. Handle partition rebalancing when nodes join/leave

Choose between local secondary index (partitioned with data) and global secondary index (partitioned by index key).

## Concept Notes

### Index Partitioning

When an index outgrows one machine, partition it. Hash partitioning spreads load evenly. Range partitioning preserves locality for range queries but risks hot spots.

### Global vs Local Secondary Index

Local secondary index: partitioned with data, requires scatter-gather for queries. Global secondary index: partitioned by index key, single lookup but writes update multiple partitions.

## Concepts

- partitioned index
- global index
- scatter-gather

## Hints

- Partition index by key hash or range
- Route point queries to single partition
- Range queries need scatter-gather

## Test Cases

### 1. Partitioned insert and lookup

Multi-node test: Index partitioned across 3 nodes (n1, n2, n3) using hash(key) % 3. Insert key "foo" (routes to partition 1 on n2). Get key "foo" should route to same partition n2 and return value. Verify point queries go to single partition.

Input:

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
```

Expected output:

```text
{"src":"n1","dest":"c0","body":{"type":"init_ok","in_reply_to":1,"msg_id":0}}
```

## Java Starter

The matching local starter file is:

```text
src/main/java/Main.java
```
