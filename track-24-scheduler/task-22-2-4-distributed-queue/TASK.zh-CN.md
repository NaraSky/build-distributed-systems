# 实现分布式任务队列

英文标题：Implement Distributed Job Queue
网页：<https://builddistributedsystem.com/tracks/scheduler/tasks/task-22-2-4-distributed-queue>

课程：24. 任务调度器
任务序号：9
短标题：分布式队列
难度：高级
子主题：分布式任务分配

## 中文导读

这道题要求你实现一个分布式任务队列。单个消息代理既是性能瓶颈也是单点故障，一旦挂掉所有任务都没了。分布式队列把任务按分区分散到多个代理上，并对每个分区做副本复制，确保任何一个代理故障都不会丢失任务。这和 Kafka 等消息系统的设计思路一脉相承。

## 题目说明

只有一个代理（Broker）的任务队列存在两个致命问题：性能瓶颈和单点故障。分布式队列的解决方案是把任务按分区分散到多个代理上，并对每个分区进行副本复制。这样不仅分散了压力，还保证了任何一个代理发生故障都不会导致任务丢失。

你需要实现一个管理分区复制型任务队列的节点：

```json
// 初始化：3 个分区，每个分区复制到 2 个代理
{ "type": "init", "msg_id": 1,
  "partitions": 3, "replication_factor": 2 }
-> { "type": "init_ok", "in_reply_to": 1 }

// 推送任务 -- 按 hash(job_id) % 3 分配到各分区
{ "type": "push_job", "msg_id": 2,
  "jobs": [{"id":"j1"},{"id":"j2"},{"id":"j3"},
            {"id":"j4"},{"id":"j5"},{"id":"j6"}] }

// 工作节点从分配的分区中取出下一个任务
{ "type": "pop_job", "msg_id": 3,
  "consumer_id": "w1", "partitions": ["p1","p2","p3"] }
-> { "type": "job_assigned", "in_reply_to": 3,
    "job": {}, "partition": "p1" }

// 添加新代理 -> 重新平衡分区
{ "type": "rebalance_partitions", "msg_id": 4,
  "new_brokers": ["broker4","broker5"],
  "target_partitions_per_broker": 1 }
-> { "type": "rebalance_complete", "in_reply_to": 4,
    "migrations": [{"partition":"p2","from":"broker1","to":"broker4"}] }
```

分区再平衡（Rebalancing）是指在新增或移除代理时，将分区从负载过高的代理迁移到负载较低的代理，使各代理的负担尽可能均匀。副本因子为 2 表示每个分区有一个主副本和一个备份副本，主代理故障时备份副本自动提升为主节点，继续提供服务。

## 涉及概念

- partitioned queue
- replication
- consumer assignment
- partition rebalancing
- broker failover

## 实现提示

- 使用 `hash(job_id) % num_partitions` 将任务分配到各分区
- 每个消费者独占一个分区，同一时间只有一个消费者从一个分区中取任务
- 再平衡将分区从负载过高的代理迁移到负载较低的代理
- 当主代理故障时，副本被提升为主节点，继续提供服务，不会丢失任务
- 副本因子为 2 意味着每个分区有一个主副本和一个备份副本

## 测试用例

### 1. 任务按分区分布

任务应按 `hash(job_id) % 3` 分布到 3 个分区中。

输入：

```json
{"src":"producer","dest":"queue","body":{"type":"init","msg_id":1,"partitions":3,"replication_factor":2}}
{"src":"producer","dest":"queue","body":{"type":"push_job","msg_id":2,"jobs":[{"id":"j1"},{"id":"j2"},{"id":"j3"},{"id":"j4"},{"id":"j5"},{"id":"j6"}]}}
```

期望输出：

```text
{"src": "queue", "dest": "producer", "body": {"type": "init_ok", "in_reply_to": 1}}
```

### 2. 消费者从分区中拉取任务

工作节点应从第一个非空分区中获取一个任务。

输入：

```json
{"src":"worker","dest":"queue","body":{"type":"pop_job","msg_id":1,"consumer_id":"w1","partitions":["p1","p2","p3"]}}
```

期望输出：

```text
{"src": "queue", "dest": "worker", "body": {"type": "job_assigned", "in_reply_to": 1, "job": {}, "partition": "p1"}}
```

## 参考资料

- [Apache Kafka Design](https://kafka.apache.org/documentation/#design)：Kafka 的分区、复制和故障转移设计文档

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
