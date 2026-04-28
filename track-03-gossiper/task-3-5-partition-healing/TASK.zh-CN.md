# 处理网络分区恢复与数据重新同步

英文标题：Handle Network Partition Healing and Resynchronization
网页：<https://builddistributedsystem.com/tracks/gossiper/tasks/task-3-5-partition-healing>

课程：3. 传播者：Gossip 信息传播
任务序号：5
短标题：分区恢复
难度：高级
子主题：朴素广播（洪泛）

## 中文导读

这道题模拟的是一个真实场景：网络分区（Network Partition）恢复后，之前被隔离的节点重新连接，它们之间的数据该如何同步？你需要实现反熵（Anti-Entropy）机制，确保分区恢复后所有节点最终达成一致。这是分布式系统中最棘手也最重要的问题之一。

## 题目说明

处理网络分区恢复后节点重新连接的场景。实现反熵机制，在曾经被分隔开的节点之间同步消息集合。

想象两个办公室之间的网线断了一段时间，各自收到了不同的消息。网线修好后，两边需要互相交换这段时间内各自收到的消息，确保双方最终拥有完全一致的信息。

## 概念说明

### 反熵

反熵（Anti-Entropy）协议会定期比较各节点之间的状态，并解决差异。当网络分区恢复后，节点必须协调各自的消息集合，以确保最终一致性（Eventual Consistency）。

## 涉及概念

- `network partitions`
- `resynchronization`
- `anti-entropy`

## 实现提示

- 检测分区何时恢复
- 与重新连接的节点交换消息集合
- 可以使用默克尔树（Merkle Tree）来实现高效同步
- 先回复 `broadcast_ok`，再转发给邻居节点，以确保输出的顺序是确定性的

## 测试用例

### 1. 分区恢复后节点间同步数据

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

- [Anti-Entropy Protocols](https://www.cs.cornell.edu/home/rvr/papers/flowgossip.pdf)：关于反熵与同步机制的研究论文

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
