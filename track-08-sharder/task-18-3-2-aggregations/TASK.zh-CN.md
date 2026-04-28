# 实现 Cross-分片 Aggregations

英文标题：Implement Cross-Shard Aggregations
网页：<https://builddistributedsystem.com/tracks/sharder/tasks/task-18-3-2-aggregations>

课程：8. 分片器：水平扩展与数据迁移
任务序号：12
短标题：Cross-分片 Aggregations
难度：intermediate
子主题：Cross-分片 Queries

## 中文导读

本题要求你完成 `实现 Cross-分片 Aggregations`。

重点关注：`distributed aggregations`、`partial aggregates`、`COUNT`、`SUM`、`AVG`。

建议先按提示逐步实现：COUNT: each 分片 returns a count, coordinator sums all counts。

协议字段、消息类型、输入输出格式请以本文件中的代码块和测试用例为准。

## 题目说明

Distributed aggregations require computing partial aggregates on each 分片, then merging partial results at the coordinator. Different aggregation functions have different merge strategies.

**COUNT aggregation**:
- 分片: `SELECT COUNT(*) FROM users WHERE age > 25` → `{"count": 150}`
- Coordinator: sum all 分片 counts → total_count = 150 + 200 + 175 = 525

**SUM aggregation**:
- 分片: `SELECT SUM(price) FROM orders` → `{"sum": 15000.50}`
- Coordinator: sum all 分片 sums → total_sum = 15000.50 + 20000.75 + 17500.25

**AVG aggregation**:
- 分片: `SELECT AVG(rating), COUNT(*) FROM reviews` → `{"sum": 450.5, "count": 100}`
- Coordinator: compute `global_avg = total_sum / total_count`
- Cannot simply average the averages! Must weight by count.

**Example query**:
```JSON
请求:  {"type": "agg_query", "msg_id": 1, "agg_type": "SUM", "field": "price", "table": "orders"}
响应: {"type": "agg_query_ok", "in_reply_to": 1, "result": 52501.50, "shards_responded": 3}
```

**AVG query example**:
```JSON
请求:  {"type": "agg_query", "msg_id": 2, "agg_type": "AVG", "field": "rating", "table": "reviews"}
响应: {"type": "agg_query_ok", "in_reply_to": 2, "result": 4.35, "shards_responded": 3}
```

## 涉及概念

- `distributed aggregations`
- `partial aggregates`
- `COUNT`
- `SUM`
- `AVG`
- `merge functions`
- `algebraic properties`

## 实现提示

- COUNT: each 分片 returns a count, coordinator sums all counts
- SUM: each 分片 returns a sum, coordinator sums all sums
- AVG: each 分片 returns (sum, count), coordinator computes total_sum / total_count
- MIN/MAX: each 分片 returns its min/max, coordinator takes the global min/max
- Be careful，包含COUNT(DISTINCT): cannot simply sum counts

## 测试用例

### 1. SUM aggregation across shards

agg_query_ok should return sum of prices from all shards (e.g., 15000.50 + 20000.75 + 17500.25 = 52501.50).

输入：

```json
{"src":"c0","dest":"coord","body":{"type":"init","msg_id":1,"shards":["s1","s2","s3"]}}
{"src":"c1","dest":"coord","body":{"type":"agg_query","msg_id":2,"agg_type":"SUM","field":"price","table":"orders"}}
```

期望输出：

```text
{"src": "coord", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

### 2. COUNT aggregation across shards

agg_query_ok should return total count from both shards (e.g., 150 + 200 = 350).

输入：

```json
{"src":"c0","dest":"coord","body":{"type":"init","msg_id":1,"shards":["s1","s2"]}}
{"src":"c1","dest":"coord","body":{"type":"agg_query","msg_id":2,"agg_type":"COUNT","field":"*","table":"users"}}
```

期望输出：

```text
{"src": "coord", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

## 参考资料

- [Distributed Aggregations](https://www.vldb.org/pvldb/vol8/p1818-truong.pdf)：Paper on distributed aggregation strategies

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
