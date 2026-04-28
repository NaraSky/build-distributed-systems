# Tune Gossip Parameters用于Maelstrom 广播

英文标题：Tune Gossip Parameters用于Maelstrom Broadcast
网页：<https://builddistributedsystem.com/tracks/gossiper/tasks/task-3-2-5-tuning>

课程：3. 传播者：Gossip 信息传播
任务序号：10
短标题：Gossip Tuning
难度：advanced
子主题：Gossip Protocol

## 中文导读

本题要求你完成 `Tune Gossip Parameters用于Maelstrom 广播`。

重点关注：`parameter tuning`、`messages-per-op`、`latency tradeoff`、`gossip optimization`。

建议先按提示逐步实现：消息-per-op = total 消息 sent / total 广播 operations。

协议字段、消息类型、输入输出格式请以本文件中的代码块和测试用例为准。

## 题目说明

The Maelstrom 广播 workload requires 消息-per-op < 30 under 网络 partitions. Your task is to implement configurable gossip parameters和track 消息 efficiency.

Implement a `configure` handler to set gossip parameters:
```JSON
请求:  {"type": "configure", "msg_id": 1, "fanout": 3, "gossip_interval_ms": 200}
响应: {"type": "configure_ok", "in_reply_to": 1}
```

And a `gossip_stats` handler to report efficiency:
```JSON
请求:  {"type": "gossip_stats", "msg_id": 2}
响应: {"type": "gossip_stats_ok", "in_reply_to": 2, 
           "broadcasts_received": 10, "gossip_messages_sent": 45,
           "messages_per_op": 4.5, "unique_messages": 10}
```

## 涉及概念

- `parameter tuning`
- `messages-per-op`
- `latency tradeoff`
- `gossip optimization`

## 实现提示

- 消息-per-op = total 消息 sent / total 广播 operations
- Lower fanout = fewer 消息 but slower convergence
- Higher gossip interval = fewer rounds but more latency
- The sweet spot balances 消息 overhead vs delivery reliability
- Track both metrics和expose them via a stats endpoint

## 测试用例

### 1. Configure updates fanout

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

### 2. Stats，包含zero broadcasts

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

- [Fly.io Gossip Glomers - Broadcast](https://fly.io/dist-sys/3a/)：Fly.io 分布式系统 challenge用于广播 workloads

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
