# 构建只增计数器 CRDT

网页：<https://builddistributedsystem.com/tracks/counter/tasks/task-4-4-g-counter>

课程：4. 计数器：分布式状态与 CRDT
任务序号：4
短标题：G-Counter CRDT
难度：进阶
子主题：丢失更新问题

## 中文导读

这道题让你实现一个 G-Counter（只增计数器）CRDT。核心思路是每个节点只维护自己的计数，总值是所有节点计数的总和，合并时对每个节点取最大值。这种设计从根本上避免了并发冲突，是理解 CRDT 的最佳入门案例。

## 题目说明

实现一个 G-Counter CRDT，其中每个节点维护自己独立的计数器。总值等于所有节点计数器的总和。合并操作是对每个节点的计数器取最大值。

## 概念说明

### 无冲突复制数据类型

CRDT（Conflict-free Replicated Data Type，无冲突复制数据类型）是专门为分布式系统设计的数据结构。它保证了收敛性：所有看到过相同更新的副本，最终一定会达到相同的状态，而且不管更新的到达顺序如何。就像投票计数一样，无论你先统计哪个投票箱，最终的总票数都是一样的。

### G-Counter

G-Counter 维护一个计数向量，每个节点对应一个槽位。递增操作只修改自己对应的槽位，总值是所有槽位之和。合并操作是对每个槽位取最大值。例如，节点 A 的向量是 [3, 1]，节点 B 的向量是 [2, 4]，合并后得到 [3, 4]，总值为 7。

## 涉及概念

- `CRDT`
- `G-Counter`
- `convergence`

## 实现提示

- 每个节点维护自己独立的计数器
- 合并时对每个节点的计数器取最大值
- 读取时将所有计数器求和得到总值

## 测试用例

### 1. G-Counter 基础测试

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

- [CRDTs Paper](https://hal.inria.fr/inria-00555588/document)：Shapiro 等人关于 CRDT 的综合论文

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
