# 实现 MapReduce 风格的工作分区

英文标题：Implement MapReduce-Style Work Partitioning
网页：<https://builddistributedsystem.com/tracks/scheduler/tasks/task-22-2-2-work-partitioning>

课程：24. 任务调度器
任务序号：7
短标题：工作分区
难度：高级
子主题：分布式任务分配

## 中文导读

这道题要求你实现工作分区（Work Partitioning）机制：把大数据集切成若干分区，分配给多个工作节点并行处理。分区策略的好坏直接影响总耗时——分得不均匀就会出现"一个人干活、其他人等着"的窘境。你还需要处理"掉队者"问题，即某个分区特别慢时如何补救。

## 题目说明

大数据集需要拆分成多个分区（Partition），让多个工作节点同时处理。分区策略决定了工作是否均匀分配，这直接影响整个任务的完成时间。

你需要实现一个能进行工作分区并处理掉队者的节点：

```json
// 将 1TB 输入均匀分配给 4 个工作节点
{ "type": "submit_mapreduce", "msg_id": 1,
  "input": "s3://data/*.txt", "map": "wordcount", "num_partitions": 4 }
-> { "type": "job_submitted", "in_reply_to": 1,
    "job_id": "mr1",
    "partition_sizes": [256, 256, 256, 256], "workers": [1,2,3,4] }

// 哈希分区在数据倾斜时比范围分区更均匀
{ "type": "benchmark_partitioning", "msg_id": 2,
  "strategies": ["range","hash"], "data": "keys_with_skew" }
-> results: range skew_factor=5.0, hash skew_factor=1.2

// 慢分区 -> 在备用节点上启动推测执行
{ "type": "submit_mapreduce", ...,
  "straggler_partition": 2, "straggler_slowdown": 5 }
-> { "type": "straggler_detected",
    "partition": 2, "action": "speculative_execution", "backup_worker": 5 }
```

哈希分区（Hash Partitioning）通过对键取哈希再取模来分配数据，即使键的分布不均匀，也能得到比较均匀的分区。范围分区（Range Partitioning）按键的范围划分，在数据倾斜（Data Skew）时容易产生大小悬殊的分区。当某个分区的执行时间远超其他分区时，它就是一个"掉队者"（Straggler），可以通过推测执行（Speculative Execution）在另一个节点上启动一份备份，谁先完成就用谁的结果。

## 涉及概念

- hash partitioning
- range partitioning
- data skew
- straggler mitigation
- speculative execution

## 实现提示

- 哈希分区：`partition_id = hash(job_id) % num_partitions`，即使键分布不均也能均匀分配
- 倾斜因子 = 最大分区大小 / 平均分区大小，越接近 1.0 表示越均衡
- 当键的分布不均匀时，范围分区会产生大小不等的分区
- 掉队者是指运行时间超过已完成分区中位数 2 倍的分区
- 推测执行：在另一个工作节点上启动一份备份副本，谁先完成就用谁的结果

## 测试用例

### 1. 数据分区

输入数据应被均匀切分为 4 个分区。

输入：

```json
{"src":"client","dest":"mr_cluster","body":{"type":"submit_mapreduce","msg_id":1,"input":"s3://data/*.txt","map":"wordcount","num_partitions":4}}
```

期望输出：

```text
{"src": "mr_cluster", "dest": "client", "body": {"type": "job_submitted", "in_reply_to": 1, "job_id": "mr1", "partition_sizes": [256, 256, 256, 256], "workers": [1,2,3,4]}}
```

### 2. 哈希分区的分布效果

在数据倾斜的情况下，哈希分区的倾斜因子应远低于范围分区。

输入：

```json
{"src":"client","dest":"mr_cluster","body":{"type":"benchmark_partitioning","msg_id":1,"strategies":["range","hash"],"data":"keys_with_skew","num_partitions":4}}
```

期望输出：

```text
{"src": "mr_cluster", "dest": "client", "body": {"type": "benchmark_complete", "in_reply_to": 1, "results": {"range": {"skew_factor": 5.0}, "hash": {"skew_factor": 1.2}}}}
```

## 参考资料

- [MapReduce Paper](https://research.google/pubs/pub62/)：Google 原始 MapReduce 论文，涵盖了分区和掉队者处理策略

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
