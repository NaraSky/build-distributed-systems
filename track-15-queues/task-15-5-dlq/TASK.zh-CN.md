# 添加 Dead Letter Queues

英文标题：Add Dead Letter Queues
网页：<https://builddistributedsystem.com/tracks/queues/tasks/task-15-5-dlq>

课程：15. 队列
任务序号：5
短标题：Dead Letter 队列
难度：intermediate
子主题：At-Most-Once和At-Least-Once Delivery

## 中文导读

本题要求你完成 `添加 Dead Letter Queues`。

重点关注：`DLQ`、`poison message`、`error handling`。

建议先按提示逐步实现：Track 重试 count per 消息。

协议字段、消息类型、输入输出格式请以本文件中的代码块和测试用例为准。

## 题目说明

Implement dead letter queues用于failed 消息:

1. Track 重试 count用于each 消息
2. On processing 故障, increment 重试 count
3. After N failures, move to dead letter 队列
4. Preserve: original 消息, error details, timestamps
5. Provide interface to inspect和replay DLQ 消息

DLQs prevent poison 消息 from blocking the 队列.

## 概念说明

### Dead Letter Queues

Some 消息 may never succeed: invalid format, missing data, bugs. Instead of retrying forever or losing them, move failures to a DLQ用于investigation. Operators can fix issues和replay 消息.

### Poison Messages

A poison 消息 is one that consistently fails processing. Without DLQ, it blocks the 队列 (if ordered) or wastes resources (if retried forever). DLQ isolates the poison so healthy 消息 flow.

## 涉及概念

- `DLQ`
- `poison message`
- `error handling`

## 实现提示

- Track 重试 count per 消息
- Move to DLQ after max retries
- Preserve error information

## 测试用例

### 1. Move to DLQ after retries

消息 m1 fails processing 3 times (max_retries=3). After 3rd 故障, 消息 should be moved to dead letter 队列，包含error details和重试 count. Verify poison 消息 does not block main 队列.

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
```

期望输出：

```text
{"src":"n1","dest":"c0","body":{"type":"init_ok","in_reply_to":1,"msg_id":0}}
```

### 2. Replay from DLQ

消息 in DLQ can be inspected和replayed. Operator fixes issue, triggers replay. 消息 moves from DLQ back to main 队列用于reprocessing. Verify DLQ provides inspection和replay capabilities.

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
```

期望输出：

```text
{"src":"n1","dest":"c0","body":{"type":"init_ok","in_reply_to":1,"msg_id":0}}
```

## 参考资料

- [DLQ Best Practices](https://aws.amazon.com/blogs/compute/designing-durable-serverless-apps-with-dlqs-for-amazon-sns-amazon-sqs-aws-lambda/)：AWS guide to dead letter queues

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
