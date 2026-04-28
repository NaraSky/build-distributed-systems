# 实现单机 MapReduce

英文标题：Implement Single-Machine MapReduce
网页：<https://builddistributedsystem.com/tracks/mapreducer/tasks/task-28-1-1-mapreduce-basics>

课程：30. MapReducer：批处理与流处理
任务序号：1
短标题：MapReduce 基础
难度：进阶
子主题：MapReduce Fundamentals

## 中文导读

本题要求你在单机上实现经典的 MapReduce 计算模型。MapReduce 的思想非常直观：先把一个大任务"拆开"（Map 阶段），再把拆开后的结果"合起来"（Reduce 阶段）。以词频统计为例，Map 阶段把每一行文本拆成一个个单词计数对，Reduce 阶段再把相同单词的计数加总。掌握这个基础模型，才能理解后续的分布式和流处理扩展。

## 题目说明

MapReduce 将工作分为两个简单的阶段：**Map** 阶段将每条输入记录转换为键值对，**Reduce** 阶段将相同键的所有值进行聚合。

你的节点需要处理三种消息类型：

```json
// 将一行文本映射为单词计数对
{ "type": "map", "msg_id": 1, "line": "hello world hello" }
-> { "type": "map_result", "in_reply_to": 1, "pairs": [["hello",1],["world",1],["hello",1]] }

// 对一个键的所有值进行归约
{ "type": "reduce", "msg_id": 2, "key": "hello", "values": [1,1,1] }
-> { "type": "reduce_result", "in_reply_to": 2, "result": ["hello", 3] }

// 执行一个完整的词频统计任务（包含多行文本）
{ "type": "execute", "msg_id": 3, "lines": ["hello world", "hello mapreduce"] }
-> { "type": "job_result", "in_reply_to": 3, "results": {"hello":2,"world":1,"mapreduce":1} }
```

execute 的完整流程是：对每一行执行 Map -> 收集所有键值对 -> 按键分组 -> 对每组执行 Reduce -> 返回最终统计结果。

## 概念说明

你可以把 MapReduce 想象成一群人一起数一摞文件中某些词出现的次数。Map 阶段就是把文件分给每个人，每人各自标记"这个词出现了一次"。Reduce 阶段就是把大家标记的结果按词汇汇总，加在一起得到总数。

## 涉及概念

- `MapReduce`
- `map phase`
- `reduce phase`
- `word count`
- `key-value pairs`
- `shuffle`

## 实现提示

- Map 阶段为输入行中的每个单词发出一个 (单词, 1) 对
- Reduce 阶段对同一个键的所有值求和
- execute 先对每行执行 Map，再按键分组，最后执行 Reduce
- 使用普通的字典或映射来在 Reduce 过程中累加计数
- 在 Map 发出结果前，对单词进行去空格和转小写处理

## 测试用例

### 1. 将单词映射为键值对

应为每个单词发出一个 (单词, 1) 对。

输入：

```json
{"src":"client","dest":"mapreduce","body":{"type":"map","msg_id":1,"line":"hello world hello"}}
```

期望输出：

```text
{"type": "map_result", "in_reply_to": 1, "pairs": [["hello", 1], ["world", 1], ["hello", 1]]}
```

### 2. 归约单词计数

应对给定键的所有值求和。

输入：

```json
{"src":"client","dest":"mapreduce","body":{"type":"reduce","msg_id":1,"key":"hello","values":[1,1,1]}}
```

期望输出：

```text
{"type": "reduce_result", "in_reply_to": 1, "result": ["hello", 3]}
```

## 参考资料

- [MapReduce: Simplified Data Processing on Large Clusters](https://research.google/pubs/pub62/)：Google MapReduce 的原始论文

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
