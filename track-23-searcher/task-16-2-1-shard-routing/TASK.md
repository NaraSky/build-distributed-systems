# Implement Document Sharding with Hash-Based Routing

Website: <https://builddistributedsystem.com/tracks/searcher/tasks/task-16-2-1-shard-routing>

Track: 23. The Searcher
Task order: 6
Short title: Shard Routing
Difficulty: advanced
Subtrack: Distributed Sharding and Replication

## Problem

To handle datasets larger than a single machine, documents are distributed across N primary shards using hash-based routing.

**Shard assignment**: `shard = hash(doc_id) % num_primary_shards`. The number of primary shards is fixed at index creation time and cannot be changed later (changing it would require rehashing all documents).

**Index flow**:
1. Client sends index request to any node (coordinator)
2. Coordinator calculates: `shard = hash(doc._id) % N`
3. Coordinator routes the request to the node hosting that shard
4. The shard indexes the document locally

**Search flow**: coordinator sends the query to ALL shards, each shard searches locally, coordinator merges results.

```json
Request:  {"type": "shard_route", "msg_id": 1, "doc_id": "abc123", "num_shards": 5}
Response: {"type": "shard_route_ok", "in_reply_to": 1, "shard": 3, "node": "n2", "hash": 2048}
```

## Concepts

- sharding
- hash routing
- primary shard
- shard assignment
- horizontal scaling

## Hints

- Assign each document to a shard using hash(doc_id) % num_shards
- The number of primary shards is fixed at index creation time
- Each shard is assigned to a node — different shards can be on different nodes
- Index requests are routed to the correct shard based on the doc_id
- Search requests must be sent to ALL shards (scatter-gather pattern)

## Test Cases

### 1. Same doc_id always routes to same shard

Both shard_route_ok responses should return the same shard number.

Input:

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1","n2"]}}
{"src":"c1","dest":"n1","body":{"type":"shard_route","msg_id":2,"doc_id":"abc","num_shards":5}}
{"src":"c1","dest":"n1","body":{"type":"shard_route","msg_id":3,"doc_id":"abc","num_shards":5}}
```

Expected output:

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

### 2. Different doc_ids distribute across shards

Different doc_ids should distribute across the 3 shards.

Input:

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"shard_route","msg_id":2,"doc_id":"a","num_shards":3}}
{"src":"c1","dest":"n1","body":{"type":"shard_route","msg_id":3,"doc_id":"b","num_shards":3}}
{"src":"c1","dest":"n1","body":{"type":"shard_route","msg_id":4,"doc_id":"c","num_shards":3}}
```

Expected output:

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

## Resources

- [Elasticsearch Sharding](https://www.elastic.co/guide/en/elasticsearch/reference/current/scalability.html): Elasticsearch documentation on sharding and scalability

## Java Starter

The matching local starter file is:

```text
src/main/java/Main.java
```
