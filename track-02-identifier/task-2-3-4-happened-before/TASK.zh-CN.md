# 实现 Happened-Before Detector，包含向量 Clocks

英文标题：Implement Happened-Before Detector，包含Vector Clocks
网页：<https://builddistributedsystem.com/tracks/identifier/tasks/task-2-3-4-happened-before>

课程：2. 标识符：分布式唯一 ID
任务序号：14
短标题：Happened-Before
难度：advanced
子主题：Logical Clocks as IDs

## 中文导读

本题要求你完成 `实现 Happened-Before Detector，包含向量 Clocks`。

重点关注：`happened-before`、`concurrent events`、`vector comparison`、`conflict detection`。

建议先按提示逐步实现：A -> B if A[i] <= B[i]用于all i,和A[j] < B[j]用于at least one j。

协议字段、消息类型、输入输出格式请以本文件中的代码块和测试用例为准。

## 题目说明

With vector clocks, you can determine the **exact causal relationship** between any two events:

- **A -> B** (A happened before B): A[i] <= B[i]用于all i,和strict <用于at least one
- **B -> A** (B happened before A): B[i] <= A[i]用于all i,和strict <用于at least one
- **A || B** (concurrent): neither dominates

Implement a `compare` handler:
```JSON
请求:  {"type": "compare", "msg_id": 1, 
           "vc_a": {"n1": 2, "n2": 1}, 
           "vc_b": {"n1": 1, "n2": 3}}
响应: {"type": "compare_ok", "in_reply_to": 1, "relation": "concurrent"}
```

Possible relations: `"a_before_b"`, `"b_before_a"`, `"concurrent"`, `"equal"`.

## 涉及概念

- `happened-before`
- `concurrent events`
- `vector comparison`
- `conflict detection`

## 实现提示

- A -> B if A[i] <= B[i]用于all i,和A[j] < B[j]用于at least one j
- A || B (concurrent) if neither A -> B nor B -> A
- Compare vectors element-wise across all 节点
- Store events，包含their vector 时钟 snapshots用于later comparison
- This is the foundation用于conflict detection in databases like Riak

## 测试用例

### 1. A before B

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"compare","msg_id":2,"vc_a":{"n1":1,"n2":0},"vc_b":{"n1":2,"n2":1}}}
```

期望输出：

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
{"src": "n1", "dest": "c1", "body": {"type": "compare_ok", "relation": "a_before_b", "in_reply_to": 2, "msg_id": 1}}
```

### 2.并发events

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"compare","msg_id":2,"vc_a":{"n1":2,"n2":1},"vc_b":{"n1":1,"n2":3}}}
```

期望输出：

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
{"src": "n1", "dest": "c1", "body": {"type": "compare_ok", "relation": "concurrent", "in_reply_to": 2, "msg_id": 1}}
```

## 参考资料

- [Why Vector Clocks Are Hard](https://riak.com/posts/technical/why-vector-clocks-are-hard/)：Basho on practical challenges，包含vector clocks in Riak

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
