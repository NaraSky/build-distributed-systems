# 实现 CRDTs

英文标题：Implement CRDTs
网页：<https://builddistributedsystem.com/tracks/advanced/tasks/task-10-5-crdt>

课程：10. 高级主题
任务序号：5
短标题：CRDTs
难度：advanced
子主题：高级 Paradigms

## 中文导读

本题要求你完成 `实现 CRDTs`。

重点关注：`CRDT`、`eventual consistency`、`conflict-free`。

建议先按提示逐步实现：Merge must be commutative, associative, idempotent。

协议字段、消息类型、输入输出格式请以本文件中的代码块和测试用例为准。

## 题目说明

Build CRDTs用于conflict-free 复制: G-计数器 (grow-only 计数器), G-Set, OR-Set.

## 概念说明

### CRDTs

Conflict-free Replicated Data Types allow concurrent updates that merge without conflicts. Merge is associative, commutative, idempotent.

## 涉及概念

- `CRDT`
- `eventual consistency`
- `conflict-free`

## 实现提示

- Merge must be commutative, associative, idempotent
- G-计数器: only increment
- OR-Set: add wins over remove

## 测试用例

### 1. G-计数器 increment和merge

Multi-节点 test: n1 increments (count n1->1), n2 increments (count n2->1). When 节点 sync, they merge their counters. Query n1用于total value, should return 2 (sum of all 节点 counts).

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1","n2"]}}
{"src":"c1","dest":"n1","body":{"type":"gcounter_increment","msg_id":2}}
{"src":"c2","dest":"n2","body":{"type":"gcounter_increment","msg_id":3}}
{"src":"c3","dest":"n1","body":{"type":"gcounter_value","msg_id":4}}
```

## 参考资料

- [CRDTs Paper](https://hal.inria.fr/inria-00555588)：Comprehensive study of CRDTs

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
