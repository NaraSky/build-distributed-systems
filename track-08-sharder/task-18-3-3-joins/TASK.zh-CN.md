# 实现跨分片连接查询

英文标题：Implement Cross-Shard JOINs
网页：<https://builddistributedsystem.com/tracks/sharder/tasks/task-18-3-3-joins>

课程：8. 分片器：水平扩展与数据迁移
任务序号：13
短标题：跨分片连接
难度：高级
子主题：跨分片查询

## 中文导读

本题要求你实现跨分片的连接（JOIN）查询。跨分片连接是分布式查询中开销最大的操作之一，因为可能需要在网络上搬运大量数据。好消息是，如果两张表按相同的键分片，连接可以在各分片本地完成；坏消息是，如果分片键不同，就需要数据混洗或广播，开销很大。理解这些策略的选择对系统性能至关重要。

## 题目说明

跨分片连接查询的开销很大，因为可能需要在网络上搬运数据。最优策略取决于表的分片方式。

**同分片连接（最佳情况）**：
- 两张表按相同的连接键进行哈希分片
- 例如：`users` 表和 `orders` 表都按 `user_id` 分片
- 每个分片可以在本地对自己的分区执行连接操作
- 协调者合并各分片的部分结果
- 初始分散之后没有额外的网络开销

**同分片连接示例**：
```json
Request:  {"type": "join_query", "msg_id": 1, "left": "users", "right": "orders", "on": "user_id"}
Response: {"type": "join_query_ok", "in_reply_to": 1, "results": [...], "strategy": "co-located", "shuffle_bytes": 0}
```

**混洗连接（最差情况）**：
- 两张表按不同的键分片
- 例如：`users` 按 `user_id` 分片，`orders` 按 `order_id` 分片
- 必须按连接键重新分区两张表
- 或者将较小的表广播到所有分片
- 网络开销很高

**混洗连接示例**：
```json
Request:  {"type": "join_query", "msg_id": 2, "left": "users", "right": "reviews", "on": "user_id"}
Response: {"type": "join_query_ok", "in_reply_to": 2, "results": [...], "strategy": "hash-shuffle", "shuffle_bytes": 5242880}
```

**实现策略**：
1. 检查两张表的分区元数据
2. 如果是同分片的，在每个分片上执行本地连接
3. 如果不是同分片的，选择开销最小的策略：
   - 如果其中一张表很小（不到 1000 行），使用广播连接
   - 如果两张表都很大，使用哈希混洗
4. 返回所使用的策略和混洗字节数，便于观测

## 涉及概念

- `distributed joins`
- `hash partitioning`
- `co-located joins`
- `shuffle joins`
- `join reordering`
- `network overhead`

## 实现提示

- 如果两张表按相同的键分片（同分片），则在每个分片上本地执行连接
- 如果分片键不同，需要跨分片混洗数据
- 广播连接：将较小的表发送到所有分片，然后本地连接
- 哈希混洗：按连接键重新分区两张表，然后本地连接
- 记录 `shuffle_bytes` 指标来衡量网络开销

## 测试用例

### 1. 同分片连接（相同分区键）

`join_query_ok` 应使用 `strategy="co-located"` 且 `shuffle_bytes=0`。

输入：

```json
{"src":"c0","dest":"coord","body":{"type":"init","msg_id":1,"shards":["s1","s2","s3"]}}
{"src":"c1","dest":"coord","body":{"type":"join_query","msg_id":2,"left":"users","right":"orders","on":"user_id"}}
```

期望输出：

```text
{"src": "coord", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

### 2. 混洗连接（不同分区键）

`join_query_ok` 应使用 `strategy="hash-shuffle"` 且 `shuffle_bytes > 0`。

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

- [Distributed Join Algorithms](https://adb.cs.elte.hu/~b_nagy/databases/distributed_joins.pdf)：分布式连接算法综述

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
