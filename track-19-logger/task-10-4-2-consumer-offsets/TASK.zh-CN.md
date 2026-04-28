# 实现 Consumer Group Offset Tracking

英文标题：Implement Consumer Group Offset Tracking
网页：<https://builddistributedsystem.com/tracks/logger/tasks/task-10-4-2-consumer-offsets>

课程：19. 日志器：WAL、LSM 与分布式日志
任务序号：17
短标题：Consumer Offsets
难度：intermediate
子主题：Distributed 日志 (Kafka Architecture)

## 中文导读

本题要求你完成 `实现 Consumer Group Offset Tracking`。

重点关注：`consumer offset`、`consumer group`、`commit offset`、`fetch offset`、`at-least-once delivery`。

建议先按提示逐步实现：Each consumer group maintains an independent offset per partition (their "bookmark")。

协议字段、消息类型、输入输出格式请以本文件中的代码块和测试用例为准。

## 题目说明

Consumer offset tracking enables consumers to read at their own pace和resume after restarts. Each consumer group independently tracks its position in each partition.

The offset lifecycle:
1. **Consumer starts**: calls `fetch_offset` to find where it last left off
2. **Consumer reads**: fetches 消息 starting from its offset
3. **Consumer processes**: performs application logic on the 消息
4. **Consumer commits**: calls `commit_offset` to save its new position
5. **Consumer crashes**: on restart, calls `fetch_offset` again和resumes from the last committed offset

This gives **at-least-once delivery**: if a consumer crashes after processing but before committing, it will re-process those 消息 on restart. For **exactly-once**, additional mechanisms are needed.

Multiple consumer groups can read the same partition independently at different speeds — a key Kafka design principle.

```JSON
请求:  {"type": "commit_offset", "msg_id": 1, "group": "analytics", "topic": "orders", "partition": 0, "offset": 42}
响应: {"type": "commit_offset_ok", "in_reply_to": 1}

请求:  {"type": "fetch_offset", "msg_id": 2, "group": "analytics", "topic": "orders", "partition": 0}
响应: {"type": "fetch_offset_ok", "in_reply_to": 2, "offset": 42}

请求:  {"type": "fetch_offset", "msg_id": 3, "group": "billing", "topic": "orders", "partition": 0}
响应: {"type": "fetch_offset_ok", "in_reply_to": 3, "offset": 0}
```

## 涉及概念

- `consumer offset`
- `consumer group`
- `commit offset`
- `fetch offset`
- `at-least-once delivery`

## 实现提示

- Each consumer group maintains an independent offset per partition (their "bookmark")
- commit_offset: 客户端 saves its current position after processing 消息
- fetch_offset: retrieve where the consumer last left off (for resuming after restart)
- If a consumer crashes before committing, it re-reads from the last committed offset (at-least-once)
- In real Kafka, offsets are stored in a special internal topic (__consumer_offsets)

## 测试用例

### 1. Commit和fetch offset roundtrip

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

### 2. Different groups track independent offsets

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

- [Kafka Consumer Offset Management](https://kafka.apache.org/documentation/#impl_offsettracking)：How Kafka tracks consumer group offsets使用the __consumer_offsets internal topic

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
