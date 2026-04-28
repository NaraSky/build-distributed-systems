# 实现 a G-计数器 (Grow-Only CRDT)

英文标题：Implement a G-Counter (Grow-Only CRDT)
网页：<https://builddistributedsystem.com/tracks/counter/tasks/task-17-2-1-g-counter>

课程：4. 计数器：分布式状态与 CRDT
任务序号：6
短标题：G-计数器
难度：intermediate
子主题：G-计数器和PN-计数器

## 中文导读

本题要求你完成 `实现 a G-计数器 (Grow-Only CRDT)`。

重点关注：`G-Counter`、`CRDT`、`vector of counters`、`element-wise max`、`convergence`。

建议先按提示逐步实现：Each 节点 maintains a vector of N integers (one slot per 节点)。

协议字段、消息类型、输入输出格式请以本文件中的代码块和测试用例为准。

## 题目说明

A G-计数器 (Grow-only 计数器) is the simplest CRDT. Each 节点 maintains a vector of N integers, one per 节点. A 节点 only increments its own slot,和the total value is the sum of all slots.

**Data structure**: vector of N integers, where N = number of 节点.

**Operations**:
- `increment()`: `counters[my_node_id] += 1`
- `value()`: `sum(counters)`
- `merge(other)`: `counters[i] = max(counters[i], other.counters[i])`用于all i

**Why it works**: each 节点 independently increments its own slot. The merge function (element-wise max) is commutative, associative,和idempotent — making it a valid CRDT that always converges regardless of 消息 ordering or duplication.

```JSON
请求:  {"type": "increment", "msg_id": 1}
响应: {"type": "increment_ok", "in_reply_to": 1, "local_value": 1}

请求:  {"type": "read", "msg_id": 2}
响应: {"type": "read_ok", "in_reply_to": 2, "value": 5}
```

## 涉及概念

- `G-Counter`
- `CRDT`
- `vector of counters`
- `element-wise max`
- `convergence`

## 实现提示

- Each 节点 maintains a vector of N integers (one slot per 节点)
- 节点 I only increments its own slot: counters[I] += 1
- Value = sum of all slots across the vector
- Merge = element-wise max of two vectors
- This guarantees convergence: merge is commutative, associative,和idempotent

## 测试用例

### 1. Increment increases local 计数器

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1","n2","n3"]}}
{"src":"c1","dest":"n1","body":{"type":"increment","msg_id":2}}
{"src":"c1","dest":"n1","body":{"type":"read","msg_id":3}}
```

期望输出：

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
{"src": "n1", "dest": "c1", "body": {"type": "increment_ok", "in_reply_to": 2, "msg_id": 1}}
{"src": "n1", "dest": "c1", "body": {"type": "read_ok", "in_reply_to": 3, "value": 1, "msg_id": 2}}
```

### 2. Multiple increments accumulate

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"increment","msg_id":2}}
{"src":"c1","dest":"n1","body":{"type":"increment","msg_id":3}}
{"src":"c1","dest":"n1","body":{"type":"increment","msg_id":4}}
{"src":"c1","dest":"n1","body":{"type":"read","msg_id":5}}
```

期望输出：

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
{"src": "n1", "dest": "c1", "body": {"type": "increment_ok", "in_reply_to": 2, "msg_id": 1}}
{"src": "n1", "dest": "c1", "body": {"type": "increment_ok", "in_reply_to": 3, "msg_id": 2}}
{"src": "n1", "dest": "c1", "body": {"type": "increment_ok", "in_reply_to": 4, "msg_id": 3}}
{"src": "n1", "dest": "c1", "body": {"type": "read_ok", "in_reply_to": 5, "value": 3, "msg_id": 4}}
```

## 参考资料

- [CRDTs: G-Counter](https://crdt.tech/glossary)：CRDT glossary，包含G-计数器 definition和properties

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
