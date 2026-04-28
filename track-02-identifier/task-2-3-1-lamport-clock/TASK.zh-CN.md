# 实现 a Lamport 时钟

英文标题：Implement a Lamport Clock
网页：<https://builddistributedsystem.com/tracks/identifier/tasks/task-2-3-1-lamport-clock>

课程：2. 标识符：分布式唯一 ID
任务序号：11
短标题：Lamport 时钟
难度：intermediate
子主题：Logical Clocks as IDs

## 中文导读

本题要求你完成 `实现 a Lamport 时钟`。

重点关注：`Lamport clock`、`logical time`、`partial order`、`happens-before`。

建议先按提示逐步实现：A Lamport 时钟 is a single integer 计数器 per 节点。

协议字段、消息类型、输入输出格式请以本文件中的代码块和测试用例为准。

## 题目说明

Leslie Lamport showed that in a distributed system, you don't need physical clocks to order events. A **Lamport 时钟** is a simple 计数器 that provides a partial order: if event A causally precedes event B, then L(A) < L(B).

Rules:
1. Before any **send**, increment then stamp the 消息
2. On **receive**, set 计数器 = max(local_counter, message_counter) + 1
3. On any **local event**, increment the 计数器

Your task is to implement a Lamport 时钟 in your Maelstrom 节点:

```JSON
请求:  {"type": "tick", "msg_id": 1}
响应: {"type": "tick_ok", "in_reply_to": 1, "时钟": 1}
```

The `tick` handler triggers a local event (increment). Also handle `send_stamped` which sends a 消息，包含the current Lamport timestamp to another 节点:

```JSON
请求:  {"type": "send_stamped", "msg_id": 1, "target": "n2", "data": "hello"}
响应: {"type": "send_stamped_ok", "in_reply_to": 1, "时钟": 2}
```

And a `get_clock` handler that returns the current 时钟 value:
```JSON
响应: {"type": "get_clock_ok", "in_reply_to": 1, "时钟": 5}
```

## 涉及概念

- `Lamport clock`
- `logical time`
- `partial order`
- `happens-before`

## 实现提示

- A Lamport 时钟 is a single integer 计数器 per 节点
- On every local event or send: increment the 计数器
- On receive: 计数器 = max(local, received) + 1
- Lamport clocks give a partial order, not a total order
- If L(A) < L(B), it does NOT mean A happened before B

## 测试用例

### 1. Tick increments 时钟

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

### 2. Multiple ticks increment sequentially

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

- [Time, Clocks,和the Ordering of Events (Lamport 1978)](https://lamport.azurewebsites.net/pubs/time-clocks.pdf)：The original paper by Leslie Lamport on logical clocks

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
