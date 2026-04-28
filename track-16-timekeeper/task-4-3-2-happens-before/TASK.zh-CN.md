# 实现 Happens-Before和Concurrency Detection

英文标题：Implement Happens-Before和Concurrency Detection
网页：<https://builddistributedsystem.com/tracks/timekeeper/tasks/task-4-3-2-happens-before>

课程：16. 时间守卫：逻辑时钟
任务序号：12
短标题：Happens-Before
难度：intermediate
子主题：向量 Clocks

## 中文导读

本题要求你完成 `实现 Happens-Before和Concurrency Detection`。

重点关注：`happens-before`、`concurrency detection`、`partial order`、`causality`。

建议先按提示逐步实现：A happens-before B if every element of A <= B和at least one is strictly less。

协议字段、消息类型、输入输出格式请以本文件中的代码块和测试用例为准。

## 题目说明

Vector clocks let you determine the causal relationship between any two events. Given two vector 时钟 stamps `a`和`b`:

- **a happens-before b** (`a -> b`): every element of `a <= b` AND at least one element of `a < b`
- **b happens-before a** (`b -> a`): every element of `b <= a` AND at least one element of `b < a`
- **concurrent** (`a || b`): neither happens-before the other (some elements of a are greater, some of b are greater)

Implement a `compare` handler:

```JSON
请求:  {"type": "compare", "msg_id": 1, "clock_a": [2, 3, 1], "clock_b": [2, 4, 2]}
响应: {"type": "compare_ok", "in_reply_to": 1, "result": "A_BEFORE_B"}

请求:  {"type": "compare", "msg_id": 2, "clock_a": [3, 1, 0], "clock_b": [1, 3, 0]}
响应: {"type": "compare_ok", "in_reply_to": 2, "result": "CONCURRENT"}

请求:  {"type": "compare", "msg_id": 3, "clock_a": [5, 3, 2], "clock_b": [2, 1, 1]}
响应: {"type": "compare_ok", "in_reply_to": 3, "result": "B_BEFORE_A"}
```

## 涉及概念

- `happens-before`
- `concurrency detection`
- `partial order`
- `causality`

## 实现提示

- A happens-before B if every element of A <= B和at least one is strictly less
- Two events are concurrent if neither happens-before the other
- Implement comparisons as element-wise vector comparison
- Equal vectors mean the same event (not concurrent)
- This is a partial order, not a total order

## 测试用例

### 1. A happens-before B

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

### 2.并发events detected

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

- [Detecting Causal Relationships使用Vector Clocks](https://en.wikipedia.org/wiki/Vector_clock)：Wikipedia overview of vector clocks和the happens-before relation

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
