# 实现节点加入时的分片再平衡

英文标题：Implement Shard Rebalancing on Node Join
网页：<https://builddistributedsystem.com/tracks/searcher/tasks/task-16-2-4-shard-rebalance>

课程：23. 搜索引擎
任务序号：9
短标题：分片再平衡
难度：高级
子主题：分布式分片与复制

## 中文导读

这道题要求你实现分片再平衡（Shard Rebalance）机制：当新节点加入集群时，将分片重新分配以均衡各节点的负载。这就像新来了一个人帮忙搬东西，你需要把原来几个人手里的货物重新分一下，让大家都不那么累。

## 题目说明

当新节点加入集群时，需要重新分配分片以均衡所有节点的负载。这是一个后台操作，不能中断正在进行的搜索。

**再平衡算法**：
1. 计算每个节点的目标分片数：`ceil(总分片数 / 节点数)`
2. 找出过载节点（分片数超过目标值）和欠载节点
3. 将过载节点上多余的分片迁移到欠载节点

**迁移过程**：
1. 在后台开始将分片数据从源节点复制到目标节点
2. 复制期间，源节点继续提供读写服务
3. 复制完成后，将新的写请求重定向到目标节点
4. 追加复制期间产生的写操作（追赶阶段）
5. 标记迁移完成，从源节点移除该分片

```json
Request:  {"type": "rebalance", "msg_id": 1, "index": "articles"}
Response: {"type": "rebalance_ok", "in_reply_to": 1, "shards_moved": 2, "source_nodes": ["n1", "n2"], "target_nodes": ["n3"], "duration_ms": 5000}
```

## 涉及概念

- shard rebalancing
- shard migration
- background operation
- even distribution
- node join

## 实现提示

- 当新节点加入时，将部分分片迁移过去以均衡负载
- 计算目标：每个节点大约持有 `总分片数 / 节点数` 个分片
- 迁移是后台操作：先复制分片数据，再更新路由信息
- 迁移期间，源分片继续处理请求
- 迁移完成后，将新请求重定向到目标节点

## 测试用例

### 1. 再平衡后分片均匀分布

`rebalance_ok` 应显示有分片被移动，以实现均匀分布。

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1","n2","n3"]}}
{"src":"c1","dest":"n1","body":{"type":"rebalance","msg_id":2,"index":"articles"}}
```

期望输出：

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

### 2. 已平衡时不进行迁移

如果分片已经均匀分布，`shards_moved` 应为 0。

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

- [Elasticsearch Shard Allocation](https://www.elastic.co/guide/en/elasticsearch/reference/current/modules-cluster.html)：关于分片分配和再平衡的官方文档

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
