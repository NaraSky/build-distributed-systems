# 基于向量时钟实现先发生关系检测器

英文标题：Implement Happened-Before Detector with Vector Clocks
网页：<https://builddistributedsystem.com/tracks/identifier/tasks/task-2-3-4-happened-before>

课程：2. 标识符：分布式唯一 ID
任务序号：14
短标题：先发生关系
难度：高级
子主题：Logical Clocks as IDs

## 中文导读

有了向量时钟，我们就能精确判断任意两个事件之间的因果关系：谁先发生、谁后发生，还是完全并发。本题要求你实现一个比较器，输入两个向量时钟，输出它们之间的关系。这是冲突检测和数据一致性的基础能力。

## 题目说明

借助向量时钟（Vector Clock），你可以精确判断任意两个事件之间的**因果关系**：

- **A -> B**（A 先于 B 发生）：对所有节点 i，A[i] <= B[i]，且至少存在一个节点 j 使得 A[j] < B[j]
- **B -> A**（B 先于 A 发生）：对所有节点 i，B[i] <= A[i]，且至少存在一个节点 j 使得 B[j] < A[j]
- **A || B**（并发）：A 和 B 互不支配，即谁也不能完全"盖过"对方

简单来说，如果 A 的向量每个分量都不超过 B，且至少有一个严格小于 B，说明 A 先发生。如果两个向量互有胜负（A 的某个分量大于 B，B 的另一个分量又大于 A），说明它们是并发的。

实现 `compare` 处理器：
```json
请求:  {"type": "compare", "msg_id": 1, 
           "vc_a": {"n1": 2, "n2": 1}, 
           "vc_b": {"n1": 1, "n2": 3}}
响应: {"type": "compare_ok", "in_reply_to": 1, "relation": "concurrent"}
```

可能的关系值有四种：`"a_before_b"`、`"b_before_a"`、`"concurrent"`、`"equal"`。

## 涉及概念

- `happened-before`
- `concurrent events`
- `vector comparison`
- `conflict detection`

## 实现提示

- 判断 A -> B 的条件：对所有节点 i 有 A[i] <= B[i]，且至少有一个节点 j 满足 A[j] < B[j]
- 判断并发（A || B）的条件：既不满足 A -> B，也不满足 B -> A
- 逐元素比较两个向量中所有节点的计数器
- 将事件与其向量时钟快照一起保存，以便后续比较
- 这是 Riak 等数据库进行冲突检测的理论基础

## 测试用例

### 1. A 先于 B 发生

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

### 2. 并发事件

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

- [Why Vector Clocks Are Hard](https://riak.com/posts/technical/why-vector-clocks-are-hard/)：Basho 团队分享在 Riak 中使用向量时钟的实际挑战

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
