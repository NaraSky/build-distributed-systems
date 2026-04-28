# 添加 Consumer Groups，包含Partitions

英文标题：Add Consumer Groups，包含Partitions
网页：<https://builddistributedsystem.com/tracks/queues/tasks/task-15-2-consumer-groups>

课程：15. 队列
任务序号：2
短标题：Consumer Groups
难度：intermediate
子主题：At-Most-Once和At-Least-Once Delivery

## 中文导读

本题要求你完成 `添加 Consumer Groups，包含Partitions`。

重点关注：`consumer groups`、`partitioning`、`parallel processing`。

建议先按提示逐步实现：Partition 消息 by key。

协议字段、消息类型、输入输出格式请以本文件中的代码块和测试用例为准。

## 题目说明

Implement Kafka-style consumer groups:

1. Topic has multiple partitions
2. 消息，包含same key go to same partition
3. Consumer group: each partition assigned to one consumer
4. Multiple groups each see all 消息
5. Rebalance partitions when consumers change

This enables parallel consumption while maintaining per-key ordering.

## 概念说明

### Consumer Groups

Kafka pioneered consumer groups. Within a group, partitions are divided among consumers用于parallelism. Different groups independently consume all 消息 (pub-sub pattern，包含scaling).

### Partition Assignment

When consumers join/leave, partitions must be reassigned. Cooperative rebalancing minimizes disruption. Partition count limits max parallelism - plan accordingly.

## 涉及概念

- `consumer groups`
- `partitioning`
- `parallel processing`

## 实现提示

- Partition 消息 by key
- Each partition assigned to one consumer per group
- Rebalance on consumer join/leave

## 测试用例

### 1. Parallel consumption

Topic，包含4 partitions. Consumer group，包含2 consumers (c1, c2). Each consumer should be assigned 2 partitions. 消息，包含same key go to same partition. Verify consumers process partitions in parallel和maintain per-key ordering.

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
```

期望输出：

```text
{"src":"n1","dest":"c0","body":{"type":"init_ok","in_reply_to":1,"msg_id":0}}
```

## 参考资料

- [Kafka Consumer Groups](https://kafka.apache.org/documentation/#intro_consumers)：Kafka consumer documentation

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
