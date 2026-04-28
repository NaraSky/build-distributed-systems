# 实现 Distributed ORDER BY，包含LIMIT

英文标题：Implement Distributed ORDER BY，包含LIMIT
网页：<https://builddistributedsystem.com/tracks/sharder/tasks/task-18-3-5-order-limit>

课程：8. 分片器：水平扩展与数据迁移
任务序号：15
短标题：Distributed ORDER BY LIMIT
难度：intermediate
子主题：Cross-分片 Queries

## 中文导读

本题要求你完成 `实现 Distributed ORDER BY，包含LIMIT`。

重点关注：`distributed sorting`、`top-N query`、`merge sort`、`tie handling`、`pagination`。

建议先按提示逐步实现：Each 分片 returns its top K results (where K = LIMIT * safety_factor)。

协议字段、消息类型、输入输出格式请以本文件中的代码块和测试用例为准。

## 题目说明

Implementing `ORDER BY score DESC LIMIT 10` in a distributed system requires each 分片 to return its local top results, then the coordinator merges them to find the global top results.

**Naive approach (wrong)**:
1. Each 分片 returns its top 10 results
2. Coordinator picks the top 10 from the combined 30
3. Problem: if one 分片 has the top 100 highest scores, we miss results 11-100!

**Correct approach**:
1. Each 分片 returns its top (LIMIT * safety_factor) results, e.g., top 30
2. Coordinator merges all partial results使用a priority 队列
3. Coordinator returns the global top 10

**Example query**:
```JSON
请求:  {"type": "top_n_query", "msg_id": 1, "table": "scores", "order_by": "score", "order": "DESC", "limit": 10}
响应: {"type": "top_n_query_ok", "in_reply_to": 1, "results": [...], "total_candidates": 90}
```

Where `total_candidates` is the sum of candidates from all shards (e.g., 30 per 分片 × 3 shards = 90).

**Handling ties**:
When two users have the same score, we need consistent ordering. Use a composite sort key:
```typescript
function compare(a, b) {
    if (a.score !== b.score) return b.score - a.score; // DESC by score
    return a.user_id.localeCompare(b.user_id); // ASC by user_id用于ties
}
```

**Pagination**:
For page 2 (`LIMIT 10 OFFSET 10`), each 分片 returns top 20 results,和the coordinator merges和returns results 11-20.

**Implementation**:
1. Send `top_n_query` to all shards，包含`limit * safety_factor`
2. Each 分片 sorts its local data和returns top N results
3. Coordinator merges使用a min-heap of size `limit`
4. Coordinator returns the global top `limit` results

## 涉及概念

- `distributed sorting`
- `top-N query`
- `merge sort`
- `tie handling`
- `pagination`
- `consistent ordering`

## 实现提示

- Each 分片 returns its top K results (where K = LIMIT * safety_factor)
- Coordinator merges all partial results使用a priority 队列 (min-heap)
- Coordinator returns the global top K results
- Use a safety_factor (e.g., 2-3x) to account用于uneven distribution
-处理ties consistently: use (score, user_id) as the sort key

## 测试用例

### 1. Top 10 scores across 3 shards

top_n_query_ok should return 10 highest scores from all shards, sorted DESC by score.

输入：

```json
{"src":"c0","dest":"coord","body":{"type":"init","msg_id":1,"shards":["s1","s2","s3"]}}
{"src":"c1","dest":"coord","body":{"type":"top_n_query","msg_id":2,"table":"scores","order_by":"score","order":"DESC","limit":10}}
```

期望输出：

```text
{"src": "coord", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

### 2. Top 10，包含ties (consistent ordering)

top_n_query_ok should handle ties consistently使用(score, user_id) as sort key.

输入：

```json
{"src":"c0","dest":"coord","body":{"type":"init","msg_id":1,"shards":["s1","s2"]}}
{"src":"c1","dest":"coord","body":{"type":"top_n_query","msg_id":2,"table":"scores","order_by":"score","order":"DESC","limit":10}}
```

期望输出：

```text
{"src": "coord", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

## 参考资料

- [Distributed Top-N Queries](https://arxiv.org/abs/1401.1810)：Paper on efficient top-N query processing in 分布式系统

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
