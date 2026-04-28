# 实现链式 MapReduce 流水线

英文标题：Implement Chained MapReduce Pipeline
网页：<https://builddistributedsystem.com/tracks/mapreducer/tasks/task-28-1-5-chained-mapreduce>

课程：30. MapReducer：批处理与流处理
任务序号：5
短标题：链式 MapReduce
难度：高级
子主题：MapReduce Fundamentals

## 中文导读

本题要求你实现一个多阶段链式 MapReduce 流水线。复杂的数据分析通常需要多轮 MapReduce 处理，前一轮的输出直接作为下一轮的输入。以"找出出现频率最高的前 N 个单词"为例，需要三个阶段：先做词频统计，再按频率排序，最后取前 N 个。这种流水线式的组合是大规模数据处理的常见模式。

## 题目说明

复杂的数据分析通常需要多个 MapReduce 阶段。链式流水线（Pipeline）将一个任务的输出直接作为下一个任务的输入，让每个任务专注于单一的数据转换。

应用场景示例：在一组文档中找出出现频率最高的前 3 个单词。

```
阶段 1（词频统计）: ["hello world", "hello there"]
                    -> {"hello":2, "world":1, "there":1}

阶段 2（按频率排序）: {"hello":2, "world":1, "there":1}
                     -> [["hello",2], ["world",1], ["there",1]]

阶段 3（取前 N 个）:  [["hello",2], ["world",1], ["there",1]], N=2
                     -> [["hello",2], ["world",1]]
```

你的节点处理一条 `pipeline` 消息，依次运行三个阶段并返回每个阶段的输出：

```json
{ "type": "pipeline", "msg_id": 1,
  "lines": ["hello world", "hello there", "world peace"],
  "top_n": 2 }
-> { "type": "pipeline_result", "in_reply_to": 1,
    "stage1": {"hello":2,"world":2,"there":1,"peace":1},
    "stage2": [["hello",2],["world",2],["there",1],["peace",1]],
    "stage3": [["hello",2],["world",2]] }
```

当频率相同时（例如 hello 和 world 都是 2），按键的字母顺序排序作为平局裁决规则，以确保输出是确定性的。

## 涉及概念

- `pipeline`
- `job chaining`
- `multi-stage processing`
- `intermediate data`
- `top-N`
- `secondary sort`

## 实现提示

- 按顺序运行各个任务：第 i 个任务的输出作为第 i+1 个任务的输入
- 任务 1 是词频统计（Map -> Reduce）
- 任务 2 按频率从高到低排序
- 任务 3 从排序后的列表中取前 N 个条目
- 返回每个阶段的中间结果，以便调用者进行检查

## 测试用例

### 1. 运行完整流水线

应运行全部三个阶段并返回每个阶段的输出。

输入：

```json
{"src":"client","dest":"pipeline","body":{"type":"pipeline","msg_id":1,"lines":["hello world","hello there","world peace"],"top_n":2}}
```

期望输出：

```text
{"type": "pipeline_result", "in_reply_to": 1, "stage1": {"hello": 2, "world": 2, "there": 1, "peace": 1}, "stage2": [["hello", 2], ["world", 2], ["peace", 1], ["there", 1]], "stage3": [["hello", 2], ["world", 2]]}
```

### 2. 取频率最高的 1 个单词

top_n=1 时应只返回出现频率最高的单词。

输入：

```json
{"src":"client","dest":"pipeline","body":{"type":"pipeline","msg_id":1,"lines":["a b a","a c"],"top_n":1}}
```

期望输出：

```text
{"type": "pipeline_result", "in_reply_to": 1, "stage1": {"a": 3, "b": 1, "c": 1}, "stage2": [["a", 3], ["b", 1], ["c", 1]], "stage3": [["a", 3]]}
```

## 参考资料

- [Chaining MapReduce Jobs in Hadoop](https://hadoop.apache.org/docs/r3.3.1/hadoop-mapreduce-client/hadoop-mapreduce-client-core/MapReduceTutorial.html)：多阶段任务链模式

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
