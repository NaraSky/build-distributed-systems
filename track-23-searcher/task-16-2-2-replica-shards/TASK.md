# Add Replica Shards for Fault Tolerance

Website: <https://builddistributedsystem.com/tracks/searcher/tasks/task-16-2-2-replica-shards>

Track: 23. The Searcher
Task order: 7
Short title: Replica Shards
Difficulty: advanced
Subtrack: Distributed Sharding and Replication

## Problem

Replica shards provide fault tolerance and read scaling. Each primary shard has one or more replicas on different nodes.

**Write flow**:
1. Write request arrives at the primary shard
2. Primary indexes the document
3. Primary forwards the write to all replica shards in parallel
4. Each replica indexes the document and sends ACK
5. Primary returns success to the client after all replicas ACK

**Read flow**: reads can be served from any copy (primary or replica), distributing read load.

**Failure handling**: if a node with a primary dies, a replica is promoted to primary. If a node with a replica dies, a new replica is allocated on another node.

```json
Request:  {"type": "create_index", "msg_id": 1, "index": "articles", "num_shards": 3, "num_replicas": 1}
Response: {"type": "create_index_ok", "in_reply_to": 1, "primary_shards": 3, "replica_shards": 3, "total_shards": 6}
```

## Concepts

- replica shard
- replication
- write propagation
- read scaling
- fault tolerance

## Hints

- Each primary shard has R replica shards on different nodes
- Writes go to the primary first, then propagate to all replicas
- Reads can be served from any replica (scaling read throughput)
- Primary wait for replicas to acknowledge before returning success
- If a replica falls behind, it is marked as "unassigned" until it catches up

## Test Cases

### 1. Create index with replicas

create_index_ok should show 3 primary + 3 replica = 6 total shards.

Input:

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1","n2","n3"]}}
{"src":"c1","dest":"n1","body":{"type":"create_index","msg_id":2,"index":"articles","num_shards":3,"num_replicas":1}}
```

Expected output:

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

### 2. Write propagates to replicas

doc_index_ok should confirm replica acknowledgement.

Input:

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1","n2"]}}
{"src":"c1","dest":"n1","body":{"type":"doc_index","msg_id":2,"index":"articles","doc":{"title":"test"},"wait_for_replicas":true}}
```

Expected output:

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

## Resources

- [Elasticsearch Replication](https://www.elastic.co/guide/en/elasticsearch/reference/current/docs-replication.html): Elasticsearch documentation on primary-replica replication

## Java Starter

The matching local starter file is:

```text
src/main/java/Main.java
```
