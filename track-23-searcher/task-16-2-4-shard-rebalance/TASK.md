# Implement Shard Rebalancing on Node Join

Website: <https://builddistributedsystem.com/tracks/searcher/tasks/task-16-2-4-shard-rebalance>

Track: 23. The Searcher
Task order: 9
Short title: Shard Rebalance
Difficulty: advanced
Subtrack: Distributed Sharding and Replication

## Problem

When a node joins the cluster, shards must be redistributed to balance load across all nodes. This is a background operation that must not disrupt ongoing searches.

**Rebalancing algorithm**:
1. Calculate target per node: `ceil(total_shards / num_nodes)`
2. Identify over-loaded nodes (more than target shards) and under-loaded nodes
3. For each excess shard on over-loaded nodes: migrate to an under-loaded node

**Migration process**:
1. Start copying shard data from source to target (background)
2. Source continues serving reads and writes during copy
3. When copy is complete, redirect new writes to target
4. Apply any writes that occurred during the copy (catch-up phase)
5. Mark migration as complete; remove shard from source

```json
Request:  {"type": "rebalance", "msg_id": 1, "index": "articles"}
Response: {"type": "rebalance_ok", "in_reply_to": 1, "shards_moved": 2, "source_nodes": ["n1", "n2"], "target_nodes": ["n3"], "duration_ms": 5000}
```

## Concepts

- shard rebalancing
- shard migration
- background operation
- even distribution
- node join

## Hints

- When a new node joins, move some shards to it to balance load
- Calculate the target: each node should have roughly total_shards / num_nodes shards
- Migration is a background operation: copy the shard data, then update routing
- During migration, the source shard continues serving requests
- After migration, redirect new requests to the target node

## Test Cases

### 1. Rebalance distributes shards evenly

rebalance_ok should show shards moved to achieve even distribution.

Input:

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1","n2","n3"]}}
{"src":"c1","dest":"n1","body":{"type":"rebalance","msg_id":2,"index":"articles"}}
```

Expected output:

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

### 2. Already balanced returns no moves

If already balanced, shards_moved should be 0.

Input:

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"rebalance","msg_id":2,"index":"balanced_idx"}}
```

Expected output:

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

## Resources

- [Elasticsearch Shard Allocation](https://www.elastic.co/guide/en/elasticsearch/reference/current/modules-cluster.html): Elasticsearch documentation on shard allocation and rebalancing

## Java Starter

The matching local starter file is:

```text
src/main/java/Main.java
```
