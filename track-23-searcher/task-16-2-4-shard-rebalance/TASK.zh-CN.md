# 实现 分片 Rebalancing on节点Join

英文标题：Implement Shard Rebalancing on节点Join
网页：<https://builddistributedsystem.com/tracks/searcher/tasks/task-16-2-4-shard-rebalance>

课程：23. 搜索器：分布式搜索
任务序号：9
短标题：分片 Rebalance
难度：advanced
子主题：Distributed Sharding和复制

## 中文导读

本题要求你完成 `实现 分片 Rebalancing on节点Join`。

重点关注：`shard rebalancing`、`shard migration`、`background operation`、`even distribution`、`node join`。

建议先按提示逐步实现：When a new 节点 joins, move some shards to it to balance load。

协议字段、消息类型、输入输出格式请以本文件中的代码块和测试用例为准。

## 题目说明

When a 节点 joins the 集群, shards must be redistributed to balance load across all 节点. This is a background operation that must not disrupt ongoing searches.

**Rebalancing algorithm**:
1. Calculate target per 节点: `ceil(total_shards / num_nodes)`
2. Identify over-loaded 节点 (more than target shards)和under-loaded 节点
3. For each excess 分片 on over-loaded 节点: migrate to an under-loaded 节点

**Migration process**:
1. Start copying 分片 data from source to target (background)
2. Source continues serving reads和writes during copy
3. When copy is complete, redirect new writes to target
4. Apply any writes that occurred during the copy (catch-up phase)
5. Mark migration as complete; remove 分片 from source

```JSON
请求:  {"type": "rebalance", "msg_id": 1, "索引": "articles"}
响应: {"type": "rebalance_ok", "in_reply_to": 1, "shards_moved": 2, "source_nodes": ["n1", "n2"], "target_nodes": ["n3"], "duration_ms": 5000}
```

## 涉及概念

- `shard rebalancing`
- `shard migration`
- `background operation`
- `even distribution`
- `node join`

## 实现提示

- When a new 节点 joins, move some shards to it to balance load
- Calculate the target: each 节点 should have roughly total_shards / num_nodes shards
- Migration is a background operation: copy the 分片 data, then update routing
- During migration, the source 分片 continues serving requests
- After migration, redirect new requests to the target 节点

## 测试用例

### 1. Rebalance distributes shards evenly

rebalance_ok should show shards moved to achieve even distribution.

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1","n2","n3"]}}
{"src":"c1","dest":"n1","body":{"type":"rebalance","msg_id":2,"index":"articles"}}
```

期望输出：

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

### 2. Already balanced returns no moves

If already balanced, shards_moved should be 0.

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"rebalance","msg_id":2,"index":"balanced_idx"}}
```

期望输出：

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

## 参考资料

- [Elasticsearch Shard Allocation](https://www.elastic.co/guide/en/elasticsearch/reference/current/modules-cluster.html)：Elasticsearch documentation on 分片 allocation和rebalancing

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
