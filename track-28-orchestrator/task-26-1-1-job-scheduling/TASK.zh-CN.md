# 实现 Job Scheduling System

英文标题：Implement Job Scheduling System
网页：<https://builddistributedsystem.com/tracks/orchestrator/tasks/task-26-1-1-job-scheduling>

课程：28. 编排器：容器调度与服务网格
任务序号：1
短标题：Job Scheduling
难度：intermediate
子主题：Scheduling

## 中文导读

本题要求你完成 `实现 Job Scheduling System`。

重点关注：`job scheduling`、`cron expressions`、`delayed execution`、`exponential backoff`、`retry policy`。

建议先按提示逐步实现：schedule_job，包含delay_ms schedules a one-time job to run after the delay。

协议字段、消息类型、输入输出格式请以本文件中的代码块和测试用例为准。

## 题目说明

A job scheduler runs tasks at a specific time or on a recurring schedule without the caller waiting. It is the backbone of background work: sending emails, cleaning up data, generating reports.

Implement a 节点 that manages job scheduling和execution:

```JSON
// Schedule a one-time job to run after a delay
{ "type": "schedule_job", "msg_id": 1,
  "task": "send-email", "payload": {"to": "user@example.com"},
  "delay_ms": 60000 }
-> { "type": "job_scheduled", "in_reply_to": 1,
    "job_id": "<uuid>", "scheduled_at": "<iso-timestamp>" }

// Schedule a recurring job使用a cron expression
{ "type": "schedule_job", "msg_id": 2,
  "task": "cleanup", "cron": "0 0 * * *", "payload": {"days": 30} }
-> { "type": "job_scheduled", "in_reply_to": 2,
    "job_id": "<uuid>", "next_run": "<iso-timestamp>" }

// Execute all jobs due at or before this time
{ "type": "execute_jobs", "msg_id": 3,
  "current_time": "2024-01-15T09:00:00Z" }
-> { "type": "jobs_executed", "in_reply_to": 3,
    "count": 2, "jobs": ["job-123", "job-456"] }

// 重试 a failed job，包含exponential backoff
{ "type": "execute_job", "msg_id": 4,
  "job_id": "job-123", "force_fail": true }
-> { "type": "job_failed", "in_reply_to": 4,
    "job_id": "job-123", "retry_scheduled": true, "backoff_ms": 2000 }
```

重试 backoff: `base_ms * 2^attempt`. Stop retrying after max_attempts is reached.

## 涉及概念

- `job scheduling`
- `cron expressions`
- `delayed execution`
- `exponential backoff`
- `retry policy`

## 实现提示

- schedule_job，包含delay_ms schedules a one-time job to run after the delay
- schedule_job，包含cron schedules a recurring job; parse the cron expression to compute next_run
- execute_jobs finds all jobs whose scheduled_at <= current_time和runs them
- On job 故障, schedule a 重试使用exponential backoff: backoff = base_ms * 2^attempt
- Each job must get a unique generated job_id returned in the 响应

## 测试用例

### 1. Schedule one-time job

Should schedule job和return a job_id，包含scheduled_at timestamp.

输入：

```json
{"src":"client","dest":"scheduler","body":{"type":"schedule_job","msg_id":1,"task":"send-email","payload":{"to":"user@example.com"},"delay_ms":60000}}
```

期望输出：

```text
{"type": "job_scheduled", "in_reply_to": 1, "job_id": ".*", "scheduled_at": ".*"}
```

### 2. Schedule recurring job，包含cron

Should parse cron expression和return next_run time.

输入：

```json
{"src":"client","dest":"scheduler","body":{"type":"schedule_job","msg_id":1,"task":"cleanup","cron":"0 0 * * *","payload":{"days":30}}}
```

期望输出：

```text
{"type": "job_scheduled", "in_reply_to": 1, "job_id": ".*", "next_run": ".*"}
```

## 参考资料

- [Cron Expression Reference](https://crontab.guru/)：Interactive cron expression editor和reference

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
