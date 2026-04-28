# 在网络分区下通过线性一致性键值测试

英文标题：Pass Linearizable KV with Network Partitions
网页：<https://builddistributedsystem.com/tracks/consensus/tasks/task-7-2-5-lin-kv-partition>

课程：6. 共识：Raft 与日志复制
任务序号：10
短标题：线性一致性键值与网络分区
难度：高级
子主题：提交与应用

## 中文导读

这是终极测试：在 5 个节点的集群中，面对网络分区（Network Partition）的情况，你的系统仍然需要通过线性一致性（Linearizability）键值存储的正确性验证。这道题综合了前面所有内容——领导者选举、日志复制、提交、快照以及分区处理。如果你能通过这道题，说明你已经实现了一个真正可用的分布式共识系统。

## 题目说明

终极挑战：在 5 个节点、存在网络分区的环境下，通过线性一致性键值存储的正确性测试。这道题综合了所有之前学过的内容：领导者选举、日志复制、日志提交、快照和分区处理。

你的系统必须做到：
1. 当多数节点可用时，继续正常处理读写请求
2. 当只有少数节点可达时，拒绝请求
3. 分区恢复后，正确地重新同步
4. 全程保持线性一致性

```json
Request:  {"type": "partition_test", "msg_id": 1, "cluster_size": 5, "operations": 100, "partition_after_op": 30, "heal_after_op": 70}
Response: {"type": "partition_test_ok", "in_reply_to": 1, "total_ops": 100, "ops_during_partition": 40, "ops_succeeded": 85, "ops_rejected": 15, "linearizable": true}

Request:  {"type": "verify_linearizability", "msg_id": 2, "history": [...]}
Response: {"type": "verify_linearizability_ok", "in_reply_to": 2, "linearizable": true, "violations": []}
```

## 涉及概念

- `linearizability`
- `network partition`
- `Maelstrom`
- `end-to-end correctness`

## 实现提示

- 网络分区会将集群分成少数派和多数派两组
- 少数派分区必须停止处理写请求（因为无法达成多数派共识）
- 多数派分区会选出新领导者并继续正常服务
- 分区恢复后，少数派节点需要通过日志复制追上最新状态
- 线性一致性意味着每次读取都必须返回最近一次已提交的写入结果

## 测试用例

### 1. 分区测试下保持线性一致性

partition_test_ok 的结果应显示 linearizable 为 true，并且在少数派分区期间有部分请求被拒绝。

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1","n2","n3","n4","n5"]}}
{"src":"c1","dest":"n1","body":{"type":"partition_test","msg_id":2,"cluster_size":5,"operations":20,"partition_after_op":5,"heal_after_op":15}}
```

期望输出：

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

### 2. 少数派分区中写请求被拒绝

ops_rejected 应大于 0，因为少数派节点无法形成多数派共识。

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1","n2","n3","n4","n5"]}}
{"src":"c1","dest":"n1","body":{"type":"partition_test","msg_id":2,"cluster_size":5,"operations":10,"partition_after_op":2,"heal_after_op":8}}
```

期望输出：

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

## 参考资料

- [Maelstrom - Linearizable KV Workload](https://github.com/jepsen-io/maelstrom/blob/main/doc/workloads.md#workload-lin-kv)：Maelstrom 线性一致性键值工作负载规范，用于测试系统的线性一致性

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
