# 添加 Replica Shards用于Fault Tolerance

英文标题：Add Replica Shards用于Fault Tolerance
网页：<https://builddistributedsystem.com/tracks/searcher/tasks/task-16-2-2-replica-shards>

课程：23. 搜索器：分布式搜索
任务序号：7
短标题：Replica Shards
难度：advanced
子主题：Distributed Sharding和复制

## 中文导读

本题要求你完成 `添加 Replica Shards用于Fault Tolerance`。

重点关注：`replica shard`、`replication`、`write propagation`、`read scaling`、`fault tolerance`。

建议先按提示逐步实现：Each primary 分片 has R replica shards on different 节点。

协议字段、消息类型、输入输出格式请以本文件中的代码块和测试用例为准。

## 题目说明

Replica shards provide 故障 tolerance和read scaling. Each primary 分片 has one or more replicas on different 节点.

**Write flow**:
1. Write 请求 arrives at the primary 分片
2. Primary indexes the document
3. Primary forwards the write to all replica shards in parallel
4. Each replica indexes the document和sends ACK
5. Primary returns success to the 客户端 after all replicas ACK

**Read flow**: reads can be served from any copy (primary or replica), distributing read load.

**故障 handling**: if a 节点，包含a primary dies, a replica is promoted to primary. If a 节点，包含a replica dies, a new replica is allocated on another 节点.

```JSON
请求:  {"type": "create_index", "msg_id": 1, "索引": "articles", "num_shards": 3, "num_replicas": 1}
响应: {"type": "create_index_ok", "in_reply_to": 1, "primary_shards": 3, "replica_shards": 3, "total_shards": 6}
```

## 涉及概念

- `replica shard`
- `replication`
- `write propagation`
- `read scaling`
- `fault tolerance`

## 实现提示

- Each primary 分片 has R replica shards on different 节点
- Writes go to the primary first, then propagate to all replicas
- Reads can be served from any replica (scaling read throughput)
- Primary wait用于replicas to acknowledge before returning success
- If a replica falls behind, it is marked as "unassigned" until it catches up

## 测试用例

### 1. 创建 索引，包含replicas

create_index_ok should show 3 primary + 3 replica = 6 total shards.

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1","n2","n3"]}}
{"src":"c1","dest":"n1","body":{"type":"create_index","msg_id":2,"index":"articles","num_shards":3,"num_replicas":1}}
```

期望输出：

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

### 2. Write propagates to replicas

doc_index_ok should confirm replica acknowledgement.

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

- [Elasticsearch Replication](https://www.elastic.co/guide/en/elasticsearch/reference/current/docs-replication.html)：Elasticsearch documentation on primary-replica 复制

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
