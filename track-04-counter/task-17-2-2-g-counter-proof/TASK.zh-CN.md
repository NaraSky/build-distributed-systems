# Prove G-计数器 CRDT Properties

英文标题：Prove G-Counter CRDT Properties
网页：<https://builddistributedsystem.com/tracks/counter/tasks/task-17-2-2-g-counter-proof>

课程：4. 计数器：分布式状态与 CRDT
任务序号：7
短标题：CRDT Proof
难度：intermediate
子主题：G-计数器和PN-计数器

## 中文导读

本题要求你完成 `Prove G-计数器 CRDT Properties`。

重点关注：`commutativity`、`associativity`、`idempotency`、`lattice`、`convergence proof`。

建议先按提示逐步实现：Commutative: merge(A, B) == merge(B, A)用于all states A, B。

协议字段、消息类型、输入输出格式请以本文件中的代码块和测试用例为准。

## 题目说明

A CRDT merge function must satisfy three properties to guarantee convergence: commutativity, associativity,和idempotency. Proving these用于the G-计数器 validates it as a correct CRDT.

**Commutativity**: `merge(A, B) == merge(B, A)`
- max(A[i], B[i]) == max(B[i], A[i])用于all i. This is true because max is commutative.

**Associativity**: `merge(A, merge(B, C)) == merge(merge(A, B), C)`
- max(A[i], max(B[i], C[i])) == max(max(A[i], B[i]), C[i]). True because max is associative.

**Idempotency**: `merge(A, A) == A`
- max(A[i], A[i]) == A[i]. True because max(x, x) == x.

These properties form a **join semi-lattice**: the set of all possible states，包含merge as the join operation. The system monotonically advances through this lattice, guaranteeing convergence.

```JSON
请求:  {"type": "crdt_verify", "msg_id": 1, "state_a": {"n1": 3, "n2": 1}, "state_b": {"n1": 1, "n2": 5}}
响应: {"type": "crdt_verify_ok", "in_reply_to": 1, "merge_ab": {"n1": 3, "n2": 5}, "merge_ba": {"n1": 3, "n2": 5}, "commutative": true, "idempotent": true}
```

## 涉及概念

- `commutativity`
- `associativity`
- `idempotency`
- `lattice`
- `convergence proof`

## 实现提示

- Commutative: merge(A, B) == merge(B, A)用于all states A, B
- Associative: merge(A, merge(B, C)) == merge(merge(A, B), C)
- Idempotent: merge(A, A) == A
- These three properties ensure convergence regardless of 消息 order or duplication
- The element-wise max operation satisfies all three properties

## 测试用例

### 1. Merge is commutative

merge_ab should equal merge_ba和commutative should be true.

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"crdt_verify","msg_id":2,"state_a":{"n1":3,"n2":1},"state_b":{"n1":1,"n2":5}}}
```

期望输出：

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

### 2. Merge is idempotent

merge(A,A) should equal A和idempotent should be true.

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"crdt_verify","msg_id":2,"state_a":{"n1":5,"n2":3},"state_b":{"n1":5,"n2":3}}}
```

期望输出：

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

## 参考资料

- [CRDT Convergence](https://hal.inria.fr/inria-00609399/document)：Shapiro et al. - A comprehensive study of CRDTs

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
