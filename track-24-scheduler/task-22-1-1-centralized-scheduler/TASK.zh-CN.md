# 实现 Centralized Job 调度器

英文标题：Implement Centralized Job Scheduler
网页：<https://builddistributedsystem.com/tracks/scheduler/tasks/task-22-1-1-centralized-scheduler>

课程：24. 调度器：任务调度
任务序号：1
短标题：Centralized 调度器
难度：intermediate
子主题：Centralized Job Scheduling

## 中文导读

本题要求你完成 `实现 Centralized Job 调度器`。

重点关注：`priority queue`、`worker assignment`、`job dispatch`、`failure handling`、`queue status`。

建议先按提示逐步实现：Maintain a max-heap of pending jobs; higher priority number = runs first。

协议字段、消息类型、输入输出格式请以本文件中的代码块和测试用例为准。

## 题目说明

A centralized scheduler is the single authority that receives all job submissions, maintains a priority 队列,和dispatches work to available workers. When a worker fails, it reassigns its jobs without the 客户端 noticing.

Implement a 节点 that acts as the central scheduler:

```JSON
// Initialize，包含available workers
{ "type": "init", "msg_id": 1,
  "workers": ["worker-1", "worker-2", "worker-3"] }
-> { "type": "init_ok", "in_reply_to": 1 }

// Submit a job; higher priority runs first
{ "type": "submit_job", "msg_id": 2,
  "job": {"id": "job1", "priority": 10, "type": "process_data"} }
-> [assigned to an available worker]

// Three jobs: priority 20 runs before 10 before 1
{ "type": "submit_job", ..., "job": {"id": "high_job", "priority": 20} }
-> { "type": "job_submitted", "job_id": "high_job" }

// Worker crashes -> scheduler reassigns its jobs
{ "type": "worker_failed", "worker_id": "worker-1" }
-> { "type": "job_reassigned",
    "job_id": "job1", "old_worker": "worker-1", "new_worker": "worker-2" }

// Inspect current 队列 state
{ "type": "get_queue_status", "msg_id": 1 }
-> { "type": "queue_status_ok", "in_reply_to": 1,
    "pending_jobs": 5, "running_jobs": 3, "workers_available": 2 }
```

## 涉及概念

- `priority queue`
- `worker assignment`
- `job dispatch`
- `failure handling`
- `queue status`

## 实现提示

- Maintain a max-heap of pending jobs; higher priority number = runs first
- On submit_job, assign immediately if a worker is free; otherwise enqueue
- On worker_failed, find all jobs running on that worker和reassign to another
- get_queue_status counts pending (queued but not assigned) vs running (assigned) separately
- Track a worker -> job mapping so you can reassign on 故障

## 测试用例

### 1. Submit和schedule job

Job should be submitted和assigned to an available worker.

输入：

```json
{"src":"client","dest":"scheduler","body":{"type":"init","msg_id":1,"workers":["worker-1","worker-2","worker-3"]}}
{"src":"client","dest":"scheduler","body":{"type":"submit_job","msg_id":2,"job":{"id":"job1","type":"process_data","priority":10,"params":{"data":"abc"}}}}
```

期望输出：

```text
{"src": "scheduler", "dest": "client", "body": {"type": "init_ok", "in_reply_to": 1}}
```

### 2. Priority scheduling order

high_job (priority 20) should be scheduled first.

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

- [Job Scheduling Algorithms](https://en.wikipedia.org/wiki/Job-shop_scheduling)：Overview of job scheduling approaches

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
