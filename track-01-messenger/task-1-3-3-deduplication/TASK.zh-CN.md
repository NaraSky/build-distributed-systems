# 实现 消息 去重，包含LRU 缓存

英文标题：Implement Message Deduplication，包含LRU Cache
网页：<https://builddistributedsystem.com/tracks/messenger/tasks/task-1-3-3-deduplication>

课程：1. 信使：消息通信基础
任务序号：13
短标题：去重
难度：intermediate
子主题：The Protocol Beneath

## 中文导读

本题要求你完成 `实现 消息 去重，包含LRU 缓存`。

重点关注：`idempotency`、`deduplication`、`LRU cache`、`at-most-once delivery`。

建议先按提示逐步实现：Use (src, msg_id) as the deduplication key since msg_id is only unique per sender。

协议字段、消息类型、输入输出格式请以本文件中的代码块和测试用例为准。

## 题目说明

Networks can duplicate 消息. If a sender retries because it did not receive an acknowledgment (but the original was actually delivered), the receiver sees the same 请求 twice. Without **deduplication**, the receiver processes it twice, which can cause incorrect state.

Your task is to implement 消息 deduplication:

1. Maintain a bounded **LRU 缓存** of recently seen 消息 IDs (capacity: 1000)
2. The deduplication key is `(src, msg_id)` — msg_id alone is not globally unique
3. When a duplicate is detected, skip processing but still reply (to ensure the sender's 重试 gets acknowledged)
4. Track和report deduplication statistics

Implement a `dedup_echo` 消息 type that behaves like echo but applies deduplication:

```JSON
请求:  {"type": "dedup_echo", "msg_id": 5, "echo": "hello"}
响应: {"type": "dedup_echo_ok", "in_reply_to": 5, "echo": "hello", "was_duplicate": false}
```

If the same `(src, msg_id)` pair is seen again:
```JSON
响应: {"type": "dedup_echo_ok", "in_reply_to": 5, "echo": "hello", "was_duplicate": true}
```

Implement a `dedup_stats` 消息 to report statistics:
```JSON
响应: {"type": "dedup_stats_ok", "total": 10, "duplicates": 2, "cache_size": 8}
```

## 涉及概念

- `idempotency`
- `deduplication`
- `LRU cache`
- `at-most-once delivery`

## 实现提示

- Use (src, msg_id) as the deduplication key since msg_id is only unique per sender
- An OrderedDict works well as a bounded LRU 缓存 in Python
- When the 缓存 exceeds its capacity, remove the oldest entry
- Skip processing用于duplicate 消息 but still acknowledge receipt
- 日志 duplicates to 标准错误用于debugging

## 测试用例

### 1. First dedup_echo is not a duplicate

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"dedup_echo","msg_id":10,"echo":"first"}}
```

期望输出：

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
{"src": "n1", "dest": "c1", "body": {"type": "dedup_echo_ok", "echo": "first", "was_duplicate": false, "in_reply_to": 10, "msg_id": 1}}
```

### 2. Duplicate msg_id from same source detected

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"dedup_echo","msg_id":10,"echo":"hello"}}
{"src":"c1","dest":"n1","body":{"type":"dedup_echo","msg_id":10,"echo":"hello"}}
```

期望输出：

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
{"src": "n1", "dest": "c1", "body": {"type": "dedup_echo_ok", "echo": "hello", "was_duplicate": false, "in_reply_to": 10, "msg_id": 1}}
{"src": "n1", "dest": "c1", "body": {"type": "dedup_echo_ok", "echo": "hello", "was_duplicate": true, "in_reply_to": 10, "msg_id": 2}}
```

## 参考资料

- [Exactly-Once Delivery in Distributed Systems](https://www.confluent.io/blog/exactly-once-semantics-are-possible-heres-how-apache-kafka-does-it/)：Confluent blog on deduplication和exactly-once semantics in Kafka

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
