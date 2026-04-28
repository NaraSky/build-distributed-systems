# 实现无冲突复制数据类型

英文标题：Implement CRDTs
网页：<https://builddistributedsystem.com/tracks/advanced/tasks/task-10-5-crdt>

课程：10. 高级主题
任务序号：5
短标题：CRDTs
难度：高级
子主题：高级范式

## 中文导读

本题要求你实现无冲突复制数据类型（CRDT），包括只增计数器（G-Counter）、只增集合（G-Set）和可观察删除集合（OR-Set）。CRDT 的核心特点是：多个副本可以独立并发更新，合并时保证不会产生冲突。这是实现最终一致性系统的利器，常用于协同编辑、分布式缓存等场景。

## 题目说明

实现用于无冲突复制的 CRDT 数据结构：只增计数器（G-Counter，只能递增的计数器）、只增集合（G-Set）和可观察删除集合（OR-Set，添加操作优先于删除操作）。

## 概念说明

### 无冲突复制数据类型

无冲突复制数据类型（CRDT）允许多个副本并发更新，合并时不会产生冲突。合并操作满足三个数学性质：结合律（Associative）、交换律（Commutative）和幂等性（Idempotent）。简单来说，无论数据以什么顺序、合并多少次，最终结果都是一样的。

## 涉及概念

- `CRDT`
- `eventual consistency`
- `conflict-free`

## 实现提示

- 合并操作必须满足交换律、结合律和幂等性
- 只增计数器：只能递增，不能递减
- 可观察删除集合：添加操作优先于删除操作

## 测试用例

### 1. 只增计数器的递增与合并

多节点测试：n1 递增一次（计数器 n1 变为 1），n2 递增一次（计数器 n2 变为 1）。当节点同步时，它们合并各自的计数器。查询 n1 的总值，应返回 2（所有节点计数之和）。

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1","n2"]}}
{"src":"c1","dest":"n1","body":{"type":"gcounter_increment","msg_id":2}}
{"src":"c2","dest":"n2","body":{"type":"gcounter_increment","msg_id":3}}
{"src":"c3","dest":"n1","body":{"type":"gcounter_value","msg_id":4}}
```

## 参考资料

- [CRDTs Paper](https://hal.inria.fr/inria-00555588)：CRDT 的综合研究论文

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
