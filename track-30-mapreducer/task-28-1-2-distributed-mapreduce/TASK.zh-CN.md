# 实现分布式 MapReduce

英文标题：Implement Distributed MapReduce
网页：<https://builddistributedsystem.com/tracks/mapreducer/tasks/task-28-1-2-distributed-mapreduce>

课程：30. MapReducer：批处理与流处理
任务序号：2
短标题：分布式 MapReduce
难度：高级
子主题：MapReduce Fundamentals

## 中文导读

本题要求你实现分布式版本的 MapReduce。单机 MapReduce 受限于一台机器的 CPU 和内存，而分布式 MapReduce 把数据切分成多块，分发给多个工作节点并行处理，最后由主节点汇总结果。你扮演的是"主节点"的角色，负责任务分配和结果合并。这是理解大规模数据处理框架（如 Hadoop）的基础。

## 题目说明

单机 MapReduce 受限于一个 CPU 和一块内存空间。分布式 MapReduce 把不同的数据块发送给不同的工作节点（Worker），让所有工作节点并行执行 Map 操作，然后由主节点（Master）合并结果并执行 Reduce。

你的节点扮演**主节点**的角色。它接收一个 `distribute` 任务请求，并协调消息中列出的工作节点：

```json
// 主节点收到分发请求
{ "type": "distribute", "msg_id": 1,
  "lines": ["hello world", "hello mapreduce", "world peace"],
  "workers": ["n2", "n3"] }

// 主节点将数据均匀切分并发送给每个工作节点
-> 发送给 n2: { "type": "map_chunk", "chunk": ["hello world", "hello mapreduce"] }
-> 发送给 n3: { "type": "map_chunk", "chunk": ["world peace"] }

// 工作节点返回各自的 Map 结果
<- n2: { "type": "chunk_result", "pairs": [["hello",1],["world",1],["hello",1],["mapreduce",1]] }
<- n3: { "type": "chunk_result", "pairs": [["world",1],["peace",1]] }

// 主节点合并、归约后返回最终结果
-> { "type": "distribute_result", "in_reply_to": 1,
    "results": {"hello":2,"world":2,"mapreduce":1,"peace":1} }
```

将输入切分为 `len(workers)` 块，分发给各个工作节点，收集所有键值对列表，然后使用与上一题相同的 Reduce 逻辑处理合并后的键值对。

## 涉及概念

- `distributed MapReduce`
- `worker nodes`
- `job splitting`
- `parallel processing`
- `result merging`

## 实现提示

- 切分操作将输入数组均匀分成多块，每个工作节点一块
- 分配操作将每块数据发送给一个工作节点，并等待其返回 Map 结果
- 合并操作在 Reduce 阶段之前将所有工作节点的输出合并在一起
- 主节点负责协调工作节点；工作节点只对分配给自己的数据块执行 Map
- 根据工作节点数量决定分块大小：向上取整（总数 / 工作节点数）

## 测试用例

### 1. 将输入切分为数据块

应将输入行均匀切分为指定数量的数据块。

输入：

```json
{"src":"client","dest":"master","body":{"type":"split","msg_id":1,"lines":["a","b","c","d"],"num_chunks":2}}
```

期望输出：

```text
{"type": "split_result", "in_reply_to": 1, "chunks": [["a", "b"], ["c", "d"]]}
```

### 2. 合并工作节点结果

应合并并归约所有工作节点的键值对数组。

输入：

```json
{"src":"client","dest":"master","body":{"type":"merge","msg_id":1,"worker_results":[[["hello",1],["world",1]],[["hello",1],["peace",1]]]}}
```

期望输出：

```text
{"type": "merge_result", "in_reply_to": 1, "results": {"hello": 2, "world": 1, "peace": 1}}
```

## 参考资料

- [MapReduce: Simplified Data Processing on Large Clusters](https://research.google/pubs/pub62/)：Google MapReduce 的原始论文

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
