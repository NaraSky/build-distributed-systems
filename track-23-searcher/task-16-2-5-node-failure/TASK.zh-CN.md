#处理Node Failure，包含Replica Promotion

英文标题：Handle节点Failure，包含Replica Promotion
网页：<https://builddistributedsystem.com/tracks/searcher/tasks/task-16-2-5-node-failure>

课程：23. 搜索器：分布式搜索
任务序号：10
短标题：Node Failure
难度：advanced
子主题：Distributed Sharding和复制

## 中文导读

本题要求你完成 `Handle节点Failure，包含Replica Promotion`。

重点关注：`node failure`、`replica promotion`、`unassigned shards`、`recovery`、`shard reallocation`。

建议先按提示逐步实现：When a 节点 fails, its primary shards must be replaced by promoting replicas。

协议字段、消息类型、输入输出格式请以本文件中的代码块和测试用例为准。

## 题目说明

When a 节点 fails, the 集群 must promote replica shards to primary和reallocate lost replicas to maintain the desired 复制 factor.

**故障 handling flow**:
1. 集群 master detects 节点 故障 (missed heartbeats用于30s)
2. For each primary 分片 on the failed 节点: promote a replica to primary
3. For each replica 分片 on the failed 节点: mark as "unassigned"
4. Allocate new replicas on healthy 节点 to restore the 复制 factor
5. New replicas sync from their primaries (recovery)

**Recovery**: when the failed 节点 comes back online, its stale shards sync from the current primaries. If the data delta is small, an incremental sync is used; otherwise, a full copy.

```JSON
请求:  {"type": "node_failure", "msg_id": 1, "failed_node": "n2"}
响应: {"type": "node_failure_ok", "in_reply_to": 1, "primaries_promoted": 2, "replicas_unassigned": 3, "recovery_started": true}
```

## 涉及概念

- `node failure`
- `replica promotion`
- `unassigned shards`
- `recovery`
- `shard reallocation`

## 实现提示

- When a 节点 fails, its primary shards must be replaced by promoting replicas
- The 集群 master detects 节点 故障 via missed heartbeats
- For each primary on the failed 节点: promote a replica to primary
- The lost replicas go into "unassigned" state和are reallocated to healthy 节点
- When the failed 节点 recovers, it syncs from the current primaries

## 测试用例

### 1. Replicas promoted on node failure

node_failure_ok should show primaries_promoted >= 0和recovery_started: true.

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1","n2","n3"]}}
{"src":"c1","dest":"n1","body":{"type":"node_failure","msg_id":2,"failed_node":"n2"}}
```

期望输出：

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

### 2. Unassigned replicas are reallocated

cluster_health should show unassigned_shards > 0 initially, then 0 after reallocation.

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1","n2","n3"]}}
{"src":"c1","dest":"n1","body":{"type":"node_failure","msg_id":2,"failed_node":"n3"}}
{"src":"c1","dest":"n1","body":{"type":"cluster_health","msg_id":3}}
```

期望输出：

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

## 参考资料

- [Elasticsearch Recovery](https://www.elastic.co/guide/en/elasticsearch/reference/current/modules-gateway.html)：Elasticsearch documentation on 分片 recovery和节点 故障 handling

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
