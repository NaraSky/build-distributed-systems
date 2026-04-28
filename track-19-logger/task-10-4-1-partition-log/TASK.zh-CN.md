# 将 Kafka 分区建模为预写日志

英文标题：Model a Kafka Partition as a Write-Ahead Log
网页：<https://builddistributedsystem.com/tracks/logger/tasks/task-10-4-1-partition-log>

课程：19. 日志器：WAL、LSM 与分布式日志
任务序号：16
短标题：Partition Log
难度：进阶
子主题：Distributed Log (Kafka Architecture)

## 中文导读

本题要求你实现一个类似 Kafka 分区的追加式日志结构。Kafka 的核心其实就是一个分布式日志系统——每个分区是一段独立的、只能追加写入的有序日志。理解这一结构，是掌握 Kafka 以及所有流式处理系统的基础。

## 题目说明

Apache Kafka 的核心是一个分布式日志（Distributed Log）。每个主题（Topic）被拆分为多个分区（Partition），每个分区是一段独立的、有序的、只能追加的日志，在磁盘上以一组段文件（Segment File）的形式存储。

分区在磁盘上的结构如下：
```
topic-orders/partition-0/
    00000000.log      # messages at offsets 0-999
    00000000.index    # sparse index: offset -> byte position
    00001000.log      # messages at offsets 1000-1999
    00001000.index
```

核心操作：
1. **追加（Append）**：生产者将消息写入日志的末尾，获得分配的偏移量（Offset）
2. **读取（Read）**：消费者指定一个偏移量，从该位置开始顺序读取消息
3. **不可修改**：消息一旦写入就不会被修改或删除（直到保留策略触发清理）

这种只追加的设计是 Kafka 能够实现超高吞吐量的原因：在现代固态硬盘上，顺序磁盘读写的速度几乎接近内存访问。

```json
Request:  {"type": "partition_append", "msg_id": 1, "topic": "orders", "partition": 0, "message": "order-1234"}
Response: {"type": "partition_append_ok", "in_reply_to": 1, "offset": 0, "segment": "00000000.log", "timestamp": 1700000000}

Request:  {"type": "partition_read", "msg_id": 2, "topic": "orders", "partition": 0, "offset": 0}
Response: {"type": "partition_read_ok", "in_reply_to": 2, "message": "order-1234", "offset": 0, "next_offset": 1}

Request:  {"type": "partition_info", "msg_id": 3, "topic": "orders", "partition": 0}
Response: {"type": "partition_info_ok", "in_reply_to": 3, "start_offset": 0, "end_offset": 42, "segments": 2, "total_bytes": 524288}
```

## 涉及概念

- `Kafka partition`
- `segment file`
- `offset`
- `append-only`
- `sequential I/O`

## 实现提示

- 一个 Kafka 分区本质上是一个以段文件目录形式存储的预写日志
- 每个段包含一个 .log 文件（原始消息）和一个 .index 文件（偏移量到字节位置的映射）
- 生产者只能向日志末尾追加写入（不能随机写入）
- 消费者从指定的偏移量开始读取，每个消费者可以按自己的节奏独立消费
- Kafka 之所以能达到每秒数百万条消息的吞吐量，是因为追加写入属于顺序读写，速度极快

## 测试用例

### 1. 追加操作返回单调递增的偏移量

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"partition_append","msg_id":2,"topic":"orders","partition":0,"message":"msg-1"}}
{"src":"c1","dest":"n1","body":{"type":"partition_append","msg_id":3,"topic":"orders","partition":0,"message":"msg-2"}}
```

期望输出：

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
{"src": "n1", "dest": "c1", "body": {"type": "partition_append_ok", "in_reply_to": 2, "offset": 0, "msg_id": 1}}
{"src": "n1", "dest": "c1", "body": {"type": "partition_append_ok", "in_reply_to": 3, "offset": 1, "msg_id": 2}}
```

### 2. 按偏移量读取返回正确的消息

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"partition_append","msg_id":2,"topic":"t","partition":0,"message":"hello"}}
{"src":"c1","dest":"n1","body":{"type":"partition_read","msg_id":3,"topic":"t","partition":0,"offset":0}}
```

期望输出：

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
{"src": "n1", "dest": "c1", "body": {"type": "partition_append_ok", "in_reply_to": 2, "offset": 0, "msg_id": 1}}
{"src": "n1", "dest": "c1", "body": {"type": "partition_read_ok", "in_reply_to": 3, "message": "hello", "offset": 0, "msg_id": 2}}
```

## 参考资料

- [The Log - Jay Kreps](https://engineering.linkedin.com/distributed-systems/log-what-every-software-engineer-should-know-about-real-time-datas-unifying)：Kafka 创始人撰写的关于"日志"这一数据结构的经典文章

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
