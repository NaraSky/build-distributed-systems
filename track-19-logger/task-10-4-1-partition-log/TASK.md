# Model a Kafka Partition as a Write-Ahead Log

Website: <https://builddistributedsystem.com/tracks/logger/tasks/task-10-4-1-partition-log>

Track: 19. The Logger
Task order: 16
Short title: Partition Log
Difficulty: intermediate
Subtrack: Distributed Log (Kafka Architecture)

## Problem

At its core, Apache Kafka is a distributed log. Each topic is split into partitions, and each partition is an independent, ordered, append-only log stored as a directory of segment files.

Partition structure on disk:
```
topic-orders/partition-0/
    00000000.log      # messages at offsets 0-999
    00000000.index    # sparse index: offset -> byte position
    00001000.log      # messages at offsets 1000-1999
    00001000.index
```

Key operations:
1. **Append**: producers write a message to the end of the log, receiving the assigned offset
2. **Read**: consumers specify an offset and read messages sequentially from that point
3. **No mutation**: once written, messages are never modified or deleted (until retention policy kicks in)

This append-only design is why Kafka achieves such high throughput: sequential disk I/O is nearly as fast as memory access on modern SSDs.

```json
Request:  {"type": "partition_append", "msg_id": 1, "topic": "orders", "partition": 0, "message": "order-1234"}
Response: {"type": "partition_append_ok", "in_reply_to": 1, "offset": 0, "segment": "00000000.log", "timestamp": 1700000000}

Request:  {"type": "partition_read", "msg_id": 2, "topic": "orders", "partition": 0, "offset": 0}
Response: {"type": "partition_read_ok", "in_reply_to": 2, "message": "order-1234", "offset": 0, "next_offset": 1}

Request:  {"type": "partition_info", "msg_id": 3, "topic": "orders", "partition": 0}
Response: {"type": "partition_info_ok", "in_reply_to": 3, "start_offset": 0, "end_offset": 42, "segments": 2, "total_bytes": 524288}
```

## Concepts

- Kafka partition
- segment file
- offset
- append-only
- sequential I/O

## Hints

- A Kafka partition is essentially a WAL stored as a directory of segment files
- Each segment has a .log file (raw messages) and a .index file (offset -> byte position)
- Producers can only append to the end of the log (no random writes)
- Consumers read at a given offset and can independently read at their own pace
- Kafka achieves millions of messages per second because appending is sequential I/O, which is extremely fast

## Test Cases

### 1. Append returns monotonically increasing offset

Input:

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"partition_append","msg_id":2,"topic":"orders","partition":0,"message":"msg-1"}}
{"src":"c1","dest":"n1","body":{"type":"partition_append","msg_id":3,"topic":"orders","partition":0,"message":"msg-2"}}
```

Expected output:

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
{"src": "n1", "dest": "c1", "body": {"type": "partition_append_ok", "in_reply_to": 2, "offset": 0, "msg_id": 1}}
{"src": "n1", "dest": "c1", "body": {"type": "partition_append_ok", "in_reply_to": 3, "offset": 1, "msg_id": 2}}
```

### 2. Read at offset returns correct message

Input:

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"partition_append","msg_id":2,"topic":"t","partition":0,"message":"hello"}}
{"src":"c1","dest":"n1","body":{"type":"partition_read","msg_id":3,"topic":"t","partition":0,"offset":0}}
```

Expected output:

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
{"src": "n1", "dest": "c1", "body": {"type": "partition_append_ok", "in_reply_to": 2, "offset": 0, "msg_id": 1}}
{"src": "n1", "dest": "c1", "body": {"type": "partition_read_ok", "in_reply_to": 3, "message": "hello", "offset": 0, "msg_id": 2}}
```

## Resources

- [The Log - Jay Kreps](https://engineering.linkedin.com/distributed-systems/log-what-every-software-engineer-should-know-about-real-time-datas-unifying): Foundational article on the log as a data structure by the creator of Kafka

## Java Starter

The matching local starter file is:

```text
src/main/java/Main.java
```
