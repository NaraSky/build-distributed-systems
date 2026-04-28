# Multi-Node Snowflake ID Verification

Website: <https://builddistributedsystem.com/tracks/identifier/tasks/task-2-2-5-multi-node>

Track: 2. The Identifier
Task order: 10
Short title: Multi-Node IDs
Difficulty: advanced
Subtrack: Snowflake IDs (Twitter's Approach)

## Problem

Snowflake IDs derive their uniqueness from the machine_id component. With 10 bits, you can have 1024 unique machines generating IDs without any coordination.

Your task is to verify uniqueness and ordering across multiple nodes:

1. Extract machine_id from Maelstrom node_id (e.g., "n3" -> machine_id 3)
2. Generate IDs and verify they are unique within a node
3. Implement a `verify_ids` handler that checks a list of IDs for uniqueness and ordering

```json
Request:  {"type": "verify_ids", "msg_id": 1, "ids": [100, 200, 300, 200]}
Response: {"type": "verify_ids_ok", "in_reply_to": 1, "count": 4, "unique": 3, "is_sorted": false, "duplicates": [200]}
```

## Concepts

- multi-node coordination
- uniqueness verification
- monotonicity
- ID distribution

## Hints

- Each node uses its own machine_id extracted from the node_id
- IDs from different nodes are unique because the machine_id bits differ
- Within a single node, IDs must be monotonically increasing
- Across nodes, IDs are only roughly sorted due to clock differences
- Use the decompose function to verify machine_id extraction

## Test Cases

### 1. Verify sorted unique IDs

Input:

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"verify_ids","msg_id":2,"ids":[10,20,30]}}
```

Expected output:

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
{"src": "n1", "dest": "c1", "body": {"type": "verify_ids_ok", "count": 3, "unique": 3, "is_sorted": true, "duplicates": [], "in_reply_to": 2, "msg_id": 1}}
```

### 2. Detect duplicates in ID list

Input:

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"verify_ids","msg_id":2,"ids":[10,20,10,30]}}
```

Expected output:

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
{"src": "n1", "dest": "c1", "body": {"type": "verify_ids_ok", "count": 4, "unique": 3, "is_sorted": false, "duplicates": [10], "in_reply_to": 2, "msg_id": 1}}
```

## Resources

- [Unique ID Generation at Scale](https://blog.twitter.com/engineering/en_us/a/2010/announcing-snowflake): Twitter Snowflake announcement blog post

## Java Starter

The matching local starter file is:

```text
src/main/java/Main.java
```
