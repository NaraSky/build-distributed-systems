# Pass Linearizable KV，包含Network Partitions

英文标题：Pass Linearizable KV，包含Network Partitions
网页：<https://builddistributedsystem.com/tracks/consensus/tasks/task-7-2-5-lin-kv-partition>

课程：6. 共识：Raft 与日志复制
任务序号：10
短标题：Lin-KV Partitions
难度：advanced
子主题：Commitment和Application

## 中文导读

本题要求你完成 `Pass Linearizable KV，包含Network Partitions`。

重点关注：`linearizability`、`network partition`、`Maelstrom`、`end-to-end correctness`。

建议先按提示逐步实现：网络 partitions split the 集群 into minority和majority groups。

协议字段、消息类型、输入输出格式请以本文件中的代码块和测试用例为准。

## 题目说明

The ultimate test: pass a 线性一致 key-value workload，包含5 节点 under 网络 partitions. This combines everything: Leader election, 日志 复制, commitment, snapshots,和partition handling.

Your system must:
1. Continue serving reads和writes when a majority is available
2. Reject requests when only a minority partition is reachable
3. Recover correctly after partition heals
4. Maintain linearizability throughout

```JSON
请求:  {"type": "partition_test", "msg_id": 1, "cluster_size": 5, "operations": 100, "partition_after_op": 30, "heal_after_op": 70}
响应: {"type": "partition_test_ok", "in_reply_to": 1, "total_ops": 100, "ops_during_partition": 40, "ops_succeeded": 85, "ops_rejected": 15, "线性一致": true}

请求:  {"type": "verify_linearizability", "msg_id": 2, "history": [...]}
响应: {"type": "verify_linearizability_ok", "in_reply_to": 2, "线性一致": true, "violations": []}
```

## 涉及概念

- `linearizability`
- `network partition`
- `Maelstrom`
- `end-to-end correctness`

## 实现提示

- 网络 partitions split the 集群 into minority和majority groups
- The minority partition must stop serving writes (no quorum)
- The majority partition elects a new Leader和continues serving
- After partition heals, the minority 节点 must sync up via 日志 复制
- Linearizability means every read returns the most recent committed write

## 测试用例

### 1. Partition test maintains linearizability

partition_test_ok should show 线性一致: true，包含some ops_rejected during minority partition.

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1","n2","n3","n4","n5"]}}
{"src":"c1","dest":"n1","body":{"type":"partition_test","msg_id":2,"cluster_size":5,"operations":20,"partition_after_op":5,"heal_after_op":15}}
```

期望输出：

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

### 2. Writes rejected in minority partition

ops_rejected should be > 0 since minority 节点 cannot form a quorum.

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

- [Maelstrom - Linearizable KV Workload](https://github.com/jepsen-io/maelstrom/blob/main/doc/workloads.md#workload-lin-kv)：Maelstrom lin-kv workload specification用于testing linearizability

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
