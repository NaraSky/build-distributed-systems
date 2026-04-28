# 从零实现 Lamport 时钟

网页：<https://builddistributedsystem.com/tracks/timekeeper/tasks/task-4-2-1-lamport-basic>

课程：16. 时间守卫：逻辑时钟
任务序号：6
短标题：Lamport 基础
难度：进阶
子主题：Lamport 时钟

## 中文导读

在分布式系统中，不同机器上的物理时钟永远无法做到完全一致。但我们仍然需要判断"事件 A 和事件 B 谁先发生"。Lamport 时钟（Lamport Clock）用一个简单到令人惊讶的方法解决了这个问题：每个节点维护一个整数计数器，发消息时加一并附上，收消息时取较大值再加一。

这道题让你从零开始实现这个经典算法，亲身体会逻辑时钟如何在没有物理时钟同步的情况下捕捉事件之间的因果关系。

## 题目说明

Lamport 时钟是最简单的逻辑时钟。每个节点（Node）维护一个整数计数器，随着每个事件的发生而递增。规则只有三条：

1. **内部事件**：计数器加 1
2. **发送消息**：计数器加 1，然后将当前计数器值附加到消息中
3. **接收消息**：取本地计数器和消息中计数器的较大值，再加 1

你需要实现一个支持以下四种消息的 Lamport 时钟节点：

`tick` 模拟一次内部事件，递增计数器：

```json
Request:  {"type": "tick", "msg_id": 1}
Response: {"type": "tick_ok", "in_reply_to": 1, "clock": 1}
```

`send_msg` 模拟向另一个节点发送消息：

```json
Request:  {"type": "send_msg", "msg_id": 2, "dest": "n2", "payload": "hello"}
Response: {"type": "send_msg_ok", "in_reply_to": 2, "clock": 2}
```

`recv_msg` 模拟从另一个节点接收消息，其中 `remote_clock` 是对方的时钟值：

```json
Request:  {"type": "recv_msg", "msg_id": 3, "from": "n2", "remote_clock": 5, "payload": "hi"}
Response: {"type": "recv_msg_ok", "in_reply_to": 3, "clock": 6}
```

`get_clock` 查询当前时钟值：

```json
Request:  {"type": "get_clock", "msg_id": 4}
Response: {"type": "get_clock_ok", "in_reply_to": 4, "clock": 6}
```

## 涉及概念

- `Lamport clock`
- `logical time`
- `happened-before`
- `causal ordering`

## 实现提示

- Lamport 时钟就是每个节点维护的一个整数，从 0 开始
- 规则一：发送消息前先递增计数器
- 规则二：接收消息时，计数器 = max(本地值, 消息中的值) + 1
- 规则三：发生内部事件时递增计数器
- 可以用 3 个节点以环形模式互发消息来测试各种场景

## 测试用例

### 1. 内部事件递增时钟

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1","n2","n3"]}}
{"src":"c1","dest":"n1","body":{"type":"tick","msg_id":2}}
{"src":"c1","dest":"n1","body":{"type":"tick","msg_id":3}}
{"src":"c1","dest":"n1","body":{"type":"get_clock","msg_id":4}}
```

期望输出：

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
{"src": "n1", "dest": "c1", "body": {"type": "tick_ok", "in_reply_to": 2, "clock": 1, "msg_id": 1}}
{"src": "n1", "dest": "c1", "body": {"type": "tick_ok", "in_reply_to": 3, "clock": 2, "msg_id": 2}}
{"src": "n1", "dest": "c1", "body": {"type": "get_clock_ok", "in_reply_to": 4, "clock": 2, "msg_id": 3}}
```

### 2. 接收消息后时钟更新为较大值加 1

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1","n2"]}}
{"src":"c1","dest":"n1","body":{"type":"tick","msg_id":2}}
{"src":"n2","dest":"n1","body":{"type":"recv_msg","msg_id":3,"from":"n2","remote_clock":10,"payload":"hi"}}
{"src":"c1","dest":"n1","body":{"type":"get_clock","msg_id":4}}
```

期望输出：

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
{"src": "n1", "dest": "c1", "body": {"type": "tick_ok", "in_reply_to": 2, "clock": 1, "msg_id": 1}}
{"src": "n1", "dest": "n2", "body": {"type": "recv_msg_ok", "in_reply_to": 3, "clock": 11, "msg_id": 2}}
{"src": "n1", "dest": "c1", "body": {"type": "get_clock_ok", "in_reply_to": 4, "clock": 11, "msg_id": 3}}
```

## 参考资料

- [Time, Clocks, and the Ordering of Events - Lamport 1978](https://lamport.azurewebsites.net/pubs/time-clocks.pdf)：Leslie Lamport 关于逻辑时钟的原始论文，分布式系统领域最重要的奠基性文献之一

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
