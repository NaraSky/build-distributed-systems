# 实现 Resource Estimation和Provisioning

英文标题：Implement Resource Estimation和Provisioning
网页：<https://builddistributedsystem.com/tracks/scheduler/tasks/task-22-1-5-resource-estimation>

课程：24. 调度器：任务调度
任务序号：5
短标题：Resource Estimation
难度：advanced
子主题：Centralized Job Scheduling

## 中文导读

本题要求你完成 `实现 Resource Estimation和Provisioning`。

重点关注：`resource estimation`、`bin packing`、`auto-scaling`、`historical analysis`、`packing efficiency`。

建议先按提示逐步实现：Historical estimation: average cpu, memory, duration from the last 10 jobs of the same type。

协议字段、消息类型、输入输出格式请以本文件中的代码块和测试用例为准。

## 题目说明

Before scheduling a job, the scheduler needs to know how many resources it requires. Good estimation averages historical data用于the same job type. Bin packing then places jobs on the fewest workers,和auto-scaling adjusts total capacity based on load.

Implement a 节点 that estimates resources, packs jobs,和makes scaling decisions:

```JSON
// Estimate from historical jobs of the same type
{ "type": "submit_job", "msg_id": 1,
  "job": {"id":"job1","type":"render_video","params":{"resolution":"1080p"}},
  "estimate_resources": true }
-> { "type": "job_submitted", "in_reply_to": 1,
    "estimated_resources": {"cpu":4,"memory":16,"duration_min":15},
    "historical_jobs_analyzed": 10 }

// Bin pack 3 jobs onto minimum workers (8cpu/32gb each)
{ "type": "submit_jobs", "msg_id": 2,
  "jobs": [{"id":"j1","cpu":4,"memory":16},
            {"id":"j2","cpu":2,"memory":8},
            {"id":"j3","cpu":4,"memory":16}],
  "worker_capacity": {"cpu":8,"memory":32} }
-> { "type": "jobs_scheduled", "in_reply_to": 2,
    "workers_provisioned": 2, "packing_efficiency": 0.75 }

// High 队列 depth -> scale up
{ "type": "check_scaling", "msg_id": 3,
  "queue_depth": 50, "avg_wait_time_ms": 300000, "workers": 5 }
-> { "type": "scaling_action", "action": "scale_up",
    "current_workers": 5, "new_workers": 10,
    "reason": "队列 depth > threshold" }
```

## 涉及概念

- `resource estimation`
- `bin packing`
- `auto-scaling`
- `historical analysis`
- `packing efficiency`

## 实现提示

- Historical estimation: average cpu, memory, duration from the last 10 jobs of the same type
- Bin packing: pack jobs onto the fewest workers without exceeding per-worker capacity
- packing_efficiency = sum(job_resources) / (workers_provisioned * worker_capacity)
- Scale up when queue_depth exceeds a threshold和average wait time is high
- Scale down when all worker utilizations are below 20%和队列 is empty

## 测试用例

### 1. Resource estimation from history

Should estimate resources by averaging similar historical jobs.

输入：

```json
{"src":"client","dest":"scheduler","body":{"type":"submit_job","msg_id":1,"job":{"id":"job1","type":"render_video","params":{"resolution":"1080p"}},"estimate_resources":true}}
```

期望输出：

```text
{"src": "scheduler", "dest": "client", "body": {"type": "job_submitted", "in_reply_to": 1, "estimated_resources": {"cpu": 4, "memory": 16, "duration_min": 15}, "historical_jobs_analyzed": 10}}
```

### 2. Bin packing efficiency

j1+j3 on worker1, j2 on worker2 = 2 workers, efficiency=0.75.

输入：

```json
{"src":"client","dest":"scheduler","body":{"type":"submit_jobs","msg_id":1,"jobs":[{"id":"j1","cpu":4,"memory":16},{"id":"j2","cpu":2,"memory":8},{"id":"j3","cpu":4,"memory":16}],"worker_capacity":{"cpu":8,"memory":32}}}
```

期望输出：

```text
{"src": "scheduler", "dest": "client", "body": {"type": "jobs_scheduled", "in_reply_to": 1, "workers_provisioned": 2, "packing_efficiency": 0.75}}
```

## 参考资料

- [Bin Packing Problem](https://en.wikipedia.org/wiki/Bin_packing_problem)：Packing items into fewest bins — NP-hard but good heuristics exist

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
