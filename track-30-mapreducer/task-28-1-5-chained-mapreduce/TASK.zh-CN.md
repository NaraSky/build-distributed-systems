# 实现 Chained MapReduce Pipeline

英文标题：Implement Chained MapReduce Pipeline
网页：<https://builddistributedsystem.com/tracks/mapreducer/tasks/task-28-1-5-chained-mapreduce>

课程：30. MapReducer：批处理与流处理
任务序号：5
短标题：Chained MapReduce
难度：advanced
子主题：MapReduce Fundamentals

## 中文导读

本题要求你完成 `实现 Chained MapReduce Pipeline`。

重点关注：`pipeline`、`job chaining`、`multi-stage processing`、`intermediate data`、`top-N`。

建议先按提示逐步实现：Run jobs in order: output of job[i] becomes input of job[i+1]。

协议字段、消息类型、输入输出格式请以本文件中的代码块和测试用例为准。

## 题目说明

Complex data analysis often needs multiple MapReduce stages. A chained pipeline feeds the output of one job directly as input to the next, keeping each job focused on a single transformation.

Example use-case: find the top 3 most frequent words across a document set.

```
Stage 1 (word count):  ["hello world", "hello there"]
                       → {"hello":2, "world":1, "there":1}

Stage 2 (sort by freq): {"hello":2, "world":1, "there":1}
                        → [["hello",2], ["world",1], ["there",1]]

Stage 3 (top N):        [["hello",2], ["world",1], ["there",1]], N=2
                        → [["hello",2], ["world",1]]
```

Your 节点 handles a single `pipeline` 消息 that runs all three stages和returns each stage's output:

```JSON
{ "type": "pipeline", "msg_id": 1,
  "lines": ["hello world", "hello there", "world peace"],
  "top_n": 2 }
→ { "type": "pipeline_result", "in_reply_to": 1,
    "stage1": {"hello":2,"world":2,"there":1,"peace":1},
    "stage2": [["hello",2],["world",2],["there",1],["peace",1]],
    "stage3": [["hello",2],["world",2]] }
```

When frequencies are equal (hello和world both 2), sort those keys alphabetically as a tiebreaker so the output is deterministic.

## 涉及概念

- `pipeline`
- `job chaining`
- `multi-stage processing`
- `intermediate data`
- `top-N`
- `secondary sort`

## 实现提示

- Run jobs in order: output of job[i] becomes input of job[i+1]
- Job 1 is a word count (map → reduce)
- Job 2 sorts the word-count results by frequency descending
- Job 3 takes the top N entries from the sorted list
- Return intermediate results用于each stage so the caller can inspect them

## 测试用例

### 1. Run full pipeline

Should run all three stages和return each stage output.

输入：

```json
{"src":"client","dest":"pipeline","body":{"type":"pipeline","msg_id":1,"lines":["hello world","hello there","world peace"],"top_n":2}}
```

期望输出：

```text
{"type": "pipeline_result", "in_reply_to": 1, "stage1": {"hello": 2, "world": 2, "there": 1, "peace": 1}, "stage2": [["hello", 2], ["world", 2], ["peace", 1], ["there", 1]], "stage3": [["hello", 2], ["world", 2]]}
```

### 2. Top 1 word

top_n=1 should return only the most frequent word.

输入：

```json
{"src":"client","dest":"pipeline","body":{"type":"pipeline","msg_id":1,"lines":["a b a","a c"],"top_n":1}}
```

期望输出：

```text
{"type": "pipeline_result", "in_reply_to": 1, "stage1": {"a": 3, "b": 1, "c": 1}, "stage2": [["a", 3], ["b", 1], ["c", 1]], "stage3": [["a", 3]]}
```

## 参考资料

- [Chaining MapReduce Jobs in Hadoop](https://hadoop.apache.org/docs/r3.3.1/hadoop-mapreduce-client/hadoop-mapreduce-client-core/MapReduceTutorial.html)：Multi-stage job chaining patterns

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
