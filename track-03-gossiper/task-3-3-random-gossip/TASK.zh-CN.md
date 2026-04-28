# 实现随机邻居的点对点传播

英文标题：Implement Peer-to-Peer Gossip with Random Neighbors
网页：<https://builddistributedsystem.com/tracks/gossiper/tasks/task-3-3-random-gossip>

课程：3. 传播者：Gossip 信息传播
任务序号：3
短标题：随机传播
难度：进阶
子主题：朴素广播（洪泛）

## 中文导读

这道题让你实现一个 Gossip 协议——每个节点随机选择一些邻居来分享信息，而不是广播给所有人。这种方式在节点发生故障时更加健壮，同时也能把消息开销控制在合理范围内。理解随机传播是掌握真实分布式系统中 Gossip 协议的关键一步。

## 题目说明

实现一个 Gossip 协议（Gossip Protocol），让每个节点随机选择部分邻居来分享信息。这种方式在面对节点故障时具有较好的鲁棒性，同时消息开销也保持在合理水平。

## 概念说明

### Gossip 协议

Gossip 协议也叫流行病协议（Epidemic Protocol），它传播信息的方式就像疾病传播一样：每个"被感染"的节点随机选择若干个同伴进行"感染"。这种方式提供了概率性的消息送达保证，并且开销是可调节的。

打个比方，这就像办公室里的八卦——你不会把一个消息告诉所有人，而是随机跟几个同事说，然后他们又随机告诉别人，最终消息就传遍了整个办公室。

## 涉及概念

- `gossip protocol`
- `random selection`
- `probabilistic broadcast`

## 实现提示

- 随机选择一部分邻居进行消息传播
- 定期重试以提高可靠性
- 在传播速度和消息开销之间取得平衡

## 测试用例

### 1. 随机传播将消息扩散到所有节点

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

- [Epidemic Algorithms](https://www.cs.cornell.edu/courses/cs6410/2018fa/slides/18-gossip-epidemic.pdf)：关于流行病/Gossip 协议的学术概述

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
