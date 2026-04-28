# 实现集中式任务调度器

英文标题：Implement Centralized Job Scheduler
网页：<https://builddistributedsystem.com/tracks/scheduler/tasks/task-22-1-1-centralized-scheduler>

课程：24. 任务调度器
任务序号：1
短标题：集中式调度器
难度：进阶
子主题：集中式任务调度

## 中文导读

这道题要求你实现一个集中式任务调度器（Centralized Scheduler），它是整个系统中唯一负责接收任务、排优先级、分配给工作节点的"指挥中心"。当工作节点故障时，调度器还要负责重新分配任务。这是理解分布式调度的起点。

## 题目说明

集中式调度器是系统中唯一的调度权威，负责接收所有任务提交、维护一个优先队列（Priority Queue），并将任务分派给空闲的工作节点。当某个工作节点故障时，调度器会将其上的任务重新分配，而客户端无感知。

实现一个充当中心调度器的节点：

```json
// 初始化，传入可用的工作节点列表
{ "type": "init", "msg_id": 1,
  "workers": ["worker-1", "worker-2", "worker-3"] }
-> { "type": "init_ok", "in_reply_to": 1 }

// 提交一个任务；优先级越高越先执行
{ "type": "submit_job", "msg_id": 2,
  "job": {"id": "job1", "priority": 10, "type": "process_data"} }
-> [分配给一个空闲的工作节点]

// 三个任务：优先级 20 先于 10 先于 1
{ "type": "submit_job", ..., "job": {"id": "high_job", "priority": 20} }
-> { "type": "job_submitted", "job_id": "high_job" }

// 工作节点崩溃 -> 调度器重新分配其任务
{ "type": "worker_failed", "worker_id": "worker-1" }
-> { "type": "job_reassigned",
    "job_id": "job1", "old_worker": "worker-1", "new_worker": "worker-2" }

// 查看当前队列状态
{ "type": "get_queue_status", "msg_id": 1 }
-> { "type": "queue_status_ok", "in_reply_to": 1,
    "pending_jobs": 5, "running_jobs": 3, "workers_available": 2 }
```

## 涉及概念

- priority queue
- worker assignment
- job dispatch
- failure handling
- queue status

## 实现提示

- 使用最大堆维护待处理任务，优先级数字越大越先执行
- 收到 `submit_job` 时，如果有空闲工作节点就立即分配；否则放入队列
- 收到 `worker_failed` 时，找到该工作节点上正在运行的所有任务，重新分配给其他节点
- `get_queue_status` 分别统计待处理（已排队但未分配）和运行中（已分配）的任务数
- 维护一个"工作节点到任务"的映射，以便在故障时快速重新分配

## 测试用例

### 1. 提交并调度任务

任务应被提交并分配给一个空闲的工作节点。

输入：

```json
{"src":"client","dest":"scheduler","body":{"type":"init","msg_id":1,"workers":["worker-1","worker-2","worker-3"]}}
{"src":"client","dest":"scheduler","body":{"type":"submit_job","msg_id":2,"job":{"id":"job1","type":"process_data","priority":10,"params":{"data":"abc"}}}}
```

期望输出：

```text
{"src": "scheduler", "dest": "client", "body": {"type": "init_ok", "in_reply_to": 1}}
```

### 2. 按优先级调度

优先级为 20 的 `high_job` 应最先被调度。

输入：

```json
{"src":"client","dest":"scheduler","body":{"type":"submit_job","msg_id":1,"job":{"id":"low_job","priority":1}}}
{"src":"client","dest":"scheduler","body":{"type":"submit_job","msg_id":2,"job":{"id":"high_job","priority":20}}}
{"src":"client","dest":"scheduler","body":{"type":"submit_job","msg_id":3,"job":{"id":"med_job","priority":10}}}
```

期望输出：

```text
{"src": "scheduler", "dest": "client", "body": {"type": "job_submitted", "in_reply_to": 2, "job_id": "high_job"}}
```

## 参考资料

- [Job Scheduling Algorithms](https://en.wikipedia.org/wiki/Job-shop_scheduling)：任务调度方法概述

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
