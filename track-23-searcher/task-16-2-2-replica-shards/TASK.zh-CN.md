# 添加副本分片实现容错

英文标题：Add Replica Shards for Fault Tolerance
网页：<https://builddistributedsystem.com/tracks/searcher/tasks/task-16-2-2-replica-shards>

课程：23. 搜索引擎
任务序号：7
短标题：副本分片
难度：高级
子主题：分布式分片与复制

## 中文导读

这道题要求你为主分片添加副本分片（Replica Shard），实现数据冗余。副本分片就像数据的"备份"，一方面提高容错能力（某台机器宕机了数据不会丢），另一方面可以分担读取压力，提升搜索吞吐量。

## 题目说明

副本分片（Replica Shard）提供容错能力和读取扩展。每个主分片在不同节点上拥有一个或多个副本。

**写入流程**：
1. 写请求到达主分片
2. 主分片索引文档
3. 主分片将写操作并行转发到所有副本分片
4. 每个副本索引文档并发送确认
5. 主分片在收到所有副本确认后，向客户端返回成功

**读取流程**：读取请求可以由任意副本（包括主分片和副本分片）来处理，从而分散读取负载。

**故障处理**：如果持有主分片的节点宕机，其中一个副本会被提升为新的主分片。如果持有副本的节点宕机，系统会在其他节点上重新分配一个新的副本。

```json
Request:  {"type": "create_index", "msg_id": 1, "index": "articles", "num_shards": 3, "num_replicas": 1}
Response: {"type": "create_index_ok", "in_reply_to": 1, "primary_shards": 3, "replica_shards": 3, "total_shards": 6}
```

## 涉及概念

- replica shard
- replication
- write propagation
- read scaling
- fault tolerance

## 实现提示

- 每个主分片有 R 个副本分片，分布在不同节点上
- 写操作先到主分片，再传播到所有副本
- 读请求可以由任意副本处理（从而提升读取吞吐量）
- 主分片需要等待所有副本确认后才返回写入成功
- 如果某个副本落后了，将其标记为"未分配"状态，直到追上进度

## 测试用例

### 1. 创建带副本的索引

`create_index_ok` 应显示 3 个主分片 + 3 个副本分片 = 共 6 个分片。

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1","n2","n3"]}}
{"src":"c1","dest":"n1","body":{"type":"create_index","msg_id":2,"index":"articles","num_shards":3,"num_replicas":1}}
```

期望输出：

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

### 2. 写操作传播到副本

`doc_index_ok` 应确认副本已完成同步。

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1","n2"]}}
{"src":"c1","dest":"n1","body":{"type":"doc_index","msg_id":2,"index":"articles","doc":{"title":"test"},"wait_for_replicas":true}}
```

期望输出：

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

## 参考资料

- [Elasticsearch Replication](https://www.elastic.co/guide/en/elasticsearch/reference/current/docs-replication.html)：关于主副本复制机制的官方文档

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
