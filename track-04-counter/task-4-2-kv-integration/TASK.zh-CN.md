# 接入顺序一致性键值存储

网页：<https://builddistributedsystem.com/tracks/counter/tasks/task-4-2-kv-integration>

课程：4. 计数器：分布式状态与 CRDT
任务序号：2
短标题：键值存储集成
难度：进阶
子主题：丢失更新问题

## 中文导读

这道题让你使用 Maelstrom 内置的顺序一致性键值存储服务来保存计数器的值。虽然顺序一致性比最终一致性更强，但在网络分区时会面临可用性方面的新挑战。通过这道题，你将体会到一致性与可用性之间的权衡。

## 题目说明

使用 Maelstrom 内置的 seq-kv 服务来存储计数器的值。这个服务提供了顺序一致性（Sequential Consistency）保证，但同时也引入了新的问题：在网络分区期间，服务的可用性会受到影响。

## 概念说明

### 顺序一致性

顺序一致性保证所有操作看起来按照某个全局顺序执行，并且这个顺序与每个进程本地的操作顺序一致。打个比方，就像排队买票，每个人都按自己的先后顺序排队，所有人合在一起也有一个明确的先后顺序。顺序一致性比最终一致性更强，但比线性一致性（Linearizability）更弱。

## 涉及概念

- `sequential consistency`
- `external storage`
- `linearizability`

## 实现提示

- 使用 Maelstrom 的 seq-kv 服务
- 将计数器的值存储在外部键值存储中
- 注意在网络分区时仍然会存在问题

## 测试用例

### 1. 基于键值存储的计数器

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"add","msg_id":2,"delta":10}}
{"src":"c2","dest":"n1","body":{"type":"read","msg_id":3}}
```

期望输出：

```text
{"src":"n1","dest":"c0","body":{"type":"init_ok","in_reply_to":1,"msg_id":0}}
{"src":"n1","dest":"c1","body":{"type":"add_ok","in_reply_to":2,"msg_id":1}}
{"src":"n1","dest":"c2","body":{"type":"read_ok","in_reply_to":3,"msg_id":2,"value":10}}
```

## 参考资料

- [Maelstrom Services](https://github.com/jepsen-io/maelstrom/blob/main/doc/services.md)：Maelstrom 内置服务的文档

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
