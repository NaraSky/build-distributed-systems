# 实现洗牌阶段与哈希分区

英文标题：Implement Shuffle Phase with Hash Partitioning
网页：<https://builddistributedsystem.com/tracks/mapreducer/tasks/task-28-1-3-shuffle-phase>

课程：30. MapReducer：批处理与流处理
任务序号：3
短标题：洗牌阶段
难度：高级
子主题：MapReduce Fundamentals

## 中文导读

本题要求你实现 MapReduce 中的洗牌阶段（Shuffle Phase）。映射阶段完成后，相同键的所有值必须被送到同一个归约器去处理，洗牌阶段正是完成这个"归类分发"工作的。它通过哈希分区把映射输出分配到不同的归约器，按键分组，还可以在本地做预聚合以减少网络传输量。这是连接映射和归约两大阶段的关键桥梁。

## 题目说明

映射阶段完成后，所有相同键的值必须到达同一个归约器（Reducer）。洗牌阶段正是做这件事的：它通过键的哈希值对映射输出进行**分区**，将每个键的值**分组**，还可以选择性地在本地进行**合并**以减少网络传输量。

你的节点需要处理三种洗牌操作：

```json
// 使用 hash(key) % N 将键值对分配到 N 个归约器
{ "type": "partition", "msg_id": 1,
  "pairs": [["hello",1],["world",1],["hello",1]],
  "num_reducers": 2 }
-> { "type": "partitioned", "in_reply_to": 1,
    "partitions": [
      {"reducer_id": 0, "pairs": [["world",1]]},
      {"reducer_id": 1, "pairs": [["hello",2]]}
    ]}

// 按键分组（返回"键 -> 值列表"的映射）
{ "type": "group", "msg_id": 2,
  "pairs": [["hello",1],["world",1],["hello",1]] }
-> { "type": "grouped", "in_reply_to": 2,
    "groups": {"hello": [1,1], "world": [1]} }

// 合并（本地预归约）：在网络传输之前先对每个键的值求和
{ "type": "combine", "msg_id": 3,
  "pairs": [["hello",1],["world",1],["hello",1]] }
-> { "type": "combined", "in_reply_to": 3,
    "pairs": [["hello",2],["world",1]] }
```

对于分区操作，在将键值对分配到归约器桶之后，还需要在每个分区内按键的字母顺序进行分组和排序。

## 概念说明

洗牌阶段可以类比为邮件分拣。映射阶段产生了一堆"信件"（键值对），洗牌就是邮局的分拣过程。首先根据收件地址的哈希值决定每封信该送到哪个"投递站"（归约器），然后把寄给同一个人的信归到一起（分组），甚至可以在发出前先合并一些信息（合并器），以减少需要运送的总量。

## 涉及概念

- `shuffle phase`
- `hash partitioning`
- `key grouping`
- `combiner`
- `reduce assignment`

## 实现提示

- 分区键计算方式：reducer_id = hash(key) % num_reducers
- 使用简单的字符串哈希：所有字符编码之和，然后取绝对值再对归约器数量取模
- 分组操作在归约之前收集每个键的所有值
- 合并是本地预归约：在映射器端先对相同键的值求和
- 在每个分区内按键的字母顺序排序

## 测试用例

### 1. 对映射输出进行分区

应通过 hash(key) % num_reducers 将键值对分配给归约器，并在分区内进行聚合。

输入：

```json
{"src":"shuffler","dest":"partitioner","body":{"type":"partition","msg_id":1,"pairs":[["hello",1],["world",1],["hello",1]],"num_reducers":2}}
```

期望输出：

```text
{"type": "partitioned", "in_reply_to": 1, "partitions": [{"reducer_id": 0, "pairs": [["world", 1]]}, {"reducer_id": 1, "pairs": [["hello", 2]]}]}
```

### 2. 按键分组

应收集每个键对应的所有值。

输入：

```json
{"src":"shuffler","dest":"grouper","body":{"type":"group","msg_id":1,"pairs":[["hello",1],["world",1],["hello",1]]}}
```

期望输出：

```text
{"type": "grouped", "in_reply_to": 1, "groups": {"hello": [1, 1], "world": [1]}}
```

## 参考资料

- [Hadoop MapReduce Tutorial](https://hadoop.apache.org/docs/r3.3.1/hadoop-mapreduce-client/hadoop-mapreduce-client-core/MapReduceTutorial.html)：深入讲解洗牌和排序过程

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
