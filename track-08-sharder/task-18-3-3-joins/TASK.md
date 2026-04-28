# Implement Cross-Shard JOINs

Website: <https://builddistributedsystem.com/tracks/sharder/tasks/task-18-3-3-joins>

Track: 8. The Sharder
Task order: 13
Short title: Cross-Shard JOINs
Difficulty: advanced
Subtrack: Cross-Shard Queries

## Problem

Cross-shard JOINs are expensive because they may require moving data across the network. The optimal strategy depends on how tables are partitioned.

**Co-located joins (best case)**:
- Both tables are hash-partitioned by the join key
- Example: `users` and `orders` both partitioned by `user_id`
- Each shard can perform the join locally on its partition
- Coordinator merges partial results
- Zero network overhead after the initial scatter

**Example co-located join**:
```json
Request:  {"type": "join_query", "msg_id": 1, "left": "users", "right": "orders", "on": "user_id"}
Response: {"type": "join_query_ok", "in_reply_to": 1, "results": [...], "strategy": "co-located", "shuffle_bytes": 0}
```

**Shuffle joins (worst case)**:
- Tables are partitioned by different keys
- Example: `users` by `user_id`, `orders` by `order_id`
- Must repartition both tables by the join key
- Or broadcast the smaller table to all shards
- High network overhead

**Example shuffle join**:
```json
Request:  {"type": "join_query", "msg_id": 2, "left": "users", "right": "reviews", "on": "user_id"}
Response: {"type": "join_query_ok", "in_reply_to": 2, "results": [...], "strategy": "hash-shuffle", "shuffle_bytes": 5242880}
```

**Implementation strategies**:
1. Check partitioning metadata for both tables
2. If co-located, execute local joins on each shard
3. If not co-located, choose the cheapest strategy:
   - Broadcast join if one table is small (< 1000 rows)
   - Hash shuffle if both tables are large
4. Return the strategy used and shuffle_bytes for visibility

## Concepts

- distributed joins
- hash partitioning
- co-located joins
- shuffle joins
- join reordering
- network overhead

## Hints

- If both tables are partitioned by the same key (co-located), join locally on each shard
- If tables are partitioned differently, you need to shuffle data across shards
- Broadcast join: send the smaller table to all shards, join locally
- Hash shuffle: repartition both tables by the join key, then join locally
- Track the "shuffle_bytes" metric to measure network overhead

## Test Cases

### 1. Co-located join (same partition key)

join_query_ok should use strategy="co-located" and shuffle_bytes=0.

Input:

```json
{"src":"c0","dest":"coord","body":{"type":"init","msg_id":1,"shards":["s1","s2","s3"]}}
{"src":"c1","dest":"coord","body":{"type":"join_query","msg_id":2,"left":"users","right":"orders","on":"user_id"}}
```

Expected output:

```text
{"src": "coord", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

### 2. Shuffle join (different partition keys)

join_query_ok should use strategy="hash-shuffle" and shuffle_bytes > 0.

Input:

```json
{"src":"c0","dest":"coord","body":{"type":"init","msg_id":1,"shards":["s1","s2"]}}
{"src":"c1","dest":"coord","body":{"type":"join_query","msg_id":2,"left":"users","right":"reviews","on":"user_id"}}
```

Expected output:

```text
{"src": "coord", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

## Resources

- [Distributed Join Algorithms](https://adb.cs.elte.hu/~b_nagy/databases/distributed_joins.pdf): Survey of distributed join algorithms

## Java Starter

The matching local starter file is:

```text
src/main/java/Main.java
```
