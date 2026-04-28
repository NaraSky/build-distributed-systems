# 构建 Grow-Only 计数器 (G-计数器) CRDT

英文标题：Build Grow-Only Counter (G-Counter) CRDT
网页：<https://builddistributedsystem.com/tracks/counter/tasks/task-4-4-g-counter>

课程：4. 计数器：分布式状态与 CRDT
任务序号：4
短标题：G-计数器 CRDT
难度：intermediate
子主题：The Lost Update Problem

## 中文导读

本题要求你完成 `构建 Grow-Only 计数器 (G-计数器) CRDT`。

重点关注：`CRDT`、`G-Counter`、`convergence`。

建议先按提示逐步实现：Each 节点 maintains its own 计数器。

协议字段、消息类型、输入输出格式请以本文件中的代码块和测试用例为准。

## 题目说明

Implement a G-计数器 CRDT where each 节点 maintains its own 计数器. The total is the sum of all per-节点 counters. Merging is done by taking the maximum of each 节点 计数器.

## 概念说明

### CRDTs

Conflict-free Replicated Data Types are data structures designed用于分布式系统. They guarantee convergence: all replicas that have seen the same updates will have the same state, regardless of update order.

### G-计数器

A G-计数器 maintains a vector of counts, one per 节点. To increment, a 节点 increments only its own entry. The total value is the sum of all entries. Merge takes the component-wise maximum.

## 涉及概念

- `CRDT`
- `G-Counter`
- `convergence`

## 实现提示

- Each 节点 maintains its own 计数器
- Merge by taking max of each 节点 计数器
- Sum all counters用于total

## 测试用例

### 1. G-计数器 基础

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1","n2"]}}
{"src":"c1","dest":"n1","body":{"type":"add","msg_id":2,"delta":3}}
{"src":"c2","dest":"n1","body":{"type":"read","msg_id":3}}
```

期望输出：

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
{"src": "n1", "dest": "c1", "body": {"type": "add_ok", "in_reply_to": 2, "msg_id": 1}}
{"src": "n1", "dest": "c2", "body": {"type": "read_ok", "value": 3, "in_reply_to": 3, "msg_id": 2}}
```

## 参考资料

- [CRDTs Paper](https://hal.inria.fr/inria-00555588/document)：Shapiro et al. comprehensive CRDT paper

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
