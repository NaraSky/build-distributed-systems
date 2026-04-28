# 实现 MapReduce

英文标题：Implement MapReduce
网页：<https://builddistributedsystem.com/tracks/advanced/tasks/task-10-1-mapreduce>

课程：10. 高级主题
任务序号：1
短标题：MapReduce
难度：advanced
子主题：高级 Paradigms

## 中文导读

本题要求你完成 `实现 MapReduce`。

重点关注：`MapReduce`、`batch processing`、`word count`。

建议先按提示逐步实现：Map phase: emit key-value pairs。

协议字段、消息类型、输入输出格式请以本文件中的代码块和测试用例为准。

## 题目说明

Implement MapReduce: Map emits (key, value) pairs, shuffle groups by key, Reduce aggregates. Build word count as example.

## 概念说明

### MapReduce

MapReduce splits batch jobs into parallelizable map和reduce phases. Map transforms data, Reduce aggregates. Shuffle handles data movement between phases.

## 涉及概念

- `MapReduce`
- `batch processing`
- `word count`

## 实现提示

- Map phase: emit key-value pairs
- Shuffle: group by key
- Reduce phase: aggregate values

## 测试用例

### 1. Map emits 键值 pairs

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"mapreduce_map","msg_id":2,"data":["hello world","hello"],"mapper":"word_count"}}
```

期望输出：

```text
{"src":"n1","dest":"c0","body":{"type":"init_ok","in_reply_to":1,"msg_id":0}}
{"src":"n1","dest":"c1","body":{"type":"mapreduce_map_ok","in_reply_to":2,"msg_id":1,"mapped":[["hello",1],["world",1],["hello",1]]}}
```

## 参考资料

- [MapReduce Paper](https://research.google/pubs/pub62/)：Google MapReduce paper

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
