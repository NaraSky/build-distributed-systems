# 实现分散-聚集查询执行

英文标题：Implement Scatter-Gather Query Execution
网页：<https://builddistributedsystem.com/tracks/sharder/tasks/task-18-3-1-scatter-gather>

课程：8. 分片器：水平扩展与数据迁移
任务序号：11
短标题：分散-聚集
难度：进阶
子主题：跨分片查询

## 中文导读

本题要求你实现分散-聚集（Scatter-Gather）查询模式，这是分布式查询最基础的执行方式。协调者将查询"分散"到所有分片，每个分片处理自己的本地数据，然后协调者"聚集"各分片的部分结果，合并成最终响应。掌握这个模式是理解跨分片查询的第一步。

## 题目说明

分散-聚集是一种基础的分布式查询执行模式。协调者将查询"分散"到所有分片，每个分片处理本地数据，协调者再将部分结果"聚集"成最终响应。

**查询执行流程**：
1. 客户端向协调者发送查询请求
2. 协调者将查询转发给所有已知分片
3. 每个分片在本地数据上执行查询
4. 每个分片将部分结果返回给协调者
5. 协调者将所有部分结果合并成完整响应
6. 协调者将合并后的响应返回给客户端

**处理部分失败**：
- 为每个分片的响应设置超时（例如 1000 毫秒）
- 如果某个分片超时，跳过它的结果，继续处理其他分片的响应
- 记录哪些分片成功响应了
- 在响应中包含 `shards_responded` 计数，让客户端知道结果是否完整

**查询示例**：
```json
Request:  {"type": "scatter_query", "msg_id": 1, "query": "SELECT * FROM users WHERE age > 25"}
Response: {"type": "scatter_query_ok", "in_reply_to": 1, "results": [...], "shards_total": 3, "shards_responded": 3}
```

如果分片 2 宕机：
```json
Response: {"type": "scatter_query_ok", "in_reply_to": 1, "results": [...], "shards_total": 3, "shards_responded": 2}
```

## 涉及概念

- `scatter-gather`
- `query coordinator`
- `partial results`
- `timeout handling`
- `fault tolerance`

## 实现提示

- 协调者并行地将查询发送到所有分片
- 每个分片在本地执行查询并返回部分结果
- 协调者将部分结果合并成最终响应
- 使用超时机制：如果某个分片在指定时间内未响应，则跳过它
- 记录哪些分片成功响应：在响应中包含 `shards_responded` 字段

## 测试用例

### 1. 所有分片成功响应

`scatter_query_ok` 应返回来自全部 3 个分片的结果，且 `shards_responded=3`。

输入：

```json
{"src":"c0","dest":"coord","body":{"type":"init","msg_id":1,"shards":["s1","s2","s3"]}}
{"src":"c1","dest":"coord","body":{"type":"scatter_query","msg_id":2,"query":"SELECT * FROM users"}}
```

期望输出：

```text
{"src": "coord", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

### 2. 一个分片超时

`scatter_query_ok` 应返回来自 2 个分片的结果（s2 超时），且 `shards_responded=2`。

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

- [Scatter-Gather Query](https://www.citusdata.com/blog/2016/08/03/scatter-gather-queries-citus/)：深入讲解分布式数据库中分散-聚集查询的执行方式

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
