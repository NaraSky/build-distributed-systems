# 实现任务调度系统

英文标题：Implement Job Scheduling System
网页：<https://builddistributedsystem.com/tracks/orchestrator/tasks/task-26-1-1-job-scheduling>

课程：28. 编排器：容器调度与服务网格
任务序号：1
短标题：Job Scheduling
难度：进阶
子主题：Scheduling

## 中文导读

这道题要求你实现一个任务调度（Job Scheduling）系统。任务调度器是后台工作的基石，负责在指定时间或按周期性计划运行任务，比如发送邮件、清理过期数据、生成报表等。你需要支持一次性延迟任务、基于 cron 表达式的周期性任务，以及失败后的指数退避重试。这是几乎所有生产系统都需要的基础能力。

## 题目说明

任务调度器在指定时间或按周期性计划运行任务，调用方无需等待任务完成。它是后台工作的基石，用于发送邮件、清理数据、生成报表等。

请实现一个管理任务调度和执行的节点：

```json
// 调度一个延迟执行的一次性任务
{ "type": "schedule_job", "msg_id": 1,
  "task": "send-email", "payload": {"to": "user@example.com"},
  "delay_ms": 60000 }
-> { "type": "job_scheduled", "in_reply_to": 1,
    "job_id": "<uuid>", "scheduled_at": "<iso-timestamp>" }

// 使用 cron 表达式调度周期性任务
{ "type": "schedule_job", "msg_id": 2,
  "task": "cleanup", "cron": "0 0 * * *", "payload": {"days": 30} }
-> { "type": "job_scheduled", "in_reply_to": 2,
    "job_id": "<uuid>", "next_run": "<iso-timestamp>" }

// 执行所有到期的任务
{ "type": "execute_jobs", "msg_id": 3,
  "current_time": "2024-01-15T09:00:00Z" }
-> { "type": "jobs_executed", "in_reply_to": 3,
    "count": 2, "jobs": ["job-123", "job-456"] }

// 失败任务按指数退避重试
{ "type": "execute_job", "msg_id": 4,
  "job_id": "job-123", "force_fail": true }
-> { "type": "job_failed", "in_reply_to": 4,
    "job_id": "job-123", "retry_scheduled": true, "backoff_ms": 2000 }
```

重试退避公式：`base_ms * 2^attempt`。达到最大重试次数后停止重试。

## 涉及概念

- `job scheduling`
- `cron expressions`
- `delayed execution`
- `exponential backoff`
- `retry policy`

## 实现提示

- 带 `delay_ms` 的 `schedule_job` 调度一个在延迟后执行的一次性任务
- 带 `cron` 的 `schedule_job` 调度周期性任务，需要解析 cron 表达式来计算下次执行时间
- `execute_jobs` 找出所有 `scheduled_at <= current_time` 的任务并执行
- 任务失败时，按指数退避调度重试：`backoff = base_ms * 2^attempt`
- 每个任务必须生成一个唯一的 `job_id` 并在响应中返回

## 测试用例

### 1. 调度一次性任务

应调度任务并返回 job_id 和 scheduled_at 时间戳。

输入：

```json
{"src":"client","dest":"scheduler","body":{"type":"schedule_job","msg_id":1,"task":"send-email","payload":{"to":"user@example.com"},"delay_ms":60000}}
```

期望输出：

```text
{"type": "job_scheduled", "in_reply_to": 1, "job_id": ".*", "scheduled_at": ".*"}
```

### 2. 使用 cron 调度周期性任务

应解析 cron 表达式并返回下次执行时间。

输入：

```json
{"src":"client","dest":"scheduler","body":{"type":"schedule_job","msg_id":1,"task":"cleanup","cron":"0 0 * * *","payload":{"days":30}}}
```

期望输出：

```text
{"type": "job_scheduled", "in_reply_to": 1, "job_id": ".*", "next_run": ".*"}
```

## 参考资料

- [Cron Expression Reference](https://crontab.guru/)：交互式 cron 表达式编辑器和参考手册

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
