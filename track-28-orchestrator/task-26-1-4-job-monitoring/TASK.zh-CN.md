# 实现 Job Monitoring和Observability

英文标题：Implement Job Monitoring和Observability
网页：<https://builddistributedsystem.com/tracks/orchestrator/tasks/task-26-1-4-job-monitoring>

课程：28. 编排器：容器调度与服务网格
任务序号：4
短标题：Job Monitoring
难度：intermediate
子主题：Scheduling

## 中文导读

本题要求你完成 `实现 Job Monitoring和Observability`。

重点关注：`job monitoring`、`status tracking`、`alerting`、`metrics aggregation`、`observability`。

建议先按提示逐步实现：update_status stores the current status和progress (0-100)用于a job_id。

协议字段、消息类型、输入输出格式请以本文件中的代码块和测试用例为准。

## 题目说明

Job monitoring gives operators visibility into what is running, how long it takes,和when things go wrong. Without it, a failed job can go undetected用于hours.

Implement a 节点 that tracks job lifecycle events和exposes aggregate statistics:

```JSON
// Record a status update，包含progress percentage
{ "type": "update_status", "msg_id": 1,
  "job_id": "job-123", "status": "running", "progress": 25 }
-> { "type": "status_updated", "in_reply_to": 1,
    "job_id": "job-123", "status": "running", "progress": 25 }

// Record completion，包含timing和resource metrics
{ "type": "job_completed", "msg_id": 2,
  "job_id": "job-123", "duration_ms": 60000,
  "resource_usage": {"cpu_percent": 75, "memory_mb": 1024} }
-> { "type": "job_completed", "in_reply_to": 2,
    "job_id": "job-123", "duration_ms": 60000,
    "resource_usage": {"cpu_percent": 75, "memory_mb": 1024} }

// Job fails after max retries -> send an alert
{ "type": "job_failed", "msg_id": 3,
  "job_id": "job-123", "error": "Connection 超时", "retries": 3 }
-> { "type": "alert_sent", "in_reply_to": 3,
    "job_id": "job-123",
    "alert": "Job failed after 3 retries: Connection 超时" }

// Aggregate statistics across all tracked jobs
{ "type": "get_stats", "msg_id": 4 }
-> { "type": "job_stats", "in_reply_to": 4,
    "total": 100, "completed": 85, "failed": 5, "avg_duration_ms": 5000 }
```

## 涉及概念

- `job monitoring`
- `status tracking`
- `alerting`
- `metrics aggregation`
- `observability`

## 实现提示

- update_status stores the current status和progress (0-100)用于a job_id
- job_completed records duration_ms和resource_usage alongside the job record
- Fire an alert only when a job fails after exhausting all retries
- get_stats aggregates totals across all jobs: count by status和average duration_ms
- Progress is a percentage 0-100 representing how far through execution the job is

## 测试用例

### 1. Track job status updates

Should record和acknowledge job status和progress.

输入：

```json
{"src":"worker","dest":"monitor","body":{"type":"update_status","msg_id":1,"job_id":"job-123","status":"running","progress":25}}
```

期望输出：

```text
{"type": "status_updated", "in_reply_to": 1, "job_id": "job-123", "status": "running", "progress": 25}
```

### 2. Record job completion，包含metrics

Should record duration和resource usage.

输入：

```json
{"src":"worker","dest":"monitor","body":{"type":"job_completed","msg_id":1,"job_id":"job-123","duration_ms":60000,"resource_usage":{"cpu_percent":75,"memory_mb":1024}}}
```

期望输出：

```text
{"type": "job_completed", "in_reply_to": 1, "job_id": "job-123", "duration_ms": 60000, "resource_usage": {"cpu_percent": 75, "memory_mb": 1024}}
```

## 参考资料

- [The Four Golden Signals](https://sre.google/sre-book/monitoring-distributed-systems/)：Google SRE guide on monitoring: latency, traffic, errors, saturation

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
