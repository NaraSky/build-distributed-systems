# 实现 MapReduce-Style Work Partitioning

英文标题：Implement MapReduce-Style Work Partitioning
网页：<https://builddistributedsystem.com/tracks/scheduler/tasks/task-22-2-2-work-partitioning>

课程：24. 调度器：任务调度
任务序号：7
短标题：Work Partitioning
难度：advanced
子主题：Distributed Work Allocation

## 中文导读

本题要求你完成 `实现 MapReduce-Style Work Partitioning`。

重点关注：`hash partitioning`、`range partitioning`、`data skew`、`straggler mitigation`、`speculative execution`。

建议先按提示逐步实现：Hash partitioning: partition_id = hash(job_id) % num_partitions — distributes evenly even用于skewed keys。

协议字段、消息类型、输入输出格式请以本文件中的代码块和测试用例为准。

## 题目说明

Large datasets are split into partitions so multiple workers can process them simultaneously. The partitioning strategy controls how evenly work is distributed, which directly affects total job time.

Implement a 节点 that partitions work和handles stragglers:

```JSON
// Split 1TB input evenly across 4 workers
{ "type": "submit_mapreduce", "msg_id": 1,
  "input": "s3://data/*.txt", "map": "wordcount", "num_partitions": 4 }
-> { "type": "job_submitted", "in_reply_to": 1,
    "job_id": "mr1",
    "partition_sizes": [256, 256, 256, 256], "workers": [1,2,3,4] }

// Hash beats range on skewed keys
{ "type": "benchmark_partitioning", "msg_id": 2,
  "strategies": ["range","hash"], "data": "keys_with_skew" }
-> results: range skew_factor=5.0, hash skew_factor=1.2

// Slow partition -> speculative execution on backup worker
{ "type": "submit_mapreduce", ...,
  "straggler_partition": 2, "straggler_slowdown": 5 }
-> { "type": "straggler_detected",
    "partition": 2, "action": "speculative_execution", "backup_worker": 5 }
```

## 涉及概念

- `hash partitioning`
- `range partitioning`
- `data skew`
- `straggler mitigation`
- `speculative execution`

## 实现提示

- Hash partitioning: partition_id = hash(job_id) % num_partitions — distributes evenly even用于skewed keys
- Skew factor = max_partition_size / avg_partition_size — closer to 1.0 means more balanced
- Range partitioning produces unequal partitions when key distribution is skewed
- A straggler is a partition whose runtime exceeds 2x the median of completed partitions
- Speculative execution: launch a backup copy on another worker和take whichever finishes first

## 测试用例

### 1. Partition input data

Input should be split into 4 equal partitions.

输入：

```json
{"src":"client","dest":"mr_cluster","body":{"type":"submit_mapreduce","msg_id":1,"input":"s3://data/*.txt","map":"wordcount","num_partitions":4}}
```

期望输出：

```text
{"src": "mr_cluster", "dest": "client", "body": {"type": "job_submitted", "in_reply_to": 1, "job_id": "mr1", "partition_sizes": [256, 256, 256, 256], "workers": [1,2,3,4]}}
```

### 2. Hash partitioning distribution

Hash should have much lower skew_factor than range on skewed data.

输入：

```json
{"src":"client","dest":"mr_cluster","body":{"type":"benchmark_partitioning","msg_id":1,"strategies":["range","hash"],"data":"keys_with_skew","num_partitions":4}}
```

期望输出：

```text
{"src": "mr_cluster", "dest": "client", "body": {"type": "benchmark_complete", "in_reply_to": 1, "results": {"range": {"skew_factor": 5.0}, "hash": {"skew_factor": 1.2}}}}
```

## 参考资料

- [MapReduce Paper](https://research.google/pubs/pub62/)：Original Google MapReduce paper covering partitioning和straggler mitigation

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
