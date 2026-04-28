# 实现 Exactly-Once Processing

英文标题：Implement Exactly-Once Processing
网页：<https://builddistributedsystem.com/tracks/mapreducer/tasks/task-28-2-5-exactly-once>

课程：30. MapReducer：批处理与流处理
任务序号：10
短标题：Exactly-Once
难度：advanced
子主题：Stream Processing

## 中文导读

本题要求你完成 `实现 Exactly-Once Processing`。

重点关注：`exactly-once`、`idempotency`、`deduplication`、`checkpointing`、`transactional commits`。

建议先按提示逐步实现：Track processed event IDs in a set; skip duplicates silently。

协议字段、消息类型、输入输出格式请以本文件中的代码块和测试用例为准。

## 题目说明

Exactly-once processing means each event affects the output exactly once, even when the system retries failed operations. It combines three mechanisms: **deduplication** (skip events already seen), **checkpointing** (save state so recovery can resume),和**transactional output** (commit results atomically).

```
Without exactly-once:
  process "hello"  -> count=1
  (crash, 重试)
  process "hello"  -> count=2  <- WRONG, counted twice

With exactly-once (deduplication):
  process "hello" (id=e1)  -> count=1, mark e1 seen
  (crash, 重试)
  process "hello" (id=e1)  -> skip (e1 already seen) -> count=1 still correct
```

Your 节点 handles four 消息 types:

```JSON
// Process an event; skip if event_id was already seen
{ "type": "process", "msg_id": 1,
  "event_id": "e1", "word": "hello" }
-> { "type": "processed", "in_reply_to": 1,
    "word": "hello", "count": 1, "was_duplicate": false }

// Save current state as a named checkpoint
{ "type": "checkpoint", "msg_id": 2, "checkpoint_id": "cp1" }
-> { "type": "checkpoint_saved", "in_reply_to": 2, "checkpoint_id": "cp1" }

// Restore state from a checkpoint
{ "type": "restore", "msg_id": 3, "checkpoint_id": "cp1" }
-> { "type": "restored", "in_reply_to": 3,
    "counts": {"hello": 1} }

// Commit pending outputs atomically
{ "type": "commit", "msg_id": 4 }
-> { "type": "committed", "in_reply_to": 4, "output_count": 1 }
```

## 涉及概念

- `exactly-once`
- `idempotency`
- `deduplication`
- `checkpointing`
- `transactional commits`

## 实现提示

- Track processed event IDs in a set; skip duplicates silently
- Checkpoint saves the current count state so recovery can resume from it
- restore loads the checkpoint和replaces current state
- commit moves pending outputs to committed atomically; rollback discards them
- At-least-once + idempotency = effectively exactly-once

## 测试用例

### 1. Idempotent processing

Second 消息，包含same event_id must be a no-op (count stays at 1).

输入：

```json
{"src":"stream","dest":"processor","body":{"type":"process","msg_id":1,"event_id":"e1","word":"hello"}}
{"src":"stream","dest":"processor","body":{"type":"process","msg_id":2,"event_id":"e1","word":"hello"}}
```

期望输出：

```text
{"type": "processed", "in_reply_to": 1, "word": "hello", "count": 1, "was_duplicate": false}
{"type": "processed", "in_reply_to": 2, "word": "hello", "count": 1, "was_duplicate": true}
```

### 2. Checkpoint和restore

Restore should return the state that was saved at checkpoint time.

输入：

```json
{"src":"stream","dest":"processor","body":{"type":"process","msg_id":1,"event_id":"e1","word":"hello"}}
{"src":"client","dest":"processor","body":{"type":"checkpoint","msg_id":2,"checkpoint_id":"cp1"}}
{"src":"client","dest":"processor","body":{"type":"restore","msg_id":3,"checkpoint_id":"cp1"}}
```

期望输出：

```text
{"type": "processed", "in_reply_to": 1, "word": "hello", "count": 1, "was_duplicate": false}
{"type": "checkpoint_saved", "in_reply_to": 2, "checkpoint_id": "cp1"}
{"type": "restored", "in_reply_to": 3, "counts": {"hello": 1}}
```

## 参考资料

- [Exactly-Once Semantics in Apache Kafka](https://www.confluent.io/blog/exactly-once-semantics-are-possible-heres-how-apache-kafka-does-it/)：How Kafka achieves exactly-once delivery end-to-end

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
