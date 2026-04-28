# 实现任务监控与可观测性

英文标题：Implement Job Monitoring and Observability
网页：<https://builddistributedsystem.com/tracks/orchestrator/tasks/task-26-1-4-job-monitoring>

课程：28. 编排器：容器调度与服务网格
任务序号：4
短标题：Job Monitoring
难度：进阶
子主题：Scheduling

## 中文导读

这道题要求你实现一个任务监控节点，用于追踪任务的生命周期事件并提供汇总统计。没有监控的话，一个失败的任务可能几个小时都不会被发现。任务监控让运维人员能看到哪些任务在运行、运行了多久、什么时候出了问题，并在关键失败时发出告警。这是保障系统可靠运行的基本能力。

## 题目说明

任务监控让运维人员能够了解哪些任务正在运行、运行了多久、什么时候出了问题。没有监控的话，一个失败的任务可能几个小时都无人察觉。

请实现一个追踪任务生命周期事件并提供汇总统计的节点：

```json
// 记录带进度百分比的状态更新
{ "type": "update_status", "msg_id": 1,
  "job_id": "job-123", "status": "running", "progress": 25 }
-> { "type": "status_updated", "in_reply_to": 1,
    "job_id": "job-123", "status": "running", "progress": 25 }

// 记录任务完成，包含耗时和资源使用情况
{ "type": "job_completed", "msg_id": 2,
  "job_id": "job-123", "duration_ms": 60000,
  "resource_usage": {"cpu_percent": 75, "memory_mb": 1024} }
-> { "type": "job_completed", "in_reply_to": 2,
    "job_id": "job-123", "duration_ms": 60000,
    "resource_usage": {"cpu_percent": 75, "memory_mb": 1024} }

// 任务在最大重试次数后仍然失败 -> 发送告警
{ "type": "job_failed", "msg_id": 3,
  "job_id": "job-123", "error": "Connection timeout", "retries": 3 }
-> { "type": "alert_sent", "in_reply_to": 3,
    "job_id": "job-123",
    "alert": "Job failed after 3 retries: Connection timeout" }

// 汇总所有被追踪任务的统计数据
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

- `update_status` 存储某个任务的当前状态和进度（0-100）
- `job_completed` 记录任务的执行耗时和资源使用情况
- 仅在任务耗尽所有重试次数后仍然失败时才触发告警
- `get_stats` 汇总所有任务的统计数据：按状态计数和平均耗时
- 进度是一个 0-100 的百分比，表示任务执行到了哪一步

## 测试用例

### 1. 追踪任务状态更新

应记录并确认任务的状态和进度。

输入：

```json
{"src":"worker","dest":"monitor","body":{"type":"update_status","msg_id":1,"job_id":"job-123","status":"running","progress":25}}
```

期望输出：

```text
{"type": "status_updated", "in_reply_to": 1, "job_id": "job-123", "status": "running", "progress": 25}
```

### 2. 记录任务完成及指标

应记录耗时和资源使用情况。

输入：

```json
{"src":"worker","dest":"monitor","body":{"type":"job_completed","msg_id":1,"job_id":"job-123","duration_ms":60000,"resource_usage":{"cpu_percent":75,"memory_mb":1024}}}
```

期望输出：

```text
{"type": "job_completed", "in_reply_to": 1, "job_id": "job-123", "duration_ms": 60000, "resource_usage": {"cpu_percent": 75, "memory_mb": 1024}}
```

## 参考资料

- [The Four Golden Signals](https://sre.google/sre-book/monitoring-distributed-systems/)：Google SRE 监控指南，介绍延迟、流量、错误率、饱和度四大黄金指标

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
