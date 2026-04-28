# Distribute 索引 Across Nodes

英文标题：Distribute Index Across Nodes
网页：<https://builddistributedsystem.com/tracks/indexes/tasks/task-13-5-distributed-index>

课程：13. 索引
任务序号：5
短标题：Distributed 索引
难度：advanced

## 中文导读

本题要求你完成 `Distribute 索引 Across Nodes`。

重点关注：`partitioned index`、`global index`、`scatter-gather`。

建议先按提示逐步实现：Partition 索引 by key hash or range。

协议字段、消息类型、输入输出格式请以本文件中的代码块和测试用例为准。

## 题目说明

Distribute your 索引 across multiple 节点:

1. Partition 索引 entries by key (hash or range)
2. Point lookups go to single partition
3. Range queries scatter to all partitions, gather results
4.处理partition rebalancing when 节点 join/leave

Choose between local secondary 索引 (partitioned，包含data)和global secondary 索引 (partitioned by 索引 key).

## 概念说明

### 索引 Partitioning

When an 索引 outgrows one machine, partition it. Hash partitioning spreads load evenly. Range partitioning preserves locality用于range queries but risks hot spots.

### Global vs Local Secondary 索引

Local secondary 索引: partitioned，包含data, requires scatter-gather用于queries. Global secondary 索引: partitioned by 索引 key, single lookup but writes update multiple partitions.

## 涉及概念

- `partitioned index`
- `global index`
- `scatter-gather`

## 实现提示

- Partition 索引 by key hash or range
- Route point queries to single partition
- Range queries need scatter-gather

## 测试用例

### 1. Partitioned insert和lookup

Multi-节点 test: 索引 partitioned across 3 节点 (n1, n2, n3)使用hash(key) % 3. Insert key "foo" (routes to partition 1 on n2). Get key "foo" should route to same partition n2和return value. Verify point queries go to single partition.

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
```

期望输出：

```text
{"src":"n1","dest":"c0","body":{"type":"init_ok","in_reply_to":1,"msg_id":0}}
```

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
