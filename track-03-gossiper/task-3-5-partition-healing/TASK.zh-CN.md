#处理Network Partition Healing和Resynchronization

英文标题：Handle Network Partition Healing和Resynchronization
网页：<https://builddistributedsystem.com/tracks/gossiper/tasks/task-3-5-partition-healing>

课程：3. 传播者：Gossip 信息传播
任务序号：5
短标题：Partition Healing
难度：advanced
子主题：Naive 广播 (Flooding)

## 中文导读

本题要求你完成 `Handle Network Partition Healing和Resynchronization`。

重点关注：`network partitions`、`resynchronization`、`anti-entropy`。

建议先按提示逐步实现：Detect when partitions heal。

协议字段、消息类型、输入输出格式请以本文件中的代码块和测试用例为准。

## 题目说明

Handle the scenario where 网络 partitions heal和previously isolated 节点 reconnect. Implement anti-entropy mechanisms to synchronize 消息 sets between 节点 that were separated.

## 概念说明

### Anti-Entropy

Anti-entropy protocols periodically compare state between 节点和resolve differences. When partitions heal, 节点 must reconcile their 消息 sets to ensure 最终一致性.

## 涉及概念

- `network partitions`
- `resynchronization`
- `anti-entropy`

## 实现提示

- Detect when partitions heal
- Exchange 消息 sets，包含reconnected 节点
- Use Merkle trees用于efficient sync
- Reply，包含broadcast_ok before forwarding to neighbors to ensure deterministic output ordering

## 测试用例

### 1. Nodes sync after partition heals

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1","n2"]}}
{"src":"c0","dest":"n1","body":{"type":"topology","msg_id":2,"topology":{"n1":["n2"],"n2":["n1"]}}}
{"src":"c1","dest":"n1","body":{"type":"broadcast","msg_id":3,"message":10}}
{"src":"c1","dest":"n1","body":{"type":"broadcast","msg_id":4,"message":20}}
{"src":"c2","dest":"n1","body":{"type":"read","msg_id":5}}
```

期望输出：

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
{"src": "n1", "dest": "c0", "body": {"type": "topology_ok", "in_reply_to": 2, "msg_id": 1}}
{"src": "n1", "dest": "c1", "body": {"type": "broadcast_ok", "in_reply_to": 3, "msg_id": 2}}
{"src": "n1", "dest": "n2", "body": {"type": "broadcast", "message": 10, "msg_id": 3}}
{"src": "n1", "dest": "c1", "body": {"type": "broadcast_ok", "in_reply_to": 4, "msg_id": 4}}
{"src": "n1", "dest": "n2", "body": {"type": "broadcast", "message": 20, "msg_id": 5}}
{"src": "n1", "dest": "c2", "body": {"type": "read_ok", "messages": [10, 20], "in_reply_to": 5, "msg_id": 6}}
```

## 参考资料

- [Anti-Entropy Protocols](https://www.cs.cornell.edu/home/rvr/papers/flowgossip.pdf)：Research on anti-entropy和synchronization

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
