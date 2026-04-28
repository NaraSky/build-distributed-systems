# 处理节点故障与副本提升

英文标题：Handle Node Failure with Replica Promotion
网页：<https://builddistributedsystem.com/tracks/searcher/tasks/task-16-2-5-node-failure>

课程：23. 搜索引擎
任务序号：10
短标题：节点故障处理
难度：高级
子主题：分布式分片与复制

## 中文导读

这道题要求你处理节点故障的场景：当一个节点宕机时，系统需要将其上的副本分片提升为主分片，并在健康节点上重新分配丢失的副本。这是分布式搜索引擎保持高可用的关键机制，确保部分机器挂掉也不影响服务。

## 题目说明

当某个节点发生故障时，集群必须将副本分片提升为主分片，并重新分配丢失的副本，以维持所需的副本数量。

**故障处理流程**：
1. 集群主节点检测到节点故障（连续 30 秒未收到心跳）
2. 将故障节点上的每个主分片的一个副本提升为新的主分片
3. 将故障节点上的每个副本分片标记为"未分配"
4. 在健康节点上分配新的副本，以恢复预定的副本数量
5. 新副本从其主分片同步数据（恢复过程）

**恢复**：当故障节点重新上线后，它上面的过期分片会从当前的主分片同步数据。如果数据差异较小，使用增量同步；否则执行全量复制。

```json
Request:  {"type": "node_failure", "msg_id": 1, "failed_node": "n2"}
Response: {"type": "node_failure_ok", "in_reply_to": 1, "primaries_promoted": 2, "replicas_unassigned": 3, "recovery_started": true}
```

## 涉及概念

- node failure
- replica promotion
- unassigned shards
- recovery
- shard reallocation

## 实现提示

- 当节点故障时，必须通过提升副本来替代其上的主分片
- 集群主节点通过心跳超时来检测节点故障
- 对于故障节点上的每个主分片，将其一个副本提升为新的主分片
- 丢失的副本进入"未分配"状态，并被重新分配到健康节点上
- 当故障节点恢复后，从当前的主分片同步数据

## 测试用例

### 1. 节点故障时副本被提升

`node_failure_ok` 应显示 `primaries_promoted >= 0` 且 `recovery_started: true`。

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1","n2","n3"]}}
{"src":"c1","dest":"n1","body":{"type":"node_failure","msg_id":2,"failed_node":"n2"}}
```

期望输出：

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

### 2. 未分配的副本被重新分配

`cluster_health` 初始应显示 `unassigned_shards > 0`，重新分配后变为 0。

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

- [Elasticsearch Recovery](https://www.elastic.co/guide/en/elasticsearch/reference/current/modules-gateway.html)：关于分片恢复和节点故障处理的官方文档

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
