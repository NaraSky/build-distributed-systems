# 实现支持递增和递减的 PN-Counter

网页：<https://builddistributedsystem.com/tracks/counter/tasks/task-17-2-3-pn-counter>

课程：4. 计数器：分布式状态与 CRDT
任务序号：8
短标题：PN-Counter
难度：进阶
子主题：G-Counter 与 PN-Counter

## 中文导读

G-Counter 只能递增不能递减。这道题让你实现 PN-Counter，它巧妙地用两个 G-Counter 解决了递减问题：一个记录递增（P），一个记录递减（N），最终值等于 P 减 N。这是一种化繁为简的经典设计思路。

## 题目说明

G-Counter 只能增长，不支持递减操作。为了支持递减，PN-Counter 使用了两个 G-Counter：P（正向）用于记录递增，N（负向）用于记录递减。

**数据结构**：两个 G-Counter 向量，分别是 P 和 N。

**操作**：
- `increment()`：`P.counters[my_id] += 1`
- `decrement()`：`N.counters[my_id] += 1`
- `value()`：`P.value() - N.value()` 即 `sum(P) - sum(N)`
- `merge(other)`：分别合并 P 向量和 N 向量

计数器的值可以变成负数（当递减次数多于递增次数时）。由于 P 和 N 各自都是独立的有效 G-Counter，所以 CRDT 的性质依然成立。

```json
Request:  {"type": "add", "msg_id": 1, "delta": 1}
Response: {"type": "add_ok", "in_reply_to": 1}

Request:  {"type": "add", "msg_id": 2, "delta": -1}
Response: {"type": "add_ok", "in_reply_to": 2}

Request:  {"type": "read", "msg_id": 3}
Response: {"type": "read_ok", "in_reply_to": 3, "value": 0}
```

## 涉及概念

- `PN-Counter`
- `increment`
- `decrement`
- `two G-Counters`
- `subtraction`

## 实现提示

- PN-Counter 使用两个 G-Counter：P（正向，记录递增）和 N（负向，记录递减）
- increment() 递增 P，decrement() 递增 N
- value() = P.value() - N.value()
- 合并时分别合并 P 向量和 N 向量
- 这样既支持递增又支持递减，同时保持了 CRDT 的性质

## 测试用例

### 1. 递增和递减相互抵消为零

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

### 2. 值可以变成负数

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

- [PN-Counter CRDT](https://en.wikipedia.org/wiki/Conflict-free_replicated_data_type#PN-Counter)：维基百科上关于 PN-Counter CRDT 的介绍

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
