# 实现 Job Deadlines和Timeouts

英文标题：Implement Job Deadlines和Timeouts
网页：<https://builddistributedsystem.com/tracks/orchestrator/tasks/task-26-1-5-job-deadlines>

课程：28. 编排器：容器调度与服务网格
任务序号：5
短标题：Deadlines
难度：intermediate
子主题：Scheduling

## 中文导读

本题要求你完成 `实现 Job Deadlines和Timeouts`。

重点关注：`deadline`、`execution timeout`、`SLA enforcement`、`queue timeout`、`resource reclamation`。

建议先按提示逐步实现：execute_job，包含duration_ms > timeout_ms must return job_timeout。

协议字段、消息类型、输入输出格式请以本文件中的代码块和测试用例为准。

## 题目说明

Without deadlines, a hung job can occupy resources indefinitely和starve everything else. 超时 enforcement cancels overdue jobs和reclaims their resources.

Implement a 节点 that enforces three categories of time limit:

```JSON
// 1. Execution 超时: job runs longer than allowed
{ "type": "execute_job", "msg_id": 1,
  "job_id": "job-123", "timeout_ms": 1000, "duration_ms": 2000 }
-> { "type": "job_timeout", "in_reply_to": 1,
    "job_id": "job-123", "reason": "Execution 超时 exceeded" }

// 2. SLA check: warn before a deadline is missed
{ "type": "check_deadlines", "msg_id": 2 }
-> { "type": "deadlines_checked", "in_reply_to": 2,
    "jobs_near_deadline": [{"job_id": "job-456", "minutes_until": 3}],
    "missed": [] }

// 3. 队列 超时: cancel jobs stuck waiting too long
{ "type": "check_queue_timeouts", "msg_id": 3,
  "max_queue_time_ms": 300000 }
-> { "type": "queue_timeouts_enforced", "in_reply_to": 3,
    "cancelled": 1, "reason": "队列 超时 exceeded" }
```

Cancelling a job用于any reason must immediately free its allocated resources.

## 涉及概念

- `deadline`
- `execution timeout`
- `SLA enforcement`
- `queue timeout`
- `resource reclamation`

## 实现提示

- execute_job，包含duration_ms > timeout_ms must return job_timeout
- check_deadlines scans running jobs和flags those within a warning threshold of their SLA
- cancel_job marks the job cancelled和sets resources_freed=true
- check_queue_timeouts cancels jobs that have been waiting beyond max_queue_time_ms
- Always free allocated resources when cancelling — other jobs may be waiting用于them

## 测试用例

### 1. Execute job，包含超时

duration_ms exceeds timeout_ms so the job should be timed out.

输入：

```json
{"src":"worker","dest":"scheduler","body":{"type":"execute_job","msg_id":1,"job_id":"job-123","timeout_ms":1000,"duration_ms":2000}}
```

期望输出：

```text
{"type": "job_timeout", "in_reply_to": 1, "job_id": "job-123", "reason": "Execution timeout exceeded"}
```

### 2. Check SLA deadlines

Should report jobs approaching their SLA deadline.

输入：

```json
{"src":"monitor","dest":"scheduler","body":{"type":"check_deadlines","msg_id":1}}
```

期望输出：

```text
{"type": "deadlines_checked", "in_reply_to": 1, "jobs_near_deadline": [{"job_id": "job-456", "minutes_until": 3}], "missed": []}
```

## 参考资料

- [Timeouts,重试,和Backoff，包含Jitter](https://aws.amazon.com/builders-library/timeouts-retries-and-backoff-with-jitter/)：AWS builders library on 超时 strategies

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
