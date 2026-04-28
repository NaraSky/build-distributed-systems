# 实现 MapReduce 框架

网页：<https://builddistributedsystem.com/tracks/advanced/tasks/task-10-1-mapreduce>

课程：10. 高级主题
任务序号：1
短标题：MapReduce
难度：高级
子主题：高级范式

## 中文导读

MapReduce 是谷歌提出的大数据处理经典模型，也是理解分布式批处理的起点。它的核心思想可以用一句话概括：先分头干活，再汇总结果。

这道题让你以单词计数为例，实现一个简易的 MapReduce 框架。你将亲手体验数据如何经过"映射、洗牌、归约"三个阶段被处理，理解为什么这种模式能够轻松扩展到海量数据。

## 题目说明

实现一个 MapReduce 框架，包含三个阶段：

1. **映射阶段（Map）**：将输入数据转换为一系列键值对。比如，对一行文本做单词计数时，每遇到一个单词就输出 `[单词, 1]` 这样的键值对。
2. **洗牌阶段（Shuffle）**：把映射阶段产生的所有键值对按键分组。比如，把所有 `["hello", 1]` 归到一组。
3. **归约阶段（Reduce）**：对每组键值对进行聚合。比如，把同一个单词对应的所有 1 加起来，得到这个单词的总出现次数。

你可以把这个过程想象成一个大型考试的批改流程：先让每个老师各自批改一部分试卷并记录分数（映射），然后按学生姓名把各科分数归拢到一起（洗牌），最后汇总每个学生的总分（归约）。

## 概念说明

### MapReduce

MapReduce 把大规模的批处理任务拆分成可以并行执行的映射和归约两个阶段。映射阶段负责数据转换，归约阶段负责汇总聚合。中间的洗牌阶段负责按键对数据进行分组和搬运。这种分而治之的思路使得处理能力可以随机器数量线性扩展。

## 涉及概念

- `MapReduce`
- `batch processing`
- `word count`

## 实现提示

- 映射阶段：遍历输入数据，为每个元素生成键值对
- 洗牌阶段：将所有键值对按键分组
- 归约阶段：对每组中的值进行聚合运算

## 测试用例

### 1. 映射阶段正确输出键值对

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

- [MapReduce Paper](https://research.google/pubs/pub62/)：谷歌发表的 MapReduce 原始论文，奠定了大规模数据处理的基础范式

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
