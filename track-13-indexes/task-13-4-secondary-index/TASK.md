# Add Secondary Indexes

Website: <https://builddistributedsystem.com/tracks/indexes/tasks/task-13-4-secondary-index>

Track: 13. Indexes
Task order: 4
Short title: Secondary Index
Difficulty: intermediate

## Problem

Implement secondary indexes for non-key attributes:

1. Primary index: primary_key -> data
2. Secondary index: attribute_value -> list of primary_keys
3. Query by attribute: secondary lookup, then primary lookups
4. Keep secondary index updated on all writes/deletes

Secondary indexes enable efficient queries on any attribute, not just the primary key.

## Concept Notes

### Secondary Indexes

Primary indexes organize data by primary key. But what if you need to find users by email or orders by status? Secondary indexes provide alternative access paths for these non-key queries.

### Implementation Approaches

1. Separate index file mapping attribute -> primary keys. 2. Covering index includes full record to avoid primary lookup. 3. Inverted index for text search.

## Concepts

- secondary index
- non-key lookup
- inverted index

## Hints

- Secondary index maps attribute to primary keys
- Update secondary index on data changes
- Handle one-to-many relationships

## Test Cases

### 1. Secondary index lookup

Input:

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"db_insert","msg_id":2,"id":1,"name":"Alice","status":"active"}}
{"src":"c2","dest":"n1","body":{"type":"db_insert","msg_id":3,"id":2,"name":"Bob","status":"active"}}
{"src":"c3","dest":"n1","body":{"type":"db_query","msg_id":4,"field":"status","value":"active"}}
```

Expected output:

```text
{"src":"n1","dest":"c0","body":{"type":"init_ok","in_reply_to":1,"msg_id":0}}
{"src":"n1","dest":"c1","body":{"type":"db_insert_ok","in_reply_to":2,"msg_id":1}}
{"src":"n1","dest":"c2","body":{"type":"db_insert_ok","in_reply_to":3,"msg_id":2}}
{"src":"n1","dest":"c3","body":{"type":"db_query_ok","in_reply_to":4,"msg_id":3,"results":[1,2]}}
```

## Java Starter

The matching local starter file is:

```text
src/main/java/Main.java
```
