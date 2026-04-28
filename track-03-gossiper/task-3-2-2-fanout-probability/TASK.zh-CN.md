# 计算可靠投递所需的最小扇出值

英文标题：Calculate Minimum Fanout for Reliable Delivery
网页：<https://builddistributedsystem.com/tracks/gossiper/tasks/task-3-2-2-fanout-probability>

课程：3. 传播者：Gossip 信息传播
任务序号：7
短标题：扇出概率分析
难度：高级
子主题：Gossip 协议

## 中文导读

这道题将 Gossip 协议的理论分析付诸实践——给定 N 个节点，扇出值 K 至少是多少才能保证消息以不低于 99% 的概率到达所有节点？你需要实现概率计算公式，并通过蒙特卡洛模拟来验证理论结果。这能帮助你理解如何在实际系统中选择合适的 Gossip 参数。

## 题目说明

扇出值 K 需要多大，才能保证所有 N 个节点都以不低于 0.99 的概率收到消息？理论告诉我们，经过 R 轮扇出为 K 的 Gossip 传播后，某个特定节点没有收到消息的概率约为 (1 - K/N)^R。

你需要完成以下任务：
1. 实现概率计算公式：P(未收到) = (1 - K/(N-1))^R
2. 对于给定的 N 和目标概率，找到最小的 K 值
3. 通过模拟 Gossip 轮次来验证理论结果

实现 `calc_fanout` 处理器：
```json
Request:  {"type": "calc_fanout", "msg_id": 1, "nodes": 25, "target_prob": 0.99, "rounds": 5}
Response: {"type": "calc_fanout_ok", "in_reply_to": 1, "min_fanout": 3, "miss_prob": 0.003}
```

以及 `simulate_gossip` 处理器，用于运行蒙特卡洛模拟：
```json
Request:  {"type": "simulate_gossip", "msg_id": 2, "nodes": 25, "fanout": 2, "rounds": 10, "trials": 100}
Response: {"type": "simulate_gossip_ok", "in_reply_to": 2, "delivery_rate": 0.98, "avg_rounds_to_all": 4.7}
```

## 涉及概念

- `probability`
- `gossip reliability`
- `fanout analysis`
- `convergence`

## 实现提示

- 一个节点在单轮中未收到消息的概率为：(1 - K/N)^R，其中 R 是轮次数
- 要在 N 个节点中实现 99% 的投递率，需要根据 Gossip 轮次数来求解 K 值
- 轮次越多，所需的 K 值越小，但延迟也越高
- 通常 log(N) 轮、扇出 K=2 就能达到较高的投递概率
- 实现一个模拟程序来验证理论公式的准确性

## 测试用例

### 1. 为小集群计算扇出值

验证说明：`calc_fanout_ok` 的响应中，`min_fanout` 应不小于 1，且 `miss_prob` 应小于 0.01。

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"calc_fanout","msg_id":2,"nodes":5,"target_prob":0.99,"rounds":5}}
```

期望输出：

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

### 2. 模拟 Gossip 并返回投递率

验证说明：`simulate_gossip_ok` 的响应中，`delivery_rate` 应在 0 到 1 之间，`avg_rounds_to_all` 应大于 0。

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"simulate_gossip","msg_id":2,"nodes":10,"fanout":3,"rounds":5,"trials":50}}
```

期望输出：

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

## 参考资料

- [Gossip Protocols - Cornell](https://www.cs.cornell.edu/courses/cs6410/2020fa/slides/22-gossip.pdf)：康奈尔大学关于 Gossip 协议分析与收敛性的课程讲义

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
