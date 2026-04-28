# 实现 Exactly-Once Semantics

英文标题：Implement Exactly-Once Semantics
网页：<https://builddistributedsystem.com/tracks/queues/tasks/task-15-4-exactly-once>

课程：15. 队列
任务序号：4
短标题：Exactly-Once
难度：advanced
子主题：At-Most-Once和At-Least-Once Delivery

## 中文导读

本题要求你完成 `实现 Exactly-Once Semantics`。

重点关注：`exactly-once`、`idempotency`、`deduplication`。

建议先按提示逐步实现：Dedup on producer side，包含消息 ID。

协议字段、消息类型、输入输出格式请以本文件中的代码块和测试用例为准。

## 题目说明

Achieve exactly-once processing semantics:

Producer side:
1. Assign unique ID to each 消息
2. 队列 deduplicates by ID

Consumer side:
1. Track processed 消息 IDs
2. Skip 消息 already processed
3. Atomically: process + commit offset + record as processed

This requires cooperation between producer, 队列,和consumer.

## 概念说明

### Exactly-Once Semantics

True exactly-once is end-to-end: exactly-once production + exactly-once consumption + idempotent processing. Kafka achieves this through idempotent producers, transactional consumers,和offset commits within transactions.

### Idempotency Keys

Using unique 消息 IDs, producers 重试 safely (队列 rejects duplicates)和consumers skip already-processed 消息. The challenge is tracking和garbage-collecting these IDs efficiently.

## 涉及概念

- `exactly-once`
- `idempotency`
- `deduplication`

## 实现提示

- Dedup on producer side，包含消息 ID
- Track processed IDs on consumer side
- Use transactions用于consume-produce

## 测试用例

### 1. Producer 去重

Producer sends 消息，包含id="msg1" twice (due to 重试). 队列 should detect duplicate based on 消息 ID和only store once. Verify consumer receives 消息 exactly once, not twice.

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
```

期望输出：

```text
{"src":"n1","dest":"c0","body":{"type":"init_ok","in_reply_to":1,"msg_id":0}}
```

### 2. Consumer skip duplicate

Consumer processes 消息 id="msg2", stores processed ID. 消息 is redelivered (due to 超时 or crash). Consumer should detect already processed this ID和skip it. Verify idempotent processing on consumer side.

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
```

期望输出：

```text
{"src":"n1","dest":"c0","body":{"type":"init_ok","in_reply_to":1,"msg_id":0}}
```

## 参考资料

- [Kafka Exactly-Once](https://www.confluent.io/blog/exactly-once-semantics-are-possible-heres-how-apache-kafka-does-it/)：How Kafka achieves exactly-once

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
