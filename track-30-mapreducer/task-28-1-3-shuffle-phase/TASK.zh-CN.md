# 实现 Shuffle Phase，包含Hash Partitioning

英文标题：Implement Shuffle Phase，包含Hash Partitioning
网页：<https://builddistributedsystem.com/tracks/mapreducer/tasks/task-28-1-3-shuffle-phase>

课程：30. MapReducer：批处理与流处理
任务序号：3
短标题：Shuffle Phase
难度：advanced
子主题：MapReduce Fundamentals

## 中文导读

本题要求你完成 `实现 Shuffle Phase，包含Hash Partitioning`。

重点关注：`shuffle phase`、`hash partitioning`、`key grouping`、`combiner`、`reduce assignment`。

建议先按提示逐步实现：Partition key: reducer_id = hash(key) % num_reducers。

协议字段、消息类型、输入输出格式请以本文件中的代码块和测试用例为准。

## 题目说明

After the map phase, all values用于the same key must reach the same reducer. The shuffle phase does exactly this: it **partitions** map outputs by key hash, **groups** values用于each key,和optionally **combines** them locally to reduce 网络 traffic.

Your 节点 handles three shuffle operations:

```JSON
// Partition pairs across N reducers使用hash(key) % N
{ "type": "partition", "msg_id": 1,
  "pairs": [["hello",1],["world",1],["hello",1]],
  "num_reducers": 2 }
→ { "type": "partitioned", "in_reply_to": 1,
    "partitions": [
      {"reducer_id": 0, "pairs": [["world",1]]},
      {"reducer_id": 1, "pairs": [["hello",2]]}
    ]}

// Group pairs by key (returns key → [values] map)
{ "type": "group", "msg_id": 2,
  "pairs": [["hello",1],["world",1],["hello",1]] }
→ { "type": "grouped", "in_reply_to": 2,
    "groups": {"hello": [1,1], "world": [1]} }

// Combine (local pre-reduce): sum values per key before sending over 网络
{ "type": "combine", "msg_id": 3,
  "pairs": [["hello",1],["world",1],["hello",1]] }
→ { "type": "combined", "in_reply_to": 3,
    "pairs": [["hello",2],["world",1]] }
```

For `partition`, after assigning pairs to reducer buckets, also group和sort keys alphabetically within each partition before returning.

## 涉及概念

- `shuffle phase`
- `hash partitioning`
- `key grouping`
- `combiner`
- `reduce assignment`

## 实现提示

- Partition key: reducer_id = hash(key) % num_reducers
- Use a simple string hash: sum of char codes, then abs() % num_reducers
- group collects all values用于the same key before reduce
- combine is a local pre-reduce: sum values用于the same key on the mapper side
- sort keys alphabetically within each partition

## 测试用例

### 1. Partition map outputs

Should assign pairs to reducers by hash(key) % num_reducers和aggregate within partition.

输入：

```json
{"src":"shuffler","dest":"partitioner","body":{"type":"partition","msg_id":1,"pairs":[["hello",1],["world",1],["hello",1]],"num_reducers":2}}
```

期望输出：

```text
{"type": "partitioned", "in_reply_to": 1, "partitions": [{"reducer_id": 0, "pairs": [["world", 1]]}, {"reducer_id": 1, "pairs": [["hello", 2]]}]}
```

### 2. Group by key

Should collect all values用于each key.

输入：

```json
{"src":"shuffler","dest":"grouper","body":{"type":"group","msg_id":1,"pairs":[["hello",1],["world",1],["hello",1]]}}
```

期望输出：

```text
{"type": "grouped", "in_reply_to": 1, "groups": {"hello": [1, 1], "world": [1]}}
```

## 参考资料

- [Hadoop MapReduce Tutorial](https://hadoop.apache.org/docs/r3.3.1/hadoop-mapreduce-client/hadoop-mapreduce-client-core/MapReduceTutorial.html)：Covers shuffle和sort in depth

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
