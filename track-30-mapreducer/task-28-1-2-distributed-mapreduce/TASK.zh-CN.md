# 实现 Distributed MapReduce

英文标题：Implement Distributed MapReduce
网页：<https://builddistributedsystem.com/tracks/mapreducer/tasks/task-28-1-2-distributed-mapreduce>

课程：30. MapReducer：批处理与流处理
任务序号：2
短标题：Distributed MapReduce
难度：advanced
子主题：MapReduce Fundamentals

## 中文导读

本题要求你完成 `实现 Distributed MapReduce`。

重点关注：`distributed MapReduce`、`worker nodes`、`job splitting`、`parallel processing`、`result merging`。

建议先按提示逐步实现：split divides the input array into equal-sized chunks, one per worker。

协议字段、消息类型、输入输出格式请以本文件中的代码块和测试用例为准。

## 题目说明

Single-machine MapReduce is limited by one CPU和one memory space. Distributed MapReduce sends different data chunks to different workers so all workers map in parallel, then the master merges和reduces.

Your 节点 plays the role of the **master**. It receives a `distribute` job 请求和must coordinate the workers listed in the 消息:

```JSON
// Master receives a distribute 请求
{ "type": "distribute", "msg_id": 1,
  "lines": ["hello world", "hello mapreduce", "world peace"],
  "workers": ["n2", "n3"] }

// Master splits lines evenly和sends to each worker
→ sends to n2: { "type": "map_chunk", "chunk": ["hello world", "hello mapreduce"] }
→ sends to n3: { "type": "map_chunk", "chunk": ["world peace"] }

// Workers reply，包含their map results
← n2: { "type": "chunk_result", "pairs": [["hello",1],["world",1],["hello",1],["mapreduce",1]] }
← n3: { "type": "chunk_result", "pairs": [["world",1],["peace",1]] }

// Master merges, reduces,和replies
→ { "type": "distribute_result", "in_reply_to": 1,
    "results": {"hello":2,"world":2,"mapreduce":1,"peace":1} }
```

Split the input into `len(workers)` chunks, forward each chunk, collect all pair lists, then run the same reduce logic from task 1 over the merged pairs.

## 涉及概念

- `distributed MapReduce`
- `worker nodes`
- `job splitting`
- `parallel processing`
- `result merging`

## 实现提示

- split divides the input array into equal-sized chunks, one per worker
- assign sends each chunk to a worker和waits用于its map result
- merge combines all worker outputs before the reduce phase
- The master coordinates workers; workers only map their assigned chunk
- Use worker count to decide chunk size: ceil(total / workers)

## 测试用例

### 1. Split input into chunks

Should split lines evenly into the requested number of chunks.

输入：

```json
{"src":"client","dest":"master","body":{"type":"split","msg_id":1,"lines":["a","b","c","d"],"num_chunks":2}}
```

期望输出：

```text
{"type": "split_result", "in_reply_to": 1, "chunks": [["a", "b"], ["c", "d"]]}
```

### 2. Merge worker results

Should merge和reduce all worker pair arrays.

输入：

```json
{"src":"client","dest":"master","body":{"type":"merge","msg_id":1,"worker_results":[[["hello",1],["world",1]],[["hello",1],["peace",1]]]}}
```

期望输出：

```text
{"type": "merge_result", "in_reply_to": 1, "results": {"hello": 2, "world": 1, "peace": 1}}
```

## 参考资料

- [MapReduce: Simplified Data Processing on Large Clusters](https://research.google/pubs/pub62/)：Original Google MapReduce paper

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
