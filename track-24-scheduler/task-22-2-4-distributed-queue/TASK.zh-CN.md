# 实现 Distributed Job 队列

英文标题：Implement Distributed Job Queue
网页：<https://builddistributedsystem.com/tracks/scheduler/tasks/task-22-2-4-distributed-queue>

课程：24. 调度器：任务调度
任务序号：9
短标题：Distributed 队列
难度：advanced
子主题：Distributed Work Allocation

## 中文导读

本题要求你完成 `实现 Distributed Job 队列`。

重点关注：`partitioned queue`、`replication`、`consumer assignment`、`partition rebalancing`、`broker failover`。

建议先按提示逐步实现：Assign jobs to partitions使用hash(job_id) % num_partitions。

协议字段、消息类型、输入输出格式请以本文件中的代码块和测试用例为准。

## 题目说明

A single-broker job 队列 is both a bottleneck和a single point of 故障. A distributed 队列 partitions jobs across multiple brokers和replicates each partition so no broker 故障 loses any jobs.

Implement a 节点 that manages a partitioned, replicated job 队列:

```JSON
// Initialize: 3 partitions, replicated to 2 brokers each
{ "type": "init", "msg_id": 1,
  "partitions": 3, "replication_factor": 2 }
-> { "type": "init_ok", "in_reply_to": 1 }

// Push jobs — assigned to partitions by hash(job_id) % 3
{ "type": "push_job", "msg_id": 2,
  "jobs": [{"id":"j1"},{"id":"j2"},{"id":"j3"},
            {"id":"j4"},{"id":"j5"},{"id":"j6"}] }

// Worker pops next job from its assigned partition
{ "type": "pop_job", "msg_id": 3,
  "consumer_id": "w1", "partitions": ["p1","p2","p3"] }
-> { "type": "job_assigned", "in_reply_to": 3,
    "job": {}, "partition": "p1" }

// Add new brokers -> rebalance partitions
{ "type": "rebalance_partitions", "msg_id": 4,
  "new_brokers": ["broker4","broker5"],
  "target_partitions_per_broker": 1 }
-> { "type": "rebalance_complete", "in_reply_to": 4,
    "migrations": [{"partition":"p2","from":"broker1","to":"broker4"}] }
```

## 涉及概念

- `partitioned queue`
- `replication`
- `consumer assignment`
- `partition rebalancing`
- `broker failover`

## 实现提示

- Assign jobs to partitions使用hash(job_id) % num_partitions
- A consumer owns a partition exclusively; only one consumer pops from a partition at a time
- Rebalancing moves partitions from over-loaded brokers to under-loaded ones
- On primary broker 故障, a replica promotes to primary和resumes serving without job loss
- 复制 factor=2 means every partition has one primary和one replica

## 测试用例

### 1. Partition job distribution

Jobs should be distributed across 3 partitions by hash(job_id) % 3.

输入：

```json
{"src":"producer","dest":"queue","body":{"type":"init","msg_id":1,"partitions":3,"replication_factor":2}}
{"src":"producer","dest":"queue","body":{"type":"push_job","msg_id":2,"jobs":[{"id":"j1"},{"id":"j2"},{"id":"j3"},{"id":"j4"},{"id":"j5"},{"id":"j6"}]}}
```

期望输出：

```text
{"src": "queue", "dest": "producer", "body": {"type": "init_ok", "in_reply_to": 1}}
```

### 2. Consumer pulls from partitions

Worker should receive one job from the first non-empty partition.

输入：

```json
{"src":"worker","dest":"queue","body":{"type":"pop_job","msg_id":1,"consumer_id":"w1","partitions":["p1","p2","p3"]}}
```

期望输出：

```text
{"src": "queue", "dest": "worker", "body": {"type": "job_assigned", "in_reply_to": 1, "job": {}, "partition": "p1"}}
```

## 参考资料

- [Apache Kafka Design](https://kafka.apache.org/documentation/#design)：How Kafka partitions, replicates,和handles failover

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
