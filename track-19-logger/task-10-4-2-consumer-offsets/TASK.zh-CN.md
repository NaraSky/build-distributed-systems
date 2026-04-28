# 实现消费者组的偏移量追踪

英文标题：Implement Consumer Group Offset Tracking
网页：<https://builddistributedsystem.com/tracks/logger/tasks/task-10-4-2-consumer-offsets>

课程：19. 日志器：WAL、LSM 与分布式日志
任务序号：17
短标题：Consumer Offsets
难度：进阶
子主题：Distributed Log (Kafka Architecture)

## 中文导读

本题要求你实现消费者组（Consumer Group）的偏移量追踪机制。每个消费者组独立记录自己在各分区中"读到哪里了"，这样消费者就能按自己的节奏消费消息，并在重启后从上次的位置继续。这是 Kafka 实现可靠消息消费的核心机制。

## 题目说明

消费者偏移量追踪（Consumer Offset Tracking）让消费者能够按自己的节奏读取消息，并在重启后恢复到之前的位置。每个消费者组独立跟踪它在每个分区中的消费进度。

偏移量的生命周期如下：
1. **消费者启动**：调用 `fetch_offset` 获取上次停止的位置
2. **消费者读取**：从偏移量所在位置开始拉取消息
3. **消费者处理**：对消息执行业务逻辑
4. **消费者提交**：调用 `commit_offset` 保存当前的消费位置
5. **消费者崩溃**：重启后再次调用 `fetch_offset`，从上次提交的偏移量继续消费

这提供了**至少一次投递（At-Least-Once Delivery）**语义：如果消费者在处理完消息后、提交偏移量之前崩溃，重启后会重新处理这些消息。要实现**精确一次（Exactly-Once）**语义，需要额外的机制。

多个消费者组可以独立地、以不同的速度读取同一个分区——这是 Kafka 的一个核心设计原则。

```json
Request:  {"type": "commit_offset", "msg_id": 1, "group": "analytics", "topic": "orders", "partition": 0, "offset": 42}
Response: {"type": "commit_offset_ok", "in_reply_to": 1}

Request:  {"type": "fetch_offset", "msg_id": 2, "group": "analytics", "topic": "orders", "partition": 0}
Response: {"type": "fetch_offset_ok", "in_reply_to": 2, "offset": 42}

Request:  {"type": "fetch_offset", "msg_id": 3, "group": "billing", "topic": "orders", "partition": 0}
Response: {"type": "fetch_offset_ok", "in_reply_to": 3, "offset": 0}
```

## 涉及概念

- `consumer offset`
- `consumer group`
- `commit offset`
- `fetch offset`
- `at-least-once delivery`

## 实现提示

- 每个消费者组为每个分区维护一个独立的偏移量（相当于一个"书签"）
- commit_offset：客户端在处理完消息后保存当前的消费位置
- fetch_offset：获取消费者上次停止的位置（用于重启后恢复消费）
- 如果消费者在提交偏移量之前崩溃，它会从上次提交的位置重新读取（至少一次语义）
- 在真正的 Kafka 中，偏移量存储在一个特殊的内部主题（__consumer_offsets）中

## 测试用例

### 1. 提交和获取偏移量的往返测试

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"commit_offset","msg_id":2,"group":"g1","topic":"t1","partition":0,"offset":10}}
{"src":"c1","dest":"n1","body":{"type":"fetch_offset","msg_id":3,"group":"g1","topic":"t1","partition":0}}
```

期望输出：

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
{"src": "n1", "dest": "c1", "body": {"type": "commit_offset_ok", "in_reply_to": 2, "msg_id": 1}}
{"src": "n1", "dest": "c1", "body": {"type": "fetch_offset_ok", "in_reply_to": 3, "offset": 10, "msg_id": 2}}
```

### 2. 不同消费者组独立追踪偏移量

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"commit_offset","msg_id":2,"group":"fast","topic":"t1","partition":0,"offset":100}}
{"src":"c1","dest":"n1","body":{"type":"commit_offset","msg_id":3,"group":"slow","topic":"t1","partition":0,"offset":5}}
{"src":"c1","dest":"n1","body":{"type":"fetch_offset","msg_id":4,"group":"fast","topic":"t1","partition":0}}
{"src":"c1","dest":"n1","body":{"type":"fetch_offset","msg_id":5,"group":"slow","topic":"t1","partition":0}}
```

期望输出：

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
{"src": "n1", "dest": "c1", "body": {"type": "commit_offset_ok", "in_reply_to": 2, "msg_id": 1}}
{"src": "n1", "dest": "c1", "body": {"type": "commit_offset_ok", "in_reply_to": 3, "msg_id": 2}}
{"src": "n1", "dest": "c1", "body": {"type": "fetch_offset_ok", "in_reply_to": 4, "offset": 100, "msg_id": 3}}
{"src": "n1", "dest": "c1", "body": {"type": "fetch_offset_ok", "in_reply_to": 5, "offset": 5, "msg_id": 4}}
```

## 参考资料

- [Kafka Consumer Offset Management](https://kafka.apache.org/documentation/#impl_offsettracking)：Kafka 官方文档，讲解如何通过 __consumer_offsets 内部主题追踪消费者组偏移量

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
