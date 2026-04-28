# 实现 a PN-计数器用于Increment和Decrement

英文标题：Implement a PN-Counter用于Increment和Decrement
网页：<https://builddistributedsystem.com/tracks/counter/tasks/task-17-2-3-pn-counter>

课程：4. 计数器：分布式状态与 CRDT
任务序号：8
短标题：PN-计数器
难度：intermediate
子主题：G-计数器和PN-计数器

## 中文导读

本题要求你完成 `实现 a PN-计数器用于Increment和Decrement`。

重点关注：`PN-Counter`、`increment`、`decrement`、`two G-Counters`、`subtraction`。

建议先按提示逐步实现：A PN-计数器 uses TWO G-Counters: P (positive/increments)和N (negative/decrements)。

协议字段、消息类型、输入输出格式请以本文件中的代码块和测试用例为准。

## 题目说明

A G-计数器 only grows. To support decrements, the PN-计数器 uses two G-Counters: P (positive)用于increments和N (negative)用于decrements.

**Data structure**: two G-计数器 vectors — P和N.

**Operations**:
- `increment()`: `P.counters[my_id] += 1`
- `decrement()`: `N.counters[my_id] += 1`
- `value()`: `P.value() - N.value()` = `sum(P) - sum(N)`
- `merge(other)`: merge P vectors separately, merge N vectors separately

The value can go negative (if more decrements than increments). The CRDT properties hold because each component (P和N) is independently a valid G-计数器.

```JSON
请求:  {"type": "add", "msg_id": 1, "delta": 1}
响应: {"type": "add_ok", "in_reply_to": 1}

请求:  {"type": "add", "msg_id": 2, "delta": -1}
响应: {"type": "add_ok", "in_reply_to": 2}

请求:  {"type": "read", "msg_id": 3}
响应: {"type": "read_ok", "in_reply_to": 3, "value": 0}
```

## 涉及概念

- `PN-Counter`
- `increment`
- `decrement`
- `two G-Counters`
- `subtraction`

## 实现提示

- A PN-计数器 uses TWO G-Counters: P (positive/increments)和N (negative/decrements)
- increment() increments P, decrement() increments N
- value() = P.value() - N.value()
- merge: merge P counters separately, merge N counters separately
- This supports both increment和decrement while maintaining CRDT properties

## 测试用例

### 1. Increment和decrement balance to zero

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"add","msg_id":2,"delta":1}}
{"src":"c1","dest":"n1","body":{"type":"add","msg_id":3,"delta":-1}}
{"src":"c1","dest":"n1","body":{"type":"read","msg_id":4}}
```

期望输出：

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
{"src": "n1", "dest": "c1", "body": {"type": "add_ok", "in_reply_to": 2, "msg_id": 1}}
{"src": "n1", "dest": "c1", "body": {"type": "add_ok", "in_reply_to": 3, "msg_id": 2}}
{"src": "n1", "dest": "c1", "body": {"type": "read_ok", "in_reply_to": 4, "value": 0, "msg_id": 3}}
```

### 2. Value can go negative

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"add","msg_id":2,"delta":-5}}
{"src":"c1","dest":"n1","body":{"type":"read","msg_id":3}}
```

期望输出：

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
{"src": "n1", "dest": "c1", "body": {"type": "add_ok", "in_reply_to": 2, "msg_id": 1}}
{"src": "n1", "dest": "c1", "body": {"type": "read_ok", "in_reply_to": 3, "value": -5, "msg_id": 2}}
```

## 参考资料

- [PN-Counter CRDT](https://en.wikipedia.org/wiki/Conflict-free_replicated_data_type#PN-Counter)：Wikipedia article on PN-计数器 CRDT

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
