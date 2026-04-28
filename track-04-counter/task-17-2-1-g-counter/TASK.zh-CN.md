# 实现只增计数器

网页：<https://builddistributedsystem.com/tracks/counter/tasks/task-17-2-1-g-counter>

课程：4. 计数器：分布式状态与 CRDT
任务序号：6
短标题：G-Counter
难度：进阶
子主题：G-Counter 与 PN-Counter

## 中文导读

这道题要求你从零实现一个只增计数器（G-Counter），它是最简单的无冲突复制数据类型。每个节点维护一个整数向量，只递增属于自己的那一格，读取时把所有格加起来就是总值。理解只增计数器是掌握所有无冲突复制数据类型的起点。

## 题目说明

只增计数器（G-Counter，Grow-only Counter）是最简单的无冲突复制数据类型（CRDT，Conflict-free Replicated Data Type）。它的设计思路非常直观：集群中有多少个节点（Node），就维护一个多长的整数向量。每个节点只能修改自己对应的那一格，想要获取计数器的总值时，把向量中所有格的数字加起来即可。

**数据结构**：一个长度为 N 的整数向量，N 等于节点总数。

**支持的操作**：
- `increment()`：把自己那一格加一，即 `counters[my_node_id] += 1`
- `value()`：把所有格的值加起来，即 `sum(counters)`
- `merge(other)`：把两个向量逐格比较，每格取较大值，即 `counters[i] = max(counters[i], other.counters[i])`

**为什么这样设计就能保证正确？** 因为每个节点只修改自己的格，不会和别人冲突。合并函数采用"逐格取最大值"的方式，满足交换律（谁先谁后无所谓）、结合律（多次合并顺序无所谓）和幂等性（重复合并不影响结果）。这三个性质保证了无论消息以什么顺序到达、是否有重复，所有节点最终都会收敛到同一个值。

```json
Request:  {"type": "increment", "msg_id": 1}
Response: {"type": "increment_ok", "in_reply_to": 1, "local_value": 1}

Request:  {"type": "read", "msg_id": 2}
Response: {"type": "read_ok", "in_reply_to": 2, "value": 5}
```

## 涉及概念

- G-Counter
- CRDT
- vector of counters
- element-wise max
- convergence

## 实现提示

- 每个节点维护一个长度为 N 的整数向量，每个节点对应一格
- 节点 I 只递增自己的那一格：`counters[I] += 1`
- 总值等于向量中所有格的数字之和
- 合并时对两个向量逐格取最大值
- 这保证了最终收敛：合并操作满足交换律、结合律和幂等性

## 测试用例

### 1. 递增操作更新本地计数器

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

### 2. 多次递增正确累加

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

- [CRDTs: G-Counter](https://crdt.tech/glossary)：CRDT 术语表，包含只增计数器的定义和性质

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
