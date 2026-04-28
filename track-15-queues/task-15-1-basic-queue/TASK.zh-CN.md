# 实现 基础 消息 队列

英文标题：Implement Basic Message Queue
网页：<https://builddistributedsystem.com/tracks/queues/tasks/task-15-1-basic-queue>

课程：15. 队列
任务序号：1
短标题：基础 队列
难度：intermediate
子主题：At-Most-Once和At-Least-Once Delivery

## 中文导读

本题要求你完成 `实现 基础 消息 队列`。

重点关注：`queue`、`producer-consumer`、`FIFO`。

建议先按提示逐步实现：Use thread-safe data structure。

协议字段、消息类型、输入输出格式请以本文件中的代码块和测试用例为准。

## 题目说明

Build a basic in-memory 消息 队列:

1. Producers enqueue 消息
2. Consumers dequeue 消息
3. 消息 delivered in FIFO order
4. Thread-safe用于concurrent access
5. Support blocking和non-blocking receive

This decouples producers和consumers in time.

## 概念说明

### 消息 Queues

Queues decouple components: producers emit 消息 without waiting, consumers process at their own pace. This enables asynchronous processing, load leveling,和resilient architectures.

### FIFO Ordering

First-in-first-out ensures 消息 are processed in send order. This matters用于ordered event streams. Strict FIFO limits parallelism - a trade-off to consider.

## 涉及概念

- `queue`
- `producer-consumer`
- `FIFO`

## 实现提示

- Use thread-safe data structure
- Block on empty 队列 or return None
-处理multiple producers/consumers

## 测试用例

### 1. FIFO order

Enqueue 消息 in order: m1, m2, m3. Dequeue should return 消息 in same order: m1, then m2, then m3. Verify FIFO ordering is preserved.

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
```

期望输出：

```text
{"src":"n1","dest":"c0","body":{"type":"init_ok","in_reply_to":1,"msg_id":0}}
```

### 2.并发access

Multiple producers enqueue concurrently. Multiple consumers dequeue concurrently. Verify 队列 handles concurrent access safely (no lost 消息, no duplicate delivery, thread-safe operations).

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
```

期望输出：

```text
{"src":"n1","dest":"c0","body":{"type":"init_ok","in_reply_to":1,"msg_id":0}}
```

## 参考资料

- [Message Queue Patterns](https://www.enterpriseintegrationpatterns.com/patterns/messaging/)：Enterprise Integration Patterns

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
