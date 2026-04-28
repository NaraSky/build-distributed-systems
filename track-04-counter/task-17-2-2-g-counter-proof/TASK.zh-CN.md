# 证明 G-Counter 的 CRDT 性质

网页：<https://builddistributedsystem.com/tracks/counter/tasks/task-17-2-2-g-counter-proof>

课程：4. 计数器：分布式状态与 CRDT
任务序号：7
短标题：CRDT 性质证明
难度：进阶
子主题：G-Counter 与 PN-Counter

## 中文导读

这道题要求你验证 G-Counter 的合并函数满足三个关键性质：交换律、结合律和幂等性。只有同时满足这三个性质，才能保证所有副本无论消息到达顺序如何，最终都会收敛到一致的状态。这是理解 CRDT 正确性基础的重要练习。

## 题目说明

一个 CRDT 的合并函数必须满足三个性质才能保证收敛：交换律（Commutativity）、结合律（Associativity）和幂等性（Idempotency）。为 G-Counter 证明这三个性质，就验证了它是一个正确的 CRDT。

**交换律**：`merge(A, B) == merge(B, A)`
- 对所有 i，max(A[i], B[i]) == max(B[i], A[i])。这是成立的，因为取最大值操作本身满足交换律。

**结合律**：`merge(A, merge(B, C)) == merge(merge(A, B), C)`
- max(A[i], max(B[i], C[i])) == max(max(A[i], B[i]), C[i])。成立，因为取最大值满足结合律。

**幂等性**：`merge(A, A) == A`
- max(A[i], A[i]) == A[i]。成立，因为 max(x, x) == x。

这三个性质构成了一个**连接半格（Join Semi-Lattice）**：所有可能状态的集合，以合并操作作为连接运算。系统在这个格上单调前进，从而保证最终收敛。可以类比为水往低处流：状态只会沿着一个方向演进，永远不会倒退。

```json
Request:  {"type": "crdt_verify", "msg_id": 1, "state_a": {"n1": 3, "n2": 1}, "state_b": {"n1": 1, "n2": 5}}
Response: {"type": "crdt_verify_ok", "in_reply_to": 1, "merge_ab": {"n1": 3, "n2": 5}, "merge_ba": {"n1": 3, "n2": 5}, "commutative": true, "idempotent": true}
```

## 涉及概念

- `commutativity`
- `associativity`
- `idempotency`
- `lattice`
- `convergence proof`

## 实现提示

- 交换律：对任意状态 A 和 B，merge(A, B) == merge(B, A)
- 结合律：merge(A, merge(B, C)) == merge(merge(A, B), C)
- 幂等性：merge(A, A) == A
- 这三个性质保证了无论消息顺序或重复如何，系统都能收敛
- 逐元素取最大值操作满足以上三个性质

## 测试用例

### 1. 合并满足交换律

验证 merge_ab 等于 merge_ba，且 commutative 为 true。

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"crdt_verify","msg_id":2,"state_a":{"n1":3,"n2":1},"state_b":{"n1":1,"n2":5}}}
```

期望输出：

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

### 2. 合并满足幂等性

验证 merge(A, A) 等于 A，且 idempotent 为 true。

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

- [CRDT Convergence](https://hal.inria.fr/inria-00609399/document)：Shapiro 等人关于 CRDT 的综合研究

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
