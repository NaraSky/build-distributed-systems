# 实现基于哈希路由的文档分片

英文标题：Implement Document Sharding with Hash-Based Routing
网页：<https://builddistributedsystem.com/tracks/searcher/tasks/task-16-2-1-shard-routing>

课程：23. 搜索引擎
任务序号：6
短标题：分片路由
难度：高级
子主题：分布式分片与复制

## 中文导读

这道题要求你实现文档的分片路由（Shard Routing），将文档通过哈希函数分配到不同的分片上。当数据量超出单台机器的容量时，分片是实现水平扩展的核心手段，就像把一本厚书拆成几册分别存放。

## 题目说明

为了处理超出单台机器容量的数据集，文档通过哈希路由分散到 N 个主分片（Primary Shard）上。

**分片分配公式**：`分片编号 = hash(doc_id) % 主分片数量`。主分片的数量在索引创建时就固定了，之后不能更改（更改意味着要重新哈希所有文档）。

**索引流程**：
1. 客户端将索引请求发送到任意节点（协调节点）
2. 协调节点计算：`分片编号 = hash(doc._id) % N`
3. 协调节点将请求转发到持有该分片的节点
4. 该分片在本地完成文档的索引

**搜索流程**：协调节点将查询发送到所有分片，每个分片在本地执行搜索，协调节点合并各分片的结果。

```json
Request:  {"type": "shard_route", "msg_id": 1, "doc_id": "abc123", "num_shards": 5}
Response: {"type": "shard_route_ok", "in_reply_to": 1, "shard": 3, "node": "n2", "hash": 2048}
```

## 涉及概念

- sharding
- hash routing
- primary shard
- shard assignment
- horizontal scaling

## 实现提示

- 使用 `hash(doc_id) % num_shards` 将每个文档分配到对应的分片
- 主分片的数量在索引创建时就已固定
- 每个分片被分配到一个节点上，不同的分片可以在不同的节点上
- 索引请求根据文档编号路由到正确的分片
- 搜索请求必须发送到所有分片（分散-聚合模式）

## 测试用例

### 1. 相同的文档编号始终路由到同一分片

两次 `shard_route_ok` 响应应返回相同的分片编号。

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1","n2"]}}
{"src":"c1","dest":"n1","body":{"type":"shard_route","msg_id":2,"doc_id":"abc","num_shards":5}}
{"src":"c1","dest":"n1","body":{"type":"shard_route","msg_id":3,"doc_id":"abc","num_shards":5}}
```

期望输出：

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

### 2. 不同的文档编号分布到不同分片

不同的文档编号应分布在 3 个分片上。

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"shard_route","msg_id":2,"doc_id":"a","num_shards":3}}
{"src":"c1","dest":"n1","body":{"type":"shard_route","msg_id":3,"doc_id":"b","num_shards":3}}
{"src":"c1","dest":"n1","body":{"type":"shard_route","msg_id":4,"doc_id":"c","num_shards":3}}
```

期望输出：

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

## 参考资料

- [Elasticsearch Sharding](https://www.elastic.co/guide/en/elasticsearch/reference/current/scalability.html)：关于分片和可扩展性的官方文档

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
