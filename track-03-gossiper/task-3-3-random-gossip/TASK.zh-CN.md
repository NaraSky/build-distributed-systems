# 实现 Peer-to-Peer Gossip，包含Random Neighbors

英文标题：Implement Peer-to-Peer Gossip，包含Random Neighbors
网页：<https://builddistributedsystem.com/tracks/gossiper/tasks/task-3-3-random-gossip>

课程：3. 传播者：Gossip 信息传播
任务序号：3
短标题：Random Gossip
难度：intermediate
子主题：Naive 广播 (Flooding)

## 中文导读

本题要求你完成 `实现 Peer-to-Peer Gossip，包含Random Neighbors`。

重点关注：`gossip protocol`、`random selection`、`probabilistic broadcast`。

建议先按提示逐步实现：Randomly select a subset of neighbors。

协议字段、消息类型、输入输出格式请以本文件中的代码块和测试用例为准。

## 题目说明

Implement a gossip protocol where each 节点 randomly selects neighbors to share information with. This provides robustness against 节点 failures while keeping 消息 overhead reasonable.

## 概念说明

### Gossip Protocols

gossip, or epidemic, protocols spread information like a disease. Each infected 节点 randomly selects peers to infect. This provides probabilistic guarantees of delivery，包含tunable overhead.

## 涉及概念

- `gossip protocol`
- `random selection`
- `probabilistic broadcast`

## 实现提示

- Randomly select a subset of neighbors
- 重试 periodically用于reliability
- Balance between speed和overhead

## 测试用例

### 1.随机Gossip spreads 消息 to all nodes

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c0","dest":"n1","body":{"type":"topology","msg_id":2,"topology":{"n1":[]}}}
{"src":"c1","dest":"n1","body":{"type":"broadcast","msg_id":3,"message":99}}
{"src":"c1","dest":"n1","body":{"type":"read","msg_id":4}}
```

期望输出：

```text
{"src":"n1","dest":"c0","body":{"type":"init_ok","in_reply_to":1,"msg_id":0}}
{"src":"n1","dest":"c0","body":{"type":"topology_ok","in_reply_to":2,"msg_id":1}}
{"src":"n1","dest":"c1","body":{"type":"broadcast_ok","in_reply_to":3,"msg_id":2}}
{"src":"n1","dest":"c1","body":{"type":"read_ok","in_reply_to":4,"msg_id":3,"messages":[99]}}
```

## 参考资料

- [Epidemic Algorithms](https://www.cs.cornell.edu/courses/cs6410/2018fa/slides/18-gossip-epidemic.pdf)：Academic overview of epidemic/gossip protocols

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
