# Calculate Minimum Fanout用于Reliable Delivery

英文标题：Calculate Minimum Fanout用于Reliable Delivery
网页：<https://builddistributedsystem.com/tracks/gossiper/tasks/task-3-2-2-fanout-probability>

课程：3. 传播者：Gossip 信息传播
任务序号：7
短标题：Fanout Probability
难度：advanced
子主题：Gossip Protocol

## 中文导读

本题要求你完成 `Calculate Minimum Fanout用于Reliable Delivery`。

重点关注：`probability`、`gossip reliability`、`fanout analysis`、`convergence`。

建议先按提示逐步实现：Probability of a 节点 NOT receiving a 消息 in one round: (1 - K/N)^R where R is rounds。

协议字段、消息类型、输入输出格式请以本文件中的代码块和测试用例为准。

## 题目说明

What fanout K guarantees that all N 节点 receive a 消息，包含probability >= 0.99? The theory says that after R rounds of gossip，包含fanout K, the probability that a specific 节点 has NOT received the 消息 is approximately (1 - K/N)^R.

Your task is to:
1. Implement the probability calculation: P(miss) = (1 - K/(N-1))^R
2. Find minimum K用于a given N和target probability
3. Simulate gossip rounds to verify empirically

Implement a `calc_fanout` handler:
```JSON
请求:  {"type": "calc_fanout", "msg_id": 1, "节点": 25, "target_prob": 0.99, "rounds": 5}
响应: {"type": "calc_fanout_ok", "in_reply_to": 1, "min_fanout": 3, "miss_prob": 0.003}
```

And a `simulate_gossip` handler that runs a Monte Carlo simulation:
```JSON
请求:  {"type": "simulate_gossip", "msg_id": 2, "节点": 25, "fanout": 2, "rounds": 10, "trials": 100}
响应: {"type": "simulate_gossip_ok", "in_reply_to": 2, "delivery_rate": 0.98, "avg_rounds_to_all": 4.7}
```

## 涉及概念

- `probability`
- `gossip reliability`
- `fanout analysis`
- `convergence`

## 实现提示

- Probability of a 节点 NOT receiving a 消息 in one round: (1 - K/N)^R where R is rounds
- For 99% delivery across N 节点, solve用于K given the number of gossip rounds
- More rounds = lower K needed, but more latency
- 日志(N) rounds，包含fanout K=2 typically suffices用于high probability delivery
- Implement a simulation to verify the theoretical formula empirically

## 测试用例

### 1. Calculate fanout用于small cluster

calc_fanout_ok should have min_fanout >= 1和miss_prob < 0.01.

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"calc_fanout","msg_id":2,"nodes":5,"target_prob":0.99,"rounds":5}}
```

期望输出：

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

### 2. Simulate Gossip returns delivery rate

simulate_gossip_ok should have delivery_rate between 0和1,和avg_rounds_to_all > 0.

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

- [Gossip Protocols - Cornell](https://www.cs.cornell.edu/courses/cs6410/2020fa/slides/22-gossip.pdf)：Cornell lecture on gossip protocol analysis和convergence

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
