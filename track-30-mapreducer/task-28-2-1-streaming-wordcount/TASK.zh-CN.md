# 实现 Streaming Word Count

英文标题：Implement Streaming Word Count
网页：<https://builddistributedsystem.com/tracks/mapreducer/tasks/task-28-2-1-streaming-wordcount>

课程：30. MapReducer：批处理与流处理
任务序号：6
短标题：Streaming Word Count
难度：intermediate
子主题：Stream Processing

## 中文导读

本题要求你完成 `实现 Streaming Word Count`。

重点关注：`stream processing`、`stateful processing`、`running aggregates`、`top-N`、`incremental updates`。

建议先按提示逐步实现：Keep a running word count dict in memory, update on every process 消息。

协议字段、消息类型、输入输出格式请以本文件中的代码块和测试用例为准。

## 题目说明

Batch MapReduce waits用于all data before producing output. Stream processing handles an **infinite flow** of events: state is updated as each event arrives,和results can be queried at any time.

Your 节点 maintains a running word count across all received 消息:

```JSON
// Process a batch of words — update running counts
{ "type": "process", "msg_id": 1, "words": ["hello", "world", "hello"] }
→ { "type": "processed", "in_reply_to": 1, "counts": {"hello": 2, "world": 1} }

// Return the top N words by count
{ "type": "topn", "msg_id": 2, "n": 2,
  "counts": {"hello": 5, "world": 3, "stream": 1} }
→ { "type": "topn", "in_reply_to": 2,
    "top_words": [["hello", 5], ["world", 3]] }

// Increment a single word和return its new count
{ "type": "update", "msg_id": 3, "word": "hello", "current_count": 5 }
→ { "type": "updated", "in_reply_to": 3, "word": "hello", "new_count": 6 }

// Emit top N from current in-memory state (periodic output)
{ "type": "output", "msg_id": 4, "interval_ms": 1000, "counts": {"hello": 10} }
→ { "type": "periodic_output", "in_reply_to": 4,
    "top_words": [["hello", 10]] }
```

Unlike batch processing, the 节点 never resets counts between 消息 — every `process` call adds to the global running totals.

## 涉及概念

- `stream processing`
- `stateful processing`
- `running aggregates`
- `top-N`
- `incremental updates`

## 实现提示

- Keep a running word count dict in memory, update on every process 消息
- topn: sort the dict by count descending, return the first N entries
- update increments a single word by 1和returns the new count
- output emits the top N words from current state without resetting it
- Lowercase和strip words before counting

## 测试用例

### 1. Process word stream

Should update running word counts和return current totals.

输入：

```json
{"src":"stream","dest":"processor","body":{"type":"process","msg_id":1,"words":["hello","world","hello"]}}
```

期望输出：

```text
{"type": "processed", "in_reply_to": 1, "counts": {"hello": 2, "world": 1}}
```

### 2. Output top N words

Should return top N words sorted by count descending.

输入：

```json
{"src":"stream","dest":"processor","body":{"type":"topn","msg_id":1,"n":2,"counts":{"hello":5,"world":3,"stream":1}}}
```

期望输出：

```text
{"type": "topn", "in_reply_to": 1, "top_words": [["hello", 5], ["world", 3]]}
```

## 参考资料

- [Streaming 101 — The World Beyond Batch](https://www.oreilly.com/ideas/the-world-beyond-batch-streaming-101)：Streaming 101 by Tyler Akidau

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
