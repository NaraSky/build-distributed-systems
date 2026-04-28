# 实现分布式排序与分页

英文标题：Implement Distributed ORDER BY with LIMIT
网页：<https://builddistributedsystem.com/tracks/sharder/tasks/task-18-3-5-order-limit>

课程：8. 分片器：水平扩展与数据迁移
任务序号：15
短标题：分布式排序与分页
难度：进阶
子主题：跨分片查询

## 中文导读

本题要求你在分布式系统中实现 `ORDER BY score DESC LIMIT 10` 这样的查询。难点在于：不能简单地让每个分片返回前 10 条然后合并，因为数据可能分布不均。你需要让每个分片多返回一些候选结果，然后由协调者用优先队列合并出全局的前 N 条。掌握这个技巧对实现分布式排行榜、分页查询等场景非常实用。

## 题目说明

在分布式系统中实现 `ORDER BY score DESC LIMIT 10`，需要每个分片返回本地的前若干条结果，然后由协调者合并得出全局的前若干条。

**朴素方法（有问题）**：
1. 每个分片返回本地前 10 条结果
2. 协调者从合并后的 30 条中选出前 10 条
3. 问题：如果某个分片包含全局最高的 100 个分数，我们会遗漏第 11 到 100 名！

**正确方法**：
1. 每个分片返回本地前（LIMIT * 安全系数）条结果，例如前 30 条
2. 协调者使用优先队列合并所有部分结果
3. 协调者返回全局前 10 条

**查询示例**：
```json
Request:  {"type": "top_n_query", "msg_id": 1, "table": "scores", "order_by": "score", "order": "DESC", "limit": 10}
Response: {"type": "top_n_query_ok", "in_reply_to": 1, "results": [...], "total_candidates": 90}
```

其中 `total_candidates` 是所有分片返回的候选结果总数（例如每个分片 30 条，3 个分片共 90 条）。

**处理并列**：
当两个用户的分数相同时，需要保证排序的一致性。使用复合排序键：
```typescript
function compare(a, b) {
    if (a.score !== b.score) return b.score - a.score; // 按分数降序
    return a.user_id.localeCompare(b.user_id); // 分数相同时按 user_id 升序
}
```

**分页**：
对于第 2 页（`LIMIT 10 OFFSET 10`），每个分片返回前 20 条结果，协调者合并后返回第 11 到 20 条。

**实现步骤**：
1. 向所有分片发送 `top_n_query`，请求 `limit * safety_factor` 条结果
2. 每个分片对本地数据排序，返回前 N 条
3. 协调者使用大小为 `limit` 的最小堆进行合并
4. 协调者返回全局前 `limit` 条结果

## 涉及概念

- `distributed sorting`
- `top-N query`
- `merge sort`
- `tie handling`
- `pagination`
- `consistent ordering`

## 实现提示

- 每个分片返回本地前 K 条结果（K = LIMIT * 安全系数）
- 协调者使用优先队列（最小堆）合并所有部分结果
- 协调者返回全局前 K 条结果
- 使用安全系数（例如 2 到 3 倍）来应对数据分布不均的情况
- 一致性地处理并列：使用 (score, user_id) 作为排序键

## 测试用例

### 1. 跨 3 个分片取前 10 名

`top_n_query_ok` 应返回所有分片中分数最高的 10 条记录，按分数降序排列。

输入：

```json
{"src":"c0","dest":"coord","body":{"type":"init","msg_id":1,"shards":["s1","s2","s3"]}}
{"src":"c1","dest":"coord","body":{"type":"top_n_query","msg_id":2,"table":"scores","order_by":"score","order":"DESC","limit":10}}
```

期望输出：

```text
{"src": "coord", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

### 2. 处理并列分数的一致性排序

`top_n_query_ok` 应使用 (score, user_id) 作为排序键来一致性地处理并列情况。

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

- [Distributed Top-N Queries](https://arxiv.org/abs/1401.1810)：关于分布式系统中高效执行 Top-N 查询的论文

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
