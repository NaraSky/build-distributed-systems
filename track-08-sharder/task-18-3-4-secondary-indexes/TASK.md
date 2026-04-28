# Implement Secondary Indexes on Sharded Data

Website: <https://builddistributedsystem.com/tracks/sharder/tasks/task-18-3-4-secondary-indexes>

Track: 8. The Sharder
Task order: 14
Short title: Secondary Indexes
Difficulty: advanced
Subtrack: Cross-Shard Queries

## Problem

When data is sharded by a primary key (e.g., `user_id`), querying by a secondary key (e.g., `email`) requires a secondary index. There are two main strategies.

**Local secondary index**:
- Each shard maintains an index for its local data only
- Query by email must be sent to ALL shards (scatter-gather)
- Simple to implement but expensive for queries

Example:
```json
Request:  {"type": "secondary_index_query", "msg_id": 1, "index": "email", "value": "alice@example.com"}
Response: {"type": "secondary_index_query_ok", "in_reply_to": 1, "results": [{"user_id": "u42", "email": "alice@example.com"}], "shards_scanned": 3}
```

**Global secondary index**:
- A separate index shard that maps email → primary_key (user_id)
- Query by email first looks up the index shard, then fetches from the data shard
- Faster queries but more complex architecture

Example with global index:
```json
Request:  {"type": "secondary_index_query", "msg_id": 2, "index": "email", "value": "bob@example.com", "use_global": true}
Response: {"type": "secondary_index_query_ok", "in_reply_to": 2, "results": [{"user_id": "u99", "email": "bob@example.com"}], "shards_scanned": 1}
```

**Write amplification**:
When a user updates their email:
1. Update primary record on shard hash(user_id)
2. Update secondary index (either local or global)
3. Two network round-trips instead of one

**Implementation**:
- Maintain an index map: `Map<index_name, Map<index_value, primary_key>>`
- For local indexes: each shard has its own index map
- For global indexes: a dedicated index shard
- On write: update both the record and all secondary indexes

## Concepts

- secondary indexes
- global indexes
- local indexes
- index sharding
- write amplification
- consistency

## Hints

- Primary index: data is partitioned by user_id
- Secondary index on email: need to lookup by email without knowing user_id
- Local secondary index: each shard maintains an index for its local data only
- Global secondary index: a separate index shard that maps email → user_id
- Write amplification: updating a document requires updating both primary and secondary indexes

## Test Cases

### 1. Local secondary index lookup

secondary_index_query_ok should return user record and shards_scanned=3 (scatter-gather).

Input:

```json
{"src":"c0","dest":"coord","body":{"type":"init","msg_id":1,"shards":["s1","s2","s3"]}}
{"src":"c1","dest":"coord","body":{"type":"secondary_index_query","msg_id":2,"index":"email","value":"alice@example.com"}}
```

Expected output:

```text
{"src": "coord", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

### 2. Global secondary index lookup

secondary_index_query_ok should return user record and shards_scanned=1 (direct lookup).

Input:

```json
{"src":"c0","dest":"coord","body":{"type":"init","msg_id":1,"shards":["s1","s2","s3"]}}
{"src":"c1","dest":"coord","body":{"type":"secondary_index_query","msg_id":2,"index":"email","value":"bob@example.com","use_global":true}}
```

Expected output:

```text
{"src": "coord", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

## Resources

- [Secondary Indexes in Distributed Systems](https://www.mongodb.com/basics/create-index): How secondary indexes work in sharded systems

## Java Starter

The matching local starter file is:

```text
src/main/java/Main.java
```
