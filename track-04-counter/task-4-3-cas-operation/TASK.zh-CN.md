# 实现比较并交换操作

网页：<https://builddistributedsystem.com/tracks/counter/tasks/task-4-3-cas-operation>

课程：4. 计数器：分布式状态与 CRDT
任务序号：3
短标题：比较并交换
难度：进阶
子主题：丢失更新问题

## 中文导读

这道题让你用比较并交换操作来实现计数器，从而解决丢失更新问题。比较并交换是一种原子操作，只有当前值与预期值匹配时才执行更新，否则就重试。这是无锁编程中最基础也最重要的原语之一。

## 题目说明

使用比较并交换（Compare-And-Swap，简称 CAS）操作来实现计数器。CAS 会在更新前检查值是否与预期一致：如果一致就执行更新，如果不一致说明有其他节点已经修改了这个值，此时需要重新读取并重试。通过这种方式可以防止丢失更新。

## 概念说明

### 比较并交换

CAS 是无锁算法的基石。它的工作原理可以类比为"乐观地尝试修改"：先读取当前值，计算新值，然后告诉系统"如果当前值还是我之前读到的那个，就把它改成新值"。如果检查失败，说明在你读取之后有其他人修改了这个值，你需要重新来过。这种"先尝试、失败就重试"的策略就是乐观并发控制（Optimistic Concurrency）的核心思想。

## 涉及概念

- `CAS`
- `optimistic concurrency`
- `atomic operations`

## 实现提示

- 先读取当前值，计算新值，然后用 CAS 更新
- 如果 CAS 失败，需要重试
- 注意处理读取和 CAS 之间的竞态条件

## 测试用例

### 1. 基于 CAS 的计数器

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"add","msg_id":2,"delta":5}}
{"src":"c2","dest":"n1","body":{"type":"read","msg_id":3}}
```

期望输出：

```text
{"src":"n1","dest":"c0","body":{"type":"init_ok","in_reply_to":1,"msg_id":0}}
{"src":"n1","dest":"c1","body":{"type":"add_ok","in_reply_to":2,"msg_id":1}}
{"src":"n1","dest":"c2","body":{"type":"read_ok","in_reply_to":3,"msg_id":2,"value":5}}
```

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
