# 实现 Cross-分片 JOINs

英文标题：Implement Cross-Shard JOINs
网页：<https://builddistributedsystem.com/tracks/sharder/tasks/task-18-3-3-joins>

课程：8. 分片器：水平扩展与数据迁移
任务序号：13
短标题：Cross-分片 JOINs
难度：advanced
子主题：Cross-分片 Queries

## 中文导读

本题要求你完成 `实现 Cross-分片 JOINs`。

重点关注：`distributed joins`、`hash partitioning`、`co-located joins`、`shuffle joins`、`join reordering`。

建议先按提示逐步实现：If both tables are partitioned by the same key (co-located), join locally on each 分片。

协议字段、消息类型、输入输出格式请以本文件中的代码块和测试用例为准。

## 题目说明

Cross-分片 JOINs are expensive because they may require moving data across the 网络. The optimal strategy depends on how tables are partitioned.

**Co-located joins (best case)**:
- Both tables are hash-partitioned by the join key
- Example: `users`和`orders` both partitioned by `user_id`
- Each 分片 can perform the join locally on its partition
- Coordinator merges partial results
- Zero 网络 overhead after the initial scatter

**Example co-located join**:
```JSON
请求:  {"type": "join_query", "msg_id": 1, "left": "users", "right": "orders", "on": "user_id"}
响应: {"type": "join_query_ok", "in_reply_to": 1, "results": [...], "strategy": "co-located", "shuffle_bytes": 0}
```

**Shuffle joins (worst case)**:
- Tables are partitioned by different keys
- Example: `users` by `user_id`, `orders` by `order_id`
- Must repartition both tables by the join key
- Or 广播 the smaller table to all shards
- High 网络 overhead

**Example shuffle join**:
```JSON
请求:  {"type": "join_query", "msg_id": 2, "left": "users", "right": "reviews", "on": "user_id"}
响应: {"type": "join_query_ok", "in_reply_to": 2, "results": [...], "strategy": "hash-shuffle", "shuffle_bytes": 5242880}
```

**Implementation strategies**:
1. Check partitioning 元数据用于both tables
2. If co-located, execute local joins on each 分片
3. If not co-located, choose the cheapest strategy:
   - 广播 join if one table is small (< 1000 rows)
   - Hash shuffle if both tables are large
4. Return the strategy used和shuffle_bytes用于visibility

## 涉及概念

- `distributed joins`
- `hash partitioning`
- `co-located joins`
- `shuffle joins`
- `join reordering`
- `network overhead`

## 实现提示

- If both tables are partitioned by the same key (co-located), join locally on each 分片
- If tables are partitioned differently, you need to shuffle data across shards
- 广播 join: send the smaller table to all shards, join locally
- Hash shuffle: repartition both tables by the join key, then join locally
- Track the "shuffle_bytes" metric to measure 网络 overhead

## 测试用例

### 1. Co-located join (same partition key)

join_query_ok should use strategy="co-located"和shuffle_bytes=0.

输入：

```json
{"src":"c0","dest":"coord","body":{"type":"init","msg_id":1,"shards":["s1","s2","s3"]}}
{"src":"c1","dest":"coord","body":{"type":"join_query","msg_id":2,"left":"users","right":"orders","on":"user_id"}}
```

期望输出：

```text
{"src": "coord", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

### 2. Shuffle join (different partition keys)

join_query_ok should use strategy="hash-shuffle"和shuffle_bytes > 0.

输入：

```json
{"src":"c0","dest":"coord","body":{"type":"init","msg_id":1,"shards":["s1","s2"]}}
{"src":"c1","dest":"coord","body":{"type":"join_query","msg_id":2,"left":"users","right":"reviews","on":"user_id"}}
```

期望输出：

```text
{"src": "coord", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

## 参考资料

- [Distributed Join Algorithms](https://adb.cs.elte.hu/~b_nagy/databases/distributed_joins.pdf)：Survey of distributed join algorithms

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
