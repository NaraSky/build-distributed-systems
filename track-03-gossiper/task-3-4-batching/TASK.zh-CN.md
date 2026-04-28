# 添加 消息 Batching to Reduce Network Overhead

英文标题：Add Message Batching to Reduce Network Overhead
网页：<https://builddistributedsystem.com/tracks/gossiper/tasks/task-3-4-batching>

课程：3. 传播者：Gossip 信息传播
任务序号：4
短标题：消息 Batching
难度：intermediate
子主题：Naive 广播 (Flooding)

## 中文导读

本题要求你完成 `添加 消息 Batching to Reduce Network Overhead`。

重点关注：`batching`、`throughput optimization`、`latency tradeoff`。

建议先按提示逐步实现：Buffer 消息 before sending。

协议字段、消息类型、输入输出格式请以本文件中的代码块和测试用例为准。

## 题目说明

Reduce 网络 overhead by batching multiple 消息 into single transmissions. Instead of sending immediately, buffer 消息和flush periodically or when the buffer reaches a threshold.

## 概念说明

### Batching Trade-offs

Batching improves throughput by reducing per-消息 overhead but increases latency. The optimal batch size depends on 消息 rate, 网络 latency,和consistency requirements.

## 涉及概念

- `batching`
- `throughput optimization`
- `latency tradeoff`

## 实现提示

- Buffer 消息 before sending
- Use a time-based flush
- Balance latency vs throughput

## 测试用例

### 1. Messages are batched together

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c0","dest":"n1","body":{"type":"topology","msg_id":2,"topology":{"n1":[]}}}
{"src":"c1","dest":"n1","body":{"type":"broadcast","msg_id":3,"message":1}}
{"src":"c2","dest":"n1","body":{"type":"broadcast","msg_id":4,"message":2}}
{"src":"c3","dest":"n1","body":{"type":"broadcast","msg_id":5,"message":3}}
{"src":"c4","dest":"n1","body":{"type":"read","msg_id":6}}
```

期望输出：

```text
{"src":"n1","dest":"c0","body":{"type":"init_ok","in_reply_to":1,"msg_id":0}}
{"src":"n1","dest":"c0","body":{"type":"topology_ok","in_reply_to":2,"msg_id":1}}
{"src":"n1","dest":"c1","body":{"type":"broadcast_ok","in_reply_to":3,"msg_id":2}}
{"src":"n1","dest":"c2","body":{"type":"broadcast_ok","in_reply_to":4,"msg_id":3}}
{"src":"n1","dest":"c3","body":{"type":"broadcast_ok","in_reply_to":5,"msg_id":4}}
{"src":"n1","dest":"c4","body":{"type":"read_ok","in_reply_to":6,"msg_id":5,"messages":[1,2,3]}}
```

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
