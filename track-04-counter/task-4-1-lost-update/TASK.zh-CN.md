# 实现基础计数器：体验丢失更新问题

网页：<https://builddistributedsystem.com/tracks/counter/tasks/task-4-1-lost-update>

课程：4. 计数器：分布式状态与 CRDT
任务序号：1
短标题：丢失更新
难度：入门
子主题：丢失更新问题

## 中文导读

这道题让你实现一个最简单的只增计数器，处理"加"和"读"两种操作。在单节点顺序执行时一切正常，但当多个节点并发更新时，你会亲眼看到"更新丢失"现象。这个问题是理解分布式计数器为什么需要特殊设计的起点。

## 题目说明

实现一个基础的只增计数器（Grow-Only Counter），支持加法操作和读取操作。多个节点（Node）共享计数器状态，但你的初始实现在并发场景下会丢失更新。

这道题故意展示了丢失更新问题（Lost Update Problem）。你的计数器在顺序操作时可以正常工作，但在多节点并发更新时会无法通过验证。

## 概念说明

### 丢失更新问题

当多个节点同时读取、修改、写入同一个状态时，更新可能会丢失。举个例子：节点 A 读到值是 5，节点 B 也读到 5，两者各自加 1 后都写入 6，结果只加了 1 而不是 2。这就像两个人同时编辑同一份文档，一个人的修改会覆盖另一个人的。这正是分布式计数器需要特殊处理的原因。

## 涉及概念

- `lost updates`
- `race conditions`
- `naive replication`

## 实现提示

- 从一个简单的计数器开始实现
- 注意观察并发更新时会发生什么
- 这道题本身就是为了让你看到失败而设计的

## 测试用例

### 1. 基础计数器加法

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"add","msg_id":2,"delta":5}}
{"src":"c1","dest":"n1","body":{"type":"read","msg_id":3}}
```

期望输出：

```text
{"src":"n1","dest":"c0","body":{"type":"init_ok","in_reply_to":1,"msg_id":0}}
{"src":"n1","dest":"c1","body":{"type":"add_ok","in_reply_to":2,"msg_id":1}}
{"src":"n1","dest":"c1","body":{"type":"read_ok","in_reply_to":3,"msg_id":2,"value":5}}
```

### 2. 顺序递增正常工作

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"add","msg_id":2,"delta":3}}
{"src":"c2","dest":"n1","body":{"type":"add","msg_id":3,"delta":2}}
{"src":"c3","dest":"n1","body":{"type":"read","msg_id":4}}
```

期望输出：

```text
{"src":"n1","dest":"c0","body":{"type":"init_ok","in_reply_to":1,"msg_id":0}}
{"src":"n1","dest":"c1","body":{"type":"add_ok","in_reply_to":2,"msg_id":1}}
{"src":"n1","dest":"c2","body":{"type":"add_ok","in_reply_to":3,"msg_id":2}}
{"src":"n1","dest":"c3","body":{"type":"read_ok","in_reply_to":4,"msg_id":3,"value":5}}
```

## 参考资料

- [G-Counter Challenge](https://fly.io/dist-sys/4/)：Fly.io 的只增计数器挑战

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
