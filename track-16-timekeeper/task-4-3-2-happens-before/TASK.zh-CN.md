# 实现先发生关系与并发检测

英文标题：Implement Happens-Before and Concurrency Detection
网页：<https://builddistributedsystem.com/tracks/timekeeper/tasks/task-4-3-2-happens-before>

课程：16. 时间守卫：逻辑时钟
任务序号：12
短标题：先发生关系
难度：进阶
子主题：向量时钟

## 中文导读

本题要求你利用向量时钟来判断两个事件之间的因果关系：谁先发生、谁后发生，还是两者并发。这是分布式系统中理解"偏序关系（Partial Order）"的关键能力，也是后续冲突检测和因果一致性的基础。

## 题目说明

向量时钟可以用来判断任意两个事件之间的因果关系。给定两个向量时钟戳 `a` 和 `b`：

- **a 先于 b 发生**（`a -> b`）：a 的每个分量都小于等于 b 的对应分量，且至少有一个分量严格小于
- **b 先于 a 发生**（`b -> a`）：b 的每个分量都小于等于 a 的对应分量，且至少有一个分量严格小于
- **并发**（`a || b`）：两者互不先发生于对方。也就是说，a 的某些分量比 b 大，而 b 的某些分量比 a 大

请实现一个 `compare` 处理器：

```json
Request:  {"type": "compare", "msg_id": 1, "clock_a": [2, 3, 1], "clock_b": [2, 4, 2]}
Response: {"type": "compare_ok", "in_reply_to": 1, "result": "A_BEFORE_B"}

Request:  {"type": "compare", "msg_id": 2, "clock_a": [3, 1, 0], "clock_b": [1, 3, 0]}
Response: {"type": "compare_ok", "in_reply_to": 2, "result": "CONCURRENT"}

Request:  {"type": "compare", "msg_id": 3, "clock_a": [5, 3, 2], "clock_b": [2, 1, 1]}
Response: {"type": "compare_ok", "in_reply_to": 3, "result": "B_BEFORE_A"}
```

## 涉及概念

- `happens-before`
- `concurrency detection`
- `partial order`
- `causality`

## 实现提示

- 如果 A 的每个分量都小于等于 B 的对应分量，且至少有一个严格小于，则 A 先于 B 发生
- 如果两者互不先于对方发生，则它们是并发的
- 通过逐位比较向量来实现判断
- 向量完全相等意味着是同一个事件，不算并发
- 这是偏序关系，不是全序关系

## 测试用例

### 1. A 先于 B 发生

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"compare","msg_id":2,"clock_a":[2,3,1],"clock_b":[2,4,2]}}
```

期望输出：

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
{"src": "n1", "dest": "c1", "body": {"type": "compare_ok", "in_reply_to": 2, "result": "A_BEFORE_B", "msg_id": 1}}
```

### 2. 检测到并发事件

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"compare","msg_id":2,"clock_a":[3,1,0],"clock_b":[1,3,0]}}
```

期望输出：

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
{"src": "n1", "dest": "c1", "body": {"type": "compare_ok", "in_reply_to": 2, "result": "CONCURRENT", "msg_id": 1}}
```

## 参考资料

- [Detecting Causal Relationships Using Vector Clocks](https://en.wikipedia.org/wiki/Vector_clock)：维基百科上关于向量时钟和先发生关系的概述

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
