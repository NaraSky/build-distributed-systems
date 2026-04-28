# Handle Node Failure with Replica Promotion

Website: <https://builddistributedsystem.com/tracks/searcher/tasks/task-16-2-5-node-failure>

Track: 23. The Searcher
Task order: 10
Short title: Node Failure
Difficulty: advanced
Subtrack: Distributed Sharding and Replication

## Problem

When a node fails, the cluster must promote replica shards to primary and reallocate lost replicas to maintain the desired replication factor.

**Failure handling flow**:
1. Cluster master detects node failure (missed heartbeats for 30s)
2. For each primary shard on the failed node: promote a replica to primary
3. For each replica shard on the failed node: mark as "unassigned"
4. Allocate new replicas on healthy nodes to restore the replication factor
5. New replicas sync from their primaries (recovery)

**Recovery**: when the failed node comes back online, its stale shards sync from the current primaries. If the data delta is small, an incremental sync is used; otherwise, a full copy.

```json
Request:  {"type": "node_failure", "msg_id": 1, "failed_node": "n2"}
Response: {"type": "node_failure_ok", "in_reply_to": 1, "primaries_promoted": 2, "replicas_unassigned": 3, "recovery_started": true}
```

## Concepts

- node failure
- replica promotion
- unassigned shards
- recovery
- shard reallocation

## Hints

- When a node fails, its primary shards must be replaced by promoting replicas
- The cluster master detects node failure via missed heartbeats
- For each primary on the failed node: promote a replica to primary
- The lost replicas go into "unassigned" state and are reallocated to healthy nodes
- When the failed node recovers, it syncs from the current primaries

## Test Cases

### 1. Replicas promoted on node failure

node_failure_ok should show primaries_promoted >= 0 and recovery_started: true.

Input:

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1","n2","n3"]}}
{"src":"c1","dest":"n1","body":{"type":"node_failure","msg_id":2,"failed_node":"n2"}}
```

Expected output:

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

### 2. Unassigned replicas are reallocated

cluster_health should show unassigned_shards > 0 initially, then 0 after reallocation.

Input:

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1","n2","n3"]}}
{"src":"c1","dest":"n1","body":{"type":"node_failure","msg_id":2,"failed_node":"n3"}}
{"src":"c1","dest":"n1","body":{"type":"cluster_health","msg_id":3}}
```

Expected output:

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

## Resources

- [Elasticsearch Recovery](https://www.elastic.co/guide/en/elasticsearch/reference/current/modules-gateway.html): Elasticsearch documentation on shard recovery and node failure handling

## Java Starter

The matching local starter file is:

```text
src/main/java/Main.java
```
