# 实现 At-Least-Once Delivery

英文标题：Implement At-Least-Once Delivery
网页：<https://builddistributedsystem.com/tracks/queues/tasks/task-15-3-at-least-once>

课程：15. 队列
任务序号：3
短标题：At-Least-Once
难度：intermediate
子主题：At-Most-Once和At-Least-Once Delivery

## 中文导读

本题要求你完成 `实现 At-Least-Once Delivery`。

重点关注：`at-least-once`、`acknowledgment`、`redelivery`。

建议先按提示逐步实现：Do not remove until acknowledged。

协议字段、消息类型、输入输出格式请以本文件中的代码块和测试用例为准。

## 题目说明

Guarantee at-least-once delivery:

1. Consumer receives 消息 (not removed from 队列)
2. 消息 marked as "in-flight"，包含timestamp
3. Consumer processes和sends acknowledgment
4. 队列 removes 消息 on ack
5. If no ack within 超时, redeliver 消息

Consumer must be idempotent to handle potential duplicates.

## 概念说明

### At-Least-Once Delivery

At-least-once means every 消息 is delivered at least once, possibly more. If an ack is lost, the 消息 is redelivered. This requires idempotent consumers that handle duplicates gracefully.

### Visibility 超时

When a consumer receives a 消息, it becomes invisible to others用于a 超时 period. If not acknowledged, it reappears. This prevents multiple consumers processing the same 消息 simultaneously.

## 涉及概念

- `at-least-once`
- `acknowledgment`
- `redelivery`

## 实现提示

- Do not remove until acknowledged
- Redeliver after 超时
- Track in-flight 消息

## 测试用例

### 1. Redeliver on 超时

Consumer receives 消息 m1，包含1s ack 超时. Consumer does not send ack within 超时. After 超时, 消息 should be redelivered to same or different consumer. Verify 消息 is not lost和redelivered at-least-once.

输入：

```json
{"src":"c0","dest":"queue","body":{"type":"init","msg_id":1,"node_id":"queue","node_ids":["queue"]}}
{"src":"producer","dest":"queue","body":{"type":"enqueue","msg_id":2,"message_id":"m1","value":"hello"}}
{"src":"consumer","dest":"queue","body":{"type":"dequeue","msg_id":3,"ack_timeout":1000}}
```

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
