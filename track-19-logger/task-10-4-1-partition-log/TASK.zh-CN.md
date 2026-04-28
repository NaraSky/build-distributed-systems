#模式l a Kafka Partition as a Write-Ahead 日志

英文标题：Model a Kafka Partition as a Write-Ahead Log
网页：<https://builddistributedsystem.com/tracks/logger/tasks/task-10-4-1-partition-log>

课程：19. 日志器：WAL、LSM 与分布式日志
任务序号：16
短标题：Partition 日志
难度：intermediate
子主题：Distributed 日志 (Kafka Architecture)

## 中文导读

本题要求你完成 `Model a Kafka Partition as a Write-Ahead 日志`。

重点关注：`Kafka partition`、`segment file`、`offset`、`append-only`、`sequential I/O`。

建议先按提示逐步实现：A Kafka partition is essentially a WAL stored as a directory of segment files。

协议字段、消息类型、输入输出格式请以本文件中的代码块和测试用例为准。

## 题目说明

At its core, Apache Kafka is a distributed 日志. Each topic is split into partitions,和each partition is an independent, ordered, append-only 日志 stored as a directory of segment files.

Partition structure on disk:
```
topic-orders/partition-0/
    00000000.日志      # 消息 at offsets 0-999
    00000000.索引    # sparse 索引: offset -> byte position
    00001000.日志      # 消息 at offsets 1000-1999
    00001000.索引
```

Key operations:
1. **Append**: producers write a 消息 to the end of the 日志, receiving the assigned offset
2. **Read**: consumers specify an offset和read 消息 sequentially from that point
3. **No mutation**: once written, 消息 are never modified or deleted (until retention policy kicks in)

This append-only design is why Kafka achieves such high throughput: sequential disk I/O is nearly as fast as memory access on modern SSDs.

```JSON
请求:  {"type": "partition_append", "msg_id": 1, "topic": "orders", "partition": 0, "消息": "order-1234"}
响应: {"type": "partition_append_ok", "in_reply_to": 1, "offset": 0, "segment": "00000000.日志", "timestamp": 1700000000}

请求:  {"type": "partition_read", "msg_id": 2, "topic": "orders", "partition": 0, "offset": 0}
响应: {"type": "partition_read_ok", "in_reply_to": 2, "消息": "order-1234", "offset": 0, "next_offset": 1}

请求:  {"type": "partition_info", "msg_id": 3, "topic": "orders", "partition": 0}
响应: {"type": "partition_info_ok", "in_reply_to": 3, "start_offset": 0, "end_offset": 42, "segments": 2, "total_bytes": 524288}
```

## 涉及概念

- `Kafka partition`
- `segment file`
- `offset`
- `append-only`
- `sequential I/O`

## 实现提示

- A Kafka partition is essentially a WAL stored as a directory of segment files
- Each segment has a .日志 file (raw 消息)和a .索引 file (offset -> byte position)
- Producers can only append to the end of the 日志 (no random writes)
- Consumers read at a given offset和can independently read at their own pace
- Kafka achieves millions of 消息 per second because appending is sequential I/O, which is extremely fast

## 测试用例

### 1. Append returns monotonically increasing offset

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

### 2. Read at offset returns correct 消息

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

- [The Log - Jay Kreps](https://engineering.linkedin.com/distributed-systems/log-what-every-software-engineer-should-know-about-real-time-datas-unifying)：Foundational article on the 日志 as a data structure by the creator of Kafka

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
