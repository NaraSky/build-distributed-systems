# 实现 Scatter-Gather Query Execution

英文标题：Implement Scatter-Gather Query Execution
网页：<https://builddistributedsystem.com/tracks/sharder/tasks/task-18-3-1-scatter-gather>

课程：8. 分片器：水平扩展与数据迁移
任务序号：11
短标题：Scatter-Gather
难度：intermediate
子主题：Cross-分片 Queries

## 中文导读

本题要求你完成 `实现 Scatter-Gather Query Execution`。

重点关注：`scatter-gather`、`query coordinator`、`partial results`、`timeout handling`、`fault tolerance`。

建议先按提示逐步实现：The coordinator sends the query to all shards in parallel。

协议字段、消息类型、输入输出格式请以本文件中的代码块和测试用例为准。

## 题目说明

Scatter-gather is a fundamental distributed query execution pattern. The coordinator "scatters" a query to all shards, each 分片 processes its local data,和the coordinator "gathers" partial results into a final 响应.

**Query execution flow**:
1. 客户端 sends a query to the coordinator
2. Coordinator forwards the query to all known shards
3. Each 分片 executes the query on its local data
4. Each 分片 returns partial results to the coordinator
5. Coordinator merges all partial results into a complete 响应
6. Coordinator returns the merged 响应 to the 客户端

**Handling partial failures**:
- Set a 超时用于each 分片 响应 (e.g., 1000ms)
- If a 分片 times out, exclude its results but continue，包含other shards
- Track which shards responded successfully
- Return a "shards_responded" count so the 客户端 knows if results are complete

**Example query**:
```JSON
请求:  {"type": "scatter_query", "msg_id": 1, "query": "SELECT * FROM users WHERE age > 25"}
响应: {"type": "scatter_query_ok", "in_reply_to": 1, "results": [...], "shards_total": 3, "shards_responded": 3}
```

If 分片 2 is down:
```JSON
响应: {"type": "scatter_query_ok", "in_reply_to": 1, "results": [...], "shards_total": 3, "shards_responded": 2}
```

## 涉及概念

- `scatter-gather`
- `query coordinator`
- `partial results`
- `timeout handling`
- `fault tolerance`

## 实现提示

- The coordinator sends the query to all shards in parallel
- Each 分片 executes the query locally和returns partial results
- The coordinator merges partial results into a final 响应
- Use timeouts: if a 分片 doesn't respond within T ms, proceed without it
- Track which shards responded: include a "shards_responded" field in the 响应

## 测试用例

### 1. All shards respond successfully

scatter_query_ok should return results from all 3 shards和shards_responded=3.

输入：

```json
{"src":"c0","dest":"coord","body":{"type":"init","msg_id":1,"shards":["s1","s2","s3"]}}
{"src":"c1","dest":"coord","body":{"type":"scatter_query","msg_id":2,"query":"SELECT * FROM users"}}
```

期望输出：

```text
{"src": "coord", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

### 2. One 分片 times out

scatter_query_ok should return results from 2 shards (s2 times out)和shards_responded=2.

输入：

```json
{"src":"c0","dest":"coord","body":{"type":"init","msg_id":1,"shards":["s1","s2","s3"]}}
{"src":"c1","dest":"coord","body":{"type":"scatter_query","msg_id":2,"query":"SELECT * FROM users","timeout_ms":500}}
```

期望输出：

```text
{"src": "coord", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

## 参考资料

- [Scatter-Gather Query](https://www.citusdata.com/blog/2016/08/03/scatter-gather-queries-citus/)：Deep dive on scatter-gather query execution in distributed databases

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
