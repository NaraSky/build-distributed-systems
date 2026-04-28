# Implement Distributed ORDER BY with LIMIT

Website: <https://builddistributedsystem.com/tracks/sharder/tasks/task-18-3-5-order-limit>

Track: 8. The Sharder
Task order: 15
Short title: Distributed ORDER BY LIMIT
Difficulty: intermediate
Subtrack: Cross-Shard Queries

## Problem

Implementing `ORDER BY score DESC LIMIT 10` in a distributed system requires each shard to return its local top results, then the coordinator merges them to find the global top results.

**Naive approach (wrong)**:
1. Each shard returns its top 10 results
2. Coordinator picks the top 10 from the combined 30
3. Problem: if one shard has the top 100 highest scores, we miss results 11-100!

**Correct approach**:
1. Each shard returns its top (LIMIT * safety_factor) results, e.g., top 30
2. Coordinator merges all partial results using a priority queue
3. Coordinator returns the global top 10

**Example query**:
```json
Request:  {"type": "top_n_query", "msg_id": 1, "table": "scores", "order_by": "score", "order": "DESC", "limit": 10}
Response: {"type": "top_n_query_ok", "in_reply_to": 1, "results": [...], "total_candidates": 90}
```

Where `total_candidates` is the sum of candidates from all shards (e.g., 30 per shard × 3 shards = 90).

**Handling ties**:
When two users have the same score, we need consistent ordering. Use a composite sort key:
```typescript
function compare(a, b) {
    if (a.score !== b.score) return b.score - a.score; // DESC by score
    return a.user_id.localeCompare(b.user_id); // ASC by user_id for ties
}
```

**Pagination**:
For page 2 (`LIMIT 10 OFFSET 10`), each shard returns top 20 results, and the coordinator merges and returns results 11-20.

**Implementation**:
1. Send `top_n_query` to all shards with `limit * safety_factor`
2. Each shard sorts its local data and returns top N results
3. Coordinator merges using a min-heap of size `limit`
4. Coordinator returns the global top `limit` results

## Concepts

- distributed sorting
- top-N query
- merge sort
- tie handling
- pagination
- consistent ordering

## Hints

- Each shard returns its top K results (where K = LIMIT * safety_factor)
- Coordinator merges all partial results using a priority queue (min-heap)
- Coordinator returns the global top K results
- Use a safety_factor (e.g., 2-3x) to account for uneven distribution
- Handle ties consistently: use (score, user_id) as the sort key

## Test Cases

### 1. Top 10 scores across 3 shards

top_n_query_ok should return 10 highest scores from all shards, sorted DESC by score.

Input:

```json
{"src":"c0","dest":"coord","body":{"type":"init","msg_id":1,"shards":["s1","s2","s3"]}}
{"src":"c1","dest":"coord","body":{"type":"top_n_query","msg_id":2,"table":"scores","order_by":"score","order":"DESC","limit":10}}
```

Expected output:

```text
{"src": "coord", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

### 2. Top 10 with ties (consistent ordering)

top_n_query_ok should handle ties consistently using (score, user_id) as sort key.

Input:

```json
{"src":"c0","dest":"coord","body":{"type":"init","msg_id":1,"shards":["s1","s2"]}}
{"src":"c1","dest":"coord","body":{"type":"top_n_query","msg_id":2,"table":"scores","order_by":"score","order":"DESC","limit":10}}
```

Expected output:

```text
{"src": "coord", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

## Resources

- [Distributed Top-N Queries](https://arxiv.org/abs/1401.1810): Paper on efficient top-N query processing in distributed systems

## Java Starter

The matching local starter file is:

```text
src/main/java/Main.java
```
