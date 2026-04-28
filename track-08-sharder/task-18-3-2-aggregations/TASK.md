# Implement Cross-Shard Aggregations

Website: <https://builddistributedsystem.com/tracks/sharder/tasks/task-18-3-2-aggregations>

Track: 8. The Sharder
Task order: 12
Short title: Cross-Shard Aggregations
Difficulty: intermediate
Subtrack: Cross-Shard Queries

## Problem

Distributed aggregations require computing partial aggregates on each shard, then merging partial results at the coordinator. Different aggregation functions have different merge strategies.

**COUNT aggregation**:
- Shard: `SELECT COUNT(*) FROM users WHERE age > 25` → `{"count": 150}`
- Coordinator: sum all shard counts → total_count = 150 + 200 + 175 = 525

**SUM aggregation**:
- Shard: `SELECT SUM(price) FROM orders` → `{"sum": 15000.50}`
- Coordinator: sum all shard sums → total_sum = 15000.50 + 20000.75 + 17500.25

**AVG aggregation**:
- Shard: `SELECT AVG(rating), COUNT(*) FROM reviews` → `{"sum": 450.5, "count": 100}`
- Coordinator: compute `global_avg = total_sum / total_count`
- Cannot simply average the averages! Must weight by count.

**Example query**:
```json
Request:  {"type": "agg_query", "msg_id": 1, "agg_type": "SUM", "field": "price", "table": "orders"}
Response: {"type": "agg_query_ok", "in_reply_to": 1, "result": 52501.50, "shards_responded": 3}
```

**AVG query example**:
```json
Request:  {"type": "agg_query", "msg_id": 2, "agg_type": "AVG", "field": "rating", "table": "reviews"}
Response: {"type": "agg_query_ok", "in_reply_to": 2, "result": 4.35, "shards_responded": 3}
```

## Concepts

- distributed aggregations
- partial aggregates
- COUNT
- SUM
- AVG
- merge functions
- algebraic properties

## Hints

- COUNT: each shard returns a count, coordinator sums all counts
- SUM: each shard returns a sum, coordinator sums all sums
- AVG: each shard returns (sum, count), coordinator computes total_sum / total_count
- MIN/MAX: each shard returns its min/max, coordinator takes the global min/max
- Be careful with COUNT(DISTINCT): cannot simply sum counts

## Test Cases

### 1. SUM aggregation across shards

agg_query_ok should return sum of prices from all shards (e.g., 15000.50 + 20000.75 + 17500.25 = 52501.50).

Input:

```json
{"src":"c0","dest":"coord","body":{"type":"init","msg_id":1,"shards":["s1","s2","s3"]}}
{"src":"c1","dest":"coord","body":{"type":"agg_query","msg_id":2,"agg_type":"SUM","field":"price","table":"orders"}}
```

Expected output:

```text
{"src": "coord", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

### 2. COUNT aggregation across shards

agg_query_ok should return total count from both shards (e.g., 150 + 200 = 350).

Input:

```json
{"src":"c0","dest":"coord","body":{"type":"init","msg_id":1,"shards":["s1","s2"]}}
{"src":"c1","dest":"coord","body":{"type":"agg_query","msg_id":2,"agg_type":"COUNT","field":"*","table":"users"}}
```

Expected output:

```text
{"src": "coord", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

## Resources

- [Distributed Aggregations](https://www.vldb.org/pvldb/vol8/p1818-truong.pdf): Paper on distributed aggregation strategies

## Java Starter

The matching local starter file is:

```text
src/main/java/Main.java
```
