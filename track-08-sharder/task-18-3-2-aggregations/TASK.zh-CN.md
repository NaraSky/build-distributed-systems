# 实现跨分片聚合

英文标题：Implement Cross-Shard Aggregations
网页：<https://builddistributedsystem.com/tracks/sharder/tasks/task-18-3-2-aggregations>

课程：8. 分片器：水平扩展与数据迁移
任务序号：12
短标题：跨分片聚合
难度：进阶
子主题：跨分片查询

## 中文导读

本题要求你实现跨分片的聚合查询。在分布式系统中，聚合操作不能简单地在各分片上独立执行后直接合并，不同的聚合函数有不同的合并策略。比如求平均值时，不能直接对各分片的平均值取平均，而是要用"总和除以总数"来计算。理解这些差异是正确实现分布式查询的关键。

## 题目说明

分布式聚合需要先在每个分片上计算局部聚合结果，再由协调者合并这些部分结果。不同的聚合函数有不同的合并策略。

**COUNT 聚合**：
- 分片：`SELECT COUNT(*) FROM users WHERE age > 25` 返回 `{"count": 150}`
- 协调者：将各分片的计数求和，total_count = 150 + 200 + 175 = 525

**SUM 聚合**：
- 分片：`SELECT SUM(price) FROM orders` 返回 `{"sum": 15000.50}`
- 协调者：将各分片的求和值相加，total_sum = 15000.50 + 20000.75 + 17500.25

**AVG 聚合**：
- 分片：`SELECT AVG(rating), COUNT(*) FROM reviews` 返回 `{"sum": 450.5, "count": 100}`
- 协调者：计算 `global_avg = total_sum / total_count`
- 注意：不能简单地对各分片的平均值再取平均！必须按数量加权。

**查询示例**：
```json
Request:  {"type": "agg_query", "msg_id": 1, "agg_type": "SUM", "field": "price", "table": "orders"}
Response: {"type": "agg_query_ok", "in_reply_to": 1, "result": 52501.50, "shards_responded": 3}
```

**AVG 查询示例**：
```json
Request:  {"type": "agg_query", "msg_id": 2, "agg_type": "AVG", "field": "rating", "table": "reviews"}
Response: {"type": "agg_query_ok", "in_reply_to": 2, "result": 4.35, "shards_responded": 3}
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

- COUNT：每个分片返回计数，协调者将所有计数求和
- SUM：每个分片返回求和值，协调者将所有求和值相加
- AVG：每个分片返回（总和，计数），协调者计算 total_sum / total_count
- MIN/MAX：每个分片返回本地的最小值/最大值，协调者取全局的最小值/最大值
- 注意 COUNT(DISTINCT)：不能简单地将各分片的去重计数相加

## 测试用例

### 1. 跨分片求和聚合

`agg_query_ok` 应返回所有分片的价格之和（例如 15000.50 + 20000.75 + 17500.25 = 52501.50）。

输入：

```json
{"src":"c0","dest":"coord","body":{"type":"init","msg_id":1,"shards":["s1","s2","s3"]}}
{"src":"c1","dest":"coord","body":{"type":"agg_query","msg_id":2,"agg_type":"SUM","field":"price","table":"orders"}}
```

期望输出：

```text
{"src": "coord", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

### 2. 跨分片计数聚合

`agg_query_ok` 应返回两个分片的总计数（例如 150 + 200 = 350）。

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

- [Distributed Aggregations](https://www.vldb.org/pvldb/vol8/p1818-truong.pdf)：关于分布式聚合策略的论文

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
