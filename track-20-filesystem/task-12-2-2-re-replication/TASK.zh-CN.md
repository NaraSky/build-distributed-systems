# 实现自动重新复制

英文标题：Implement Automatic Re-Replication
网页：<https://builddistributedsystem.com/tracks/filesystem/tasks/task-12-2-2-re-replication>

课程：20. 文件系统：容错与再平衡
任务序号：7
短标题：Re-Replication
难度：高级
子主题：Fault Tolerance and Rebalancing

## 中文导读

这道题要求你实现自动重新复制机制。当某台块服务器宕机后，它上面的数据块副本数就会低于目标值（通常是 3）。主节点需要自动检测这些"副本不足"的数据块，并从现有副本复制到新的服务器上，恢复到安全的副本数量。这是分布式文件系统自我修复能力的核心。

## 题目说明

当一台块服务器宕机时，它上面的数据块变成"副本不足"状态。主节点必须自动调度重新复制，将副本数恢复到目标值。

重新复制的算法：
1. **检测**：主节点发现某台服务器的心跳缺失，将其标记为宕机
2. **扫描**：找出所有原本存放在宕机服务器上的数据块，它们现在的副本数不足
3. **排优先级**：只剩 1 个副本的数据块最为紧急（再丢一台就彻底丢数据了），优先复制它们
4. **调度**：对于每个副本不足的数据块，选择一台尚未持有该块的健康服务器
5. **复制**：指示一个现有副本将数据发送到新服务器
6. **更新**：在主节点的元数据中，将新服务器加入该数据块的位置列表

```json
Request:  {"type": "check_replication", "msg_id": 1}
Response: {"type": "check_replication_ok", "in_reply_to": 1, "under_replicated": [
    {"chunk": "ch_001", "current_rf": 2, "target_rf": 3, "missing_on": ["cs3"]},
    {"chunk": "ch_005", "current_rf": 1, "target_rf": 3, "priority": "critical"}
]}

Request:  {"type": "replicate_chunk", "msg_id": 2, "chunk": "ch_005", "source": "cs1", "target": "cs4"}
Response: {"type": "replicate_chunk_ok", "in_reply_to": 2, "chunk": "ch_005", "new_rf": 2, "bytes_copied": 67108864}
```

## 涉及概念

- `re-replication`
- `under-replicated chunks`
- `replication factor`
- `failure recovery`

## 实现提示

- 当一台服务器宕机时，它上面的数据块的副本数会降到 3 以下
- 主节点扫描副本不足的数据块并调度重新复制
- 选择一台尚未持有该数据块的健康服务器作为新副本
- 从现有副本将数据复制到新服务器
- 优先处理：只剩 1 个副本的数据块最为紧急（距离数据丢失只差一次故障）

## 测试用例

### 1. 检查复制状态，发现副本不足的数据块

check_replication_ok 应当列出副本不足的数据块，包含 current_rf 和 target_rf。

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"check_replication","msg_id":2}}
```

期望输出：

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

### 2. 将数据块复制到新服务器

replicate_chunk_ok 应当显示 new_rf 大于之前的副本数。

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1","n2","n3","n4"]}}
{"src":"c1","dest":"n1","body":{"type":"replicate_chunk","msg_id":2,"chunk":"ch_005","source":"n2","target":"n4"}}
```

期望输出：

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

## 参考资料

- [HDFS Replication Management](https://hadoop.apache.org/docs/stable/hadoop-project-dist/hadoop-hdfs/HdfsDesign.html)：HDFS 中关于副本放置和重新复制策略的文档

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
