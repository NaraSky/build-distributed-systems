# Implement Scatter-Gather Query Execution

Website: <https://builddistributedsystem.com/tracks/sharder/tasks/task-18-3-1-scatter-gather>

Track: 8. The Sharder
Task order: 11
Short title: Scatter-Gather
Difficulty: intermediate
Subtrack: Cross-Shard Queries

## Problem

Scatter-gather is a fundamental distributed query execution pattern. The coordinator "scatters" a query to all shards, each shard processes its local data, and the coordinator "gathers" partial results into a final response.

**Query execution flow**:
1. Client sends a query to the coordinator
2. Coordinator forwards the query to all known shards
3. Each shard executes the query on its local data
4. Each shard returns partial results to the coordinator
5. Coordinator merges all partial results into a complete response
6. Coordinator returns the merged response to the client

**Handling partial failures**:
- Set a timeout for each shard response (e.g., 1000ms)
- If a shard times out, exclude its results but continue with other shards
- Track which shards responded successfully
- Return a "shards_responded" count so the client knows if results are complete

**Example query**:
```json
Request:  {"type": "scatter_query", "msg_id": 1, "query": "SELECT * FROM users WHERE age > 25"}
Response: {"type": "scatter_query_ok", "in_reply_to": 1, "results": [...], "shards_total": 3, "shards_responded": 3}
```

If shard 2 is down:
```json
Response: {"type": "scatter_query_ok", "in_reply_to": 1, "results": [...], "shards_total": 3, "shards_responded": 2}
```

## Concepts

- scatter-gather
- query coordinator
- partial results
- timeout handling
- fault tolerance

## Hints

- The coordinator sends the query to all shards in parallel
- Each shard executes the query locally and returns partial results
- The coordinator merges partial results into a final response
- Use timeouts: if a shard doesn't respond within T ms, proceed without it
- Track which shards responded: include a "shards_responded" field in the response

## Test Cases

### 1. All shards respond successfully

scatter_query_ok should return results from all 3 shards and shards_responded=3.

Input:

```json
{"src":"c0","dest":"coord","body":{"type":"init","msg_id":1,"shards":["s1","s2","s3"]}}
{"src":"c1","dest":"coord","body":{"type":"scatter_query","msg_id":2,"query":"SELECT * FROM users"}}
```

Expected output:

```text
{"src": "coord", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

### 2. One shard times out

scatter_query_ok should return results from 2 shards (s2 times out) and shards_responded=2.

Input:

```json
{"src":"c0","dest":"coord","body":{"type":"init","msg_id":1,"shards":["s1","s2","s3"]}}
{"src":"c1","dest":"coord","body":{"type":"scatter_query","msg_id":2,"query":"SELECT * FROM users","timeout_ms":500}}
```

Expected output:

```text
{"src": "coord", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

## Resources

- [Scatter-Gather Query](https://www.citusdata.com/blog/2016/08/03/scatter-gather-queries-citus/): Deep dive on scatter-gather query execution in distributed databases

## Java Starter

The matching local starter file is:

```text
src/main/java/Main.java
```
