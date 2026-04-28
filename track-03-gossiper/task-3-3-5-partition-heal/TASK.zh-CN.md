# Simulate Network Partition和Healing

英文标题：Simulate Network Partition和Healing
网页：<https://builddistributedsystem.com/tracks/gossiper/tasks/task-3-3-5-partition-heal>

课程：3. 传播者：Gossip 信息传播
任务序号：15
短标题：Partition Heal
难度：advanced
子主题：Topology-Aware Gossip

## 中文导读

本题要求你完成 `Simulate Network Partition和Healing`。

重点关注：`network partition`、`partition healing`、`convergence`、`split brain`。

建议先按提示逐步实现：A partition blocks all 消息 between two groups of 节点。

协议字段、消息类型、输入输出格式请以本文件中的代码块和测试用例为准。

## 题目说明

网络 partitions split the 集群 into isolated groups. After the partition heals, gossip must merge the diverged states. Your task is to simulate this.

Implement:
1. `partition` - Block 消息 to specified 节点
2. `heal` - Unblock all 节点  
3. `partition_status` - Report current partition state

```JSON
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

- A partition blocks all 消息 between two groups of 节点
- Each side continues to gossip internally
- On healing, cross-partition gossip resumes和states converge
- Track time-to-convergence after partition heals
- Implement partition as a blocked-destinations set

## 测试用例

### 1. Partition blocks specified nodes

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

### 2. Heal removes all blocks

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

- [Jepsen: Network Partitions](https://jepsen.io/analyses)：Jepsen analyses of how databases handle 网络 partitions

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
