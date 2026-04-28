# 实现资源估算与自动扩缩容

英文标题：Implement Resource Estimation and Provisioning
网页：<https://builddistributedsystem.com/tracks/scheduler/tasks/task-22-1-5-resource-estimation>

课程：24. 任务调度器
任务序号：5
短标题：资源估算
难度：高级
子主题：集中式任务调度

## 中文导读

这道题要求你实现资源估算（Resource Estimation）、装箱打包（Bin Packing）和自动扩缩容。在调度任务之前，需要先预估它需要多少资源，然后把任务尽可能紧凑地安排到最少的机器上，并根据负载动态调整机器数量。这三步是高效利用计算资源的关键。

## 题目说明

在调度任务之前，调度器需要知道任务需要多少资源。好的估算方法是对同类型历史任务的数据取平均值。装箱打包（Bin Packing）将任务放到尽可能少的工作节点上，自动扩缩容则根据负载调整总容量。

实现一个能进行资源估算、任务打包和扩缩容决策的节点：

```json
// 根据同类型历史任务进行资源估算
{ "type": "submit_job", "msg_id": 1,
  "job": {"id":"job1","type":"render_video","params":{"resolution":"1080p"}},
  "estimate_resources": true }
-> { "type": "job_submitted", "in_reply_to": 1,
    "estimated_resources": {"cpu":4,"memory":16,"duration_min":15},
    "historical_jobs_analyzed": 10 }

// 将 3 个任务装箱到最少的工作节点上（每个节点 8核/32GB）
{ "type": "submit_jobs", "msg_id": 2,
  "jobs": [{"id":"j1","cpu":4,"memory":16},
            {"id":"j2","cpu":2,"memory":8},
            {"id":"j3","cpu":4,"memory":16}],
  "worker_capacity": {"cpu":8,"memory":32} }
-> { "type": "jobs_scheduled", "in_reply_to": 2,
    "workers_provisioned": 2, "packing_efficiency": 0.75 }

// 队列深度过大 -> 扩容
{ "type": "check_scaling", "msg_id": 3,
  "queue_depth": 50, "avg_wait_time_ms": 300000, "workers": 5 }
-> { "type": "scaling_action", "action": "scale_up",
    "current_workers": 5, "new_workers": 10,
    "reason": "Queue depth > threshold" }
```

## 涉及概念

- resource estimation
- bin packing
- auto-scaling
- historical analysis
- packing efficiency

## 实现提示

- 历史估算：取同类型最近 10 个任务的平均 CPU、内存和耗时
- 装箱打包：将任务放到尽可能少的工作节点上，但不超过每个节点的容量上限
- 打包效率 = 所有任务的资源总和 / (使用的工作节点数 * 单节点容量)
- 当队列深度超过阈值且平均等待时间过长时，进行扩容
- 当所有工作节点利用率低于 20% 且队列为空时，进行缩容

## 测试用例

### 1. 基于历史数据的资源估算

应通过对同类型历史任务取平均值来估算资源。

输入：

```json
{"src":"client","dest":"scheduler","body":{"type":"submit_job","msg_id":1,"job":{"id":"job1","type":"render_video","params":{"resolution":"1080p"}},"estimate_resources":true}}
```

期望输出：

```text
{"src": "scheduler", "dest": "client", "body": {"type": "job_submitted", "in_reply_to": 1, "estimated_resources": {"cpu": 4, "memory": 16, "duration_min": 15}, "historical_jobs_analyzed": 10}}
```

### 2. 装箱打包效率

j1 和 j3 放在 worker1，j2 放在 worker2，共需 2 个工作节点，打包效率为 0.75。

输入：

```json
{"src":"client","dest":"scheduler","body":{"type":"submit_jobs","msg_id":1,"jobs":[{"id":"j1","cpu":4,"memory":16},{"id":"j2","cpu":2,"memory":8},{"id":"j3","cpu":4,"memory":16}],"worker_capacity":{"cpu":8,"memory":32}}}
```

期望输出：

```text
{"src": "scheduler", "dest": "client", "body": {"type": "jobs_scheduled", "in_reply_to": 1, "workers_provisioned": 2, "packing_efficiency": 0.75}}
```

## 参考资料

- [Bin Packing Problem](https://en.wikipedia.org/wiki/Bin_packing_problem)：将物品装入最少箱子的经典问题，虽然是 NP 难问题，但有很好的启发式算法

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
