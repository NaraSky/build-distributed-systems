# 实现 Single-Machine MapReduce

英文标题：Implement Single-Machine MapReduce
网页：<https://builddistributedsystem.com/tracks/mapreducer/tasks/task-28-1-1-mapreduce-basics>

课程：30. MapReducer：批处理与流处理
任务序号：1
短标题：MapReduce Basics
难度：intermediate
子主题：MapReduce Fundamentals

## 中文导读

本题要求你完成 `实现 Single-Machine MapReduce`。

重点关注：`MapReduce`、`map phase`、`reduce phase`、`word count`、`key-value pairs`。

建议先按提示逐步实现：Map emits (word, 1)用于each word in the input line。

协议字段、消息类型、输入输出格式请以本文件中的代码块和测试用例为准。

## 题目说明

MapReduce splits work into two simple phases: **map** transforms each input record into key-value pairs,和**reduce** aggregates all values用于the same key.

Your 节点 handles three 消息 types:

```JSON
// Map a single line into word-count pairs
{ "type": "map", "msg_id": 1, "line": "hello world hello" }
→ { "type": "map_result", "in_reply_to": 1, "pairs": [["hello",1],["world",1],["hello",1]] }

// Reduce a list of values用于one key
{ "type": "reduce", "msg_id": 2, "key": "hello", "values": [1,1,1] }
→ { "type": "reduce_result", "in_reply_to": 2, "result": ["hello", 3] }

// Execute a full word-count job over multiple lines
{ "type": "execute", "msg_id": 3, "lines": ["hello world", "hello mapreduce"] }
→ { "type": "job_result", "in_reply_to": 3, "results": {"hello":2,"world":1,"mapreduce":1} }
```

The execute flow: run map on every line → collect all pairs → group pairs by key → reduce each group → return the final counts.

## 涉及概念

- `MapReduce`
- `map phase`
- `reduce phase`
- `word count`
- `key-value pairs`
- `shuffle`

## 实现提示

- Map emits (word, 1)用于each word in the input line
- Reduce sums all values用于the same key
- execute runs map on each line, groups by key, then reduces
- Use a plain dict/map to accumulate counts during reduce
- Strip和lowercase words before emitting from map

## 测试用例

### 1. Map word to pairs

Should emit one (word, 1) pair per word token.

输入：

```json
{"src":"client","dest":"mapreduce","body":{"type":"map","msg_id":1,"line":"hello world hello"}}
```

期望输出：

```text
{"type": "map_result", "in_reply_to": 1, "pairs": [["hello", 1], ["world", 1], ["hello", 1]]}
```

### 2. Reduce word counts

Should sum all values用于the given key.

输入：

```json
{"src":"client","dest":"mapreduce","body":{"type":"reduce","msg_id":1,"key":"hello","values":[1,1,1]}}
```

期望输出：

```text
{"type": "reduce_result", "in_reply_to": 1, "result": ["hello", 3]}
```

## 参考资料

- [MapReduce: Simplified Data Processing on Large Clusters](https://research.google/pubs/pub62/)：The original Google MapReduce paper

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
