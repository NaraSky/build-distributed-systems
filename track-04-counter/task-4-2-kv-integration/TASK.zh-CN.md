# Integrate Sequentially Consistent 键值 存储

英文标题：Integrate Sequentially Consistent Key-Value Store
网页：<https://builddistributedsystem.com/tracks/counter/tasks/task-4-2-kv-integration>

课程：4. 计数器：分布式状态与 CRDT
任务序号：2
短标题：KV Integration
难度：intermediate
子主题：The Lost Update Problem

## 中文导读

本题要求你完成 `Integrate Sequentially Consistent 键值 存储`。

重点关注：`sequential consistency`、`external storage`、`linearizability`。

建议先按提示逐步实现：Use Maelstrom seq-kv service。

协议字段、消息类型、输入输出格式请以本文件中的代码块和测试用例为准。

## 题目说明

Use Maelstrom's built-in seq-kv service to store your 计数器 value. This provides sequential consistency but introduces new challenges around availability during 网络 partitions.

## 概念说明

### Sequential Consistency

Sequential consistency guarantees that all operations appear to happen in some total order consistent，包含each process's local order. This is stronger than 最终一致性 but weaker than linearizability.

## 涉及概念

- `sequential consistency`
- `external storage`
- `linearizability`

## 实现提示

- Use Maelstrom seq-kv service
- Store 计数器 in external KV
- This still has issues under partitions

## 测试用例

### 1. KV-based 计数器

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

- [Maelstrom Services](https://github.com/jepsen-io/maelstrom/blob/main/doc/services.md)：Documentation用于Maelstrom built-in services

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
