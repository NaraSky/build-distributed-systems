# 调优 Gossip 参数以应对 Maelstrom 广播测试

英文标题：Tune Gossip Parameters for Maelstrom Broadcast
网页：<https://builddistributedsystem.com/tracks/gossiper/tasks/task-3-2-5-tuning>

课程：3. 传播者：Gossip 信息传播
任务序号：10
短标题：Gossip 调优
难度：高级
子主题：Gossip 协议

## 中文导读

这道题是 Gossip 协议系列的综合实践——Maelstrom 广播测试要求在网络分区条件下，每次操作产生的消息数不超过 30 条。你需要实现可配置的 Gossip 参数，并通过统计接口跟踪消息效率。这是把前面学到的理论知识应用到实际性能调优的过程。

## 题目说明

Maelstrom 广播测试要求在网络分区的情况下，每次操作产生的消息数（messages-per-op）小于 30。你的任务是实现可配置的 Gossip 参数，并跟踪消息传递效率。

实现 `configure` 处理器来设置 Gossip 参数：
```json
Request:  {"type": "configure", "msg_id": 1, "fanout": 3, "gossip_interval_ms": 200}
Response: {"type": "configure_ok", "in_reply_to": 1}
```

以及 `gossip_stats` 处理器来报告效率指标：
```json
Request:  {"type": "gossip_stats", "msg_id": 2}
Response: {"type": "gossip_stats_ok", "in_reply_to": 2, 
           "broadcasts_received": 10, "gossip_messages_sent": 45,
           "messages_per_op": 4.5, "unique_messages": 10}
```

## 涉及概念

- `parameter tuning`
- `messages-per-op`
- `latency tradeoff`
- `gossip optimization`

## 实现提示

- 每次操作消息数 = 总发送消息数 / 总广播操作数
- 扇出值越小，消息越少，但收敛越慢
- Gossip 间隔越长，轮次越少，但延迟越高
- 最佳参数是在消息开销和投递可靠性之间找到的平衡点
- 同时跟踪两项指标，并通过统计接口对外暴露

## 测试用例

### 1. 配置更新扇出值

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1","n2","n3"]}}
{"src":"c1","dest":"n1","body":{"type":"configure","msg_id":2,"fanout":3,"gossip_interval_ms":100}}
```

期望输出：

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
{"src": "n1", "dest": "c1", "body": {"type": "configure_ok", "in_reply_to": 2, "msg_id": 1}}
```

### 2. 零广播时的统计信息

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"gossip_stats","msg_id":2}}
```

期望输出：

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
{"src": "n1", "dest": "c1", "body": {"type": "gossip_stats_ok", "broadcasts_received": 0, "gossip_messages_sent": 0, "messages_per_op": 0, "unique_messages": 0, "in_reply_to": 2, "msg_id": 1}}
```

## 参考资料

- [Fly.io Gossip Glomers - Broadcast](https://fly.io/dist-sys/3a/)：Fly.io 分布式系统广播挑战题

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
