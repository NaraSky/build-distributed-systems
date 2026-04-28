# 模拟网络分区与恢复

英文标题：Simulate Network Partition and Healing
网页：<https://builddistributedsystem.com/tracks/gossiper/tasks/task-3-3-5-partition-heal>

课程：3. 传播者：Gossip 信息传播
任务序号：15
短标题：分区恢复
难度：高级
子主题：Topology-Aware Gossip

## 中文导读

这道题让你模拟网络分区（Network Partition）及其恢复过程。网络分区就像一堵墙把集群劈成两半，两边各自运行、互不相通。当这堵墙消失（分区恢复）后，两边需要通过八卦传播重新同步各自产生的数据。这是理解分布式系统中"脑裂"问题和最终一致性的重要练习。

## 题目说明

网络分区（Network Partition）会将集群分割成若干个互相隔离的组。分区恢复后，八卦传播必须将各组在分区期间产生的不同状态合并起来。你的任务就是模拟这个过程。

需要实现以下功能：
1. `partition` - 屏蔽发往指定节点的消息
2. `heal` - 解除所有屏蔽
3. `partition_status` - 报告当前的分区状态

```json
请求:  {"type": "partition", "msg_id": 1, "blocked": ["n3", "n4"]}
响应: {"type": "partition_ok", "in_reply_to": 1}

请求:  {"type": "heal", "msg_id": 2}
响应: {"type": "heal_ok", "in_reply_to": 2}

请求:  {"type": "partition_status", "msg_id": 3}
响应: {"type": "partition_status_ok", "in_reply_to": 3, "blocked": [], "is_partitioned": false, "messages_dropped": 5}
```

## 涉及概念

- `network partition`
- `partition healing`
- `convergence`
- `split brain`

## 实现提示

- 分区会阻断两组节点之间的所有消息传递
- 分区期间，每一侧的节点继续在内部进行八卦传播
- 分区恢复后，跨分区的八卦传播恢复，各侧的状态逐渐趋于一致
- 记录分区恢复后达到一致所需的时间
- 可以用一个"被屏蔽的目标节点集合"来实现分区效果

## 测试用例

### 1. 分区正确屏蔽指定节点

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1","n2"]}}
{"src":"c1","dest":"n1","body":{"type":"partition","msg_id":2,"blocked":["n2"]}}
{"src":"c1","dest":"n1","body":{"type":"partition_status","msg_id":3}}
```

期望输出：

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
{"src": "n1", "dest": "c1", "body": {"type": "partition_ok", "in_reply_to": 2, "msg_id": 1}}
{"src": "n1", "dest": "c1", "body": {"type": "partition_status_ok", "blocked": ["n2"], "is_partitioned": true, "messages_dropped": 0, "in_reply_to": 3, "msg_id": 2}}
```

### 2. 恢复操作解除所有屏蔽

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1","n2"]}}
{"src":"c1","dest":"n1","body":{"type":"partition","msg_id":2,"blocked":["n2"]}}
{"src":"c1","dest":"n1","body":{"type":"heal","msg_id":3}}
{"src":"c1","dest":"n1","body":{"type":"partition_status","msg_id":4}}
```

期望输出：

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
{"src": "n1", "dest": "c1", "body": {"type": "partition_ok", "in_reply_to": 2, "msg_id": 1}}
{"src": "n1", "dest": "c1", "body": {"type": "heal_ok", "in_reply_to": 3, "msg_id": 2}}
{"src": "n1", "dest": "c1", "body": {"type": "partition_status_ok", "blocked": [], "is_partitioned": false, "messages_dropped": 0, "in_reply_to": 4, "msg_id": 3}}
```

## 参考资料

- [Jepsen: Network Partitions](https://jepsen.io/analyses)：Jepsen 对各种数据库在网络分区下表现的分析报告

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
