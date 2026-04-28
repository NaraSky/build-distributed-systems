# 实现 Document Sharding，包含Hash-Based Routing

英文标题：Implement Document Sharding，包含Hash-Based Routing
网页：<https://builddistributedsystem.com/tracks/searcher/tasks/task-16-2-1-shard-routing>

课程：23. 搜索器：分布式搜索
任务序号：6
短标题：分片 Routing
难度：advanced
子主题：Distributed Sharding和复制

## 中文导读

本题要求你完成 `实现 Document Sharding，包含Hash-Based Routing`。

重点关注：`sharding`、`hash routing`、`primary shard`、`shard assignment`、`horizontal scaling`。

建议先按提示逐步实现：Assign each document to a 分片使用hash(doc_id) % num_shards。

协议字段、消息类型、输入输出格式请以本文件中的代码块和测试用例为准。

## 题目说明

To handle datasets larger than a single machine, documents are distributed across N primary shards使用hash-based routing.

**分片 assignment**: `分片 = hash(doc_id) % num_primary_shards`. The number of primary shards is fixed at 索引 creation time和cannot be changed later (changing it would require rehashing all documents).

**索引 flow**:
1. 客户端 sends 索引 请求 to any 节点 (coordinator)
2. Coordinator calculates: `分片 = hash(doc._id) % N`
3. Coordinator routes the 请求 to the 节点 hosting that 分片
4. The 分片 indexes the document locally

**Search flow**: coordinator sends the query to ALL shards, each 分片 searches locally, coordinator merges results.

```JSON
请求:  {"type": "shard_route", "msg_id": 1, "doc_id": "abc123", "num_shards": 5}
响应: {"type": "shard_route_ok", "in_reply_to": 1, "分片": 3, "节点": "n2", "hash": 2048}
```

## 涉及概念

- `sharding`
- `hash routing`
- `primary shard`
- `shard assignment`
- `horizontal scaling`

## 实现提示

- Assign each document to a 分片使用hash(doc_id) % num_shards
- The number of primary shards is fixed at 索引 creation time
- Each 分片 is assigned to a 节点 — different shards can be on different 节点
- 索引 requests are routed to the correct 分片 based on the doc_id
- Search requests must be sent to ALL shards (scatter-gather pattern)

## 测试用例

### 1. Same doc_id always routes to same 分片

Both shard_route_ok responses should return the same 分片 number.

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

### 2. Different doc_ids distribute across shards

Different doc_ids should distribute across the 3 shards.

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

- [Elasticsearch Sharding](https://www.elastic.co/guide/en/elasticsearch/reference/current/scalability.html)：Elasticsearch documentation on sharding和scalability

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
