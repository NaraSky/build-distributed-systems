# 实现 Lamport 逻辑时钟

网页：<https://builddistributedsystem.com/tracks/identifier/tasks/task-2-3-1-lamport-clock>

课程：2. 标识符：分布式唯一 ID
任务序号：11
短标题：Lamport 时钟
难度：进阶
子主题：用逻辑时钟做标识

## 中文导读

在分布式系统中，不同机器的物理时钟很难完全同步。Leslie Lamport 提出了一个优雅的解决方案：不靠物理时钟，仅用一个简单的整数计数器就能给事件排出先后顺序。

这道题让你亲手实现 Lamport 时钟（Lamport Clock）。它的规则很简单——发消息时加一，收消息时取较大值再加一。虽然简单，但它是理解分布式系统中"时间"这一概念的基石。

## 题目说明

Leslie Lamport 证明了，在分布式系统中不需要物理时钟也可以对事件排序。Lamport 时钟本质上是一个整数计数器，它提供了一种偏序关系（Partial Order）：如果事件 A 确实因果地先于事件 B 发生，那么 A 的时钟值一定小于 B 的时钟值。

三条核心规则：
1. 每次**发送**消息前，先把计数器加 1，然后把计数器的值附在消息上
2. 每次**接收**消息时，取本地计数器和消息中计数器的较大值，再加 1
3. 每次发生**本地事件**时，把计数器加 1

你需要在 Maelstrom 节点中实现这个 Lamport 时钟：

`tick` 处理器模拟一次本地事件，递增计数器并返回当前值：

```json
Request:  {"type": "tick", "msg_id": 1}
Response: {"type": "tick_ok", "in_reply_to": 1, "clock": 1}
```

`send_stamped` 处理器将带有当前 Lamport 时间戳的消息发送给另一个节点：

```json
Request:  {"type": "send_stamped", "msg_id": 1, "target": "n2", "data": "hello"}
Response: {"type": "send_stamped_ok", "in_reply_to": 1, "clock": 2}
```

`get_clock` 处理器返回当前的时钟值：

```json
Response: {"type": "get_clock_ok", "in_reply_to": 1, "clock": 5}
```

## 涉及概念

- `Lamport clock`
- `logical time`
- `partial order`
- `happens-before`

## 实现提示

- Lamport 时钟就是每个节点维护的一个整数，初始值为 0
- 每次本地事件或发送消息时：计数器加 1
- 每次接收消息时：计数器 = max(本地值, 收到的值) + 1
- Lamport 时钟只能提供偏序，不能提供全序。也就是说，如果 L(A) < L(B)，并**不**意味着 A 一定发生在 B 之前；但如果 A 确实发生在 B 之前，那么 L(A) 一定小于 L(B)

## 测试用例

### 1. tick 操作递增时钟

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"tick","msg_id":2}}
```

期望输出：

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
{"src": "n1", "dest": "c1", "body": {"type": "tick_ok", "clock": 1, "in_reply_to": 2, "msg_id": 1}}
```

### 2. 多次 tick 依次递增

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"tick","msg_id":2}}
{"src":"c1","dest":"n1","body":{"type":"tick","msg_id":3}}
{"src":"c1","dest":"n1","body":{"type":"tick","msg_id":4}}
```

期望输出：

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
{"src": "n1", "dest": "c1", "body": {"type": "tick_ok", "clock": 1, "in_reply_to": 2, "msg_id": 1}}
{"src": "n1", "dest": "c1", "body": {"type": "tick_ok", "clock": 2, "in_reply_to": 3, "msg_id": 2}}
{"src": "n1", "dest": "c1", "body": {"type": "tick_ok", "clock": 3, "in_reply_to": 4, "msg_id": 3}}
```

## 参考资料

- [Time, Clocks, and the Ordering of Events (Lamport 1978)](https://lamport.azurewebsites.net/pubs/time-clocks.pdf)：Leslie Lamport 关于逻辑时钟的原始论文，分布式系统领域的经典之作

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
