# 实现流式词频统计

英文标题：Implement Streaming Word Count
网页：<https://builddistributedsystem.com/tracks/mapreducer/tasks/task-28-2-1-streaming-wordcount>

课程：30. MapReducer：批处理与流处理
任务序号：6
短标题：流式词频统计
难度：进阶
子主题：Stream Processing

## 中文导读

本题要求你实现一个流式词频统计节点。与批处理等所有数据到齐才出结果不同，流处理面对的是源源不断的事件流。你的节点需要在内存中维护一个持续更新的词频表，每收到一批新单词就累加计数，随时可以查询当前的统计结果。这是从批处理思维转向流处理思维的第一步。

## 题目说明

批处理模式的 MapReduce 需要等所有数据到齐才能产生输出。流处理（Stream Processing）则处理**无限的事件流**：每当一个事件到达就立即更新状态，结果可以在任意时刻查询。

你的节点需要在所有收到的消息中维护一个持续累加的词频统计表：

```json
// 处理一批单词——更新运行中的计数
{ "type": "process", "msg_id": 1, "words": ["hello", "world", "hello"] }
-> { "type": "processed", "in_reply_to": 1, "counts": {"hello": 2, "world": 1} }

// 返回按计数排名的前 N 个单词
{ "type": "topn", "msg_id": 2, "n": 2,
  "counts": {"hello": 5, "world": 3, "stream": 1} }
-> { "type": "topn", "in_reply_to": 2,
    "top_words": [["hello", 5], ["world", 3]] }

// 对单个单词计数加 1 并返回新计数
{ "type": "update", "msg_id": 3, "word": "hello", "current_count": 5 }
-> { "type": "updated", "in_reply_to": 3, "word": "hello", "new_count": 6 }

// 从当前内存状态中输出前 N 个单词（周期性输出）
{ "type": "output", "msg_id": 4, "interval_ms": 1000, "counts": {"hello": 10} }
-> { "type": "periodic_output", "in_reply_to": 4,
    "top_words": [["hello", 10]] }
```

与批处理不同，节点在消息之间不会重置计数。每次 `process` 调用都会累加到全局运行总数上。

## 概念说明

流式处理就像一个一直开着的水龙头：水不停地流，你不能等水放完了再量有多少，而是需要一边接水一边计量。词频统计节点就像一个实时计数器，每来一个单词就在对应的格子上加一。你可以随时看一眼计数器上的数字，而不用等"全部单词都处理完"。

## 涉及概念

- `stream processing`
- `stateful processing`
- `running aggregates`
- `top-N`
- `incremental updates`

## 实现提示

- 在内存中维护一个持续运行的词频字典，每次收到 process 消息时更新
- 排名查询：按计数从高到低排序，返回前 N 个条目
- 更新操作将单个单词的计数加 1 并返回新值
- 输出操作从当前状态读取前 N 个单词，但不重置状态
- 计数前对单词进行去空格和转小写处理

## 测试用例

### 1. 处理单词流

应更新运行中的词频统计并返回当前总计数。

输入：

```json
{"src":"stream","dest":"processor","body":{"type":"process","msg_id":1,"words":["hello","world","hello"]}}
```

期望输出：

```text
{"type": "processed", "in_reply_to": 1, "counts": {"hello": 2, "world": 1}}
```

### 2. 输出前 N 个单词

应返回按计数从高到低排序的前 N 个单词。

输入：

```json
{"src":"stream","dest":"processor","body":{"type":"topn","msg_id":1,"n":2,"counts":{"hello":5,"world":3,"stream":1}}}
```

期望输出：

```text
{"type": "topn", "in_reply_to": 1, "top_words": [["hello", 5], ["world", 3]]}
```

## 参考资料

- [Streaming 101 — The World Beyond Batch](https://www.oreilly.com/ideas/the-world-beyond-batch-streaming-101)：Tyler Akidau 的流处理入门文章

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
