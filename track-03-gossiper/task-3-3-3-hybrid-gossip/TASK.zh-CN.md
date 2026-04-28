# 实现树与八卦混合广播

英文标题：Implement Hybrid Tree and Gossip Broadcast
网页：<https://builddistributedsystem.com/tracks/gossiper/tasks/task-3-3-3-hybrid-gossip>

课程：3. 传播者：Gossip 信息传播
任务序号：13
短标题：混合八卦广播
难度：高级
子主题：Topology-Aware Gossip

## 中文导读

这道题让你把树广播和八卦传播两种方式结合起来。纯树广播速度快但不够可靠，纯八卦传播可靠但速度慢且浪费消息。混合方案取二者之长：先通过树快速分发，再用八卦轮次兜底补漏，从而同时获得低延迟和高可靠性。这是实际分布式系统中常用的经典设计思路。

## 题目说明

纯树广播速度快但很脆弱，纯八卦传播（Gossip）可靠但速度慢且浪费消息。**混合方案**利用树结构完成首次快速转发（高效、低延迟），再用八卦传播保障可靠性（补上遗漏的节点）。

你需要实现一个混合广播机制：
1. 收到广播时，立即通过树邻居转发
2. 定期将所有已知消息通过八卦方式发送给随机节点（补漏轮次）
3. 为每条消息记录投递路径（是通过树还是通过八卦送达的）

```json
请求:  {"type": "delivery_info", "msg_id": 1, "value": 42}
响应: {"type": "delivery_info_ok", "in_reply_to": 1, "value": 42, "delivered_via": "tree", "hops": 1}
```

```json
请求:  {"type": "hybrid_stats", "msg_id": 2}
响应: {"type": "hybrid_stats_ok", "in_reply_to": 2, "tree_deliveries": 8, "gossip_deliveries": 2, "total": 10}
```

## 涉及概念

- `hybrid broadcast`
- `tree overlay`
- `gossip fallback`
- `convergence speed`

## 实现提示

- 首跳使用树转发，实现快速投递（低延迟）
- 后台的八卦轮次负责补上被遗漏的节点（高可靠性）
- 记录每条消息是通过树还是八卦方式投递的
- 可以对比纯树、纯八卦和混合三种方式的收敛速度
- 混合方案兼顾了两种方式的优点

## 测试用例

### 1. 通过树广播并记录投递信息

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"topology","msg_id":2,"topology":{"n1":[]}}}
{"src":"c1","dest":"n1","body":{"type":"broadcast","msg_id":3,"message":42}}
{"src":"c1","dest":"n1","body":{"type":"delivery_info","msg_id":4,"value":42}}
```

期望输出：

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
{"src": "n1", "dest": "c1", "body": {"type": "topology_ok", "in_reply_to": 2, "msg_id": 1}}
{"src": "n1", "dest": "c1", "body": {"type": "broadcast_ok", "in_reply_to": 3, "msg_id": 2}}
{"src": "n1", "dest": "c1", "body": {"type": "delivery_info_ok", "value": 42, "delivered_via": "tree", "hops": 0, "in_reply_to": 4, "msg_id": 3}}
```

### 2. 零消息时的混合统计

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"hybrid_stats","msg_id":2}}
```

期望输出：

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
{"src": "n1", "dest": "c1", "body": {"type": "hybrid_stats_ok", "tree_deliveries": 0, "gossip_deliveries": 0, "total": 0, "in_reply_to": 2, "msg_id": 1}}
```

## 参考资料

- [Plumtree: Epidemic Broadcast Trees](https://asc.di.fct.unl.pt/~jleitao/pdf/srds07-leitao.pdf)：关于将树广播与八卦传播结合以实现高效广播的经典论文

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
