# 实现任务截止时间与超时控制

英文标题：Implement Job Deadlines and Timeouts
网页：<https://builddistributedsystem.com/tracks/orchestrator/tasks/task-26-1-5-job-deadlines>

课程：28. 编排器：容器调度与服务网格
任务序号：5
短标题：Deadlines
难度：进阶
子主题：Scheduling

## 中文导读

这道题要求你实现一个强制执行时间限制的节点。如果没有截止时间，一个卡住的任务可能会无限期地占用资源，拖垮整个系统。超时控制会取消逾期的任务并回收它们占用的资源。你需要处理三种场景：执行超时、SLA 截止时间预警和排队超时。这是保证系统资源不被滥用的关键机制。

## 题目说明

如果没有截止时间（Deadline），一个卡住的任务会无限期占用资源，导致其他任务被饿死。超时控制会取消逾期任务并回收其资源。

请实现一个强制执行三类时间限制的节点：

```json
// 1. 执行超时：任务运行时间超过允许值
{ "type": "execute_job", "msg_id": 1,
  "job_id": "job-123", "timeout_ms": 1000, "duration_ms": 2000 }
-> { "type": "job_timeout", "in_reply_to": 1,
    "job_id": "job-123", "reason": "Execution timeout exceeded" }

// 2. SLA 检查：在错过截止时间之前发出预警
{ "type": "check_deadlines", "msg_id": 2 }
-> { "type": "deadlines_checked", "in_reply_to": 2,
    "jobs_near_deadline": [{"job_id": "job-456", "minutes_until": 3}],
    "missed": [] }

// 3. 排队超时：取消等待时间过长的任务
{ "type": "check_queue_timeouts", "msg_id": 3,
  "max_queue_time_ms": 300000 }
-> { "type": "queue_timeouts_enforced", "in_reply_to": 3,
    "cancelled": 1, "reason": "Queue timeout exceeded" }
```

无论因为什么原因取消任务，都必须立即释放该任务已分配的资源。

## 涉及概念

- `deadline`
- `execution timeout`
- `SLA enforcement`
- `queue timeout`
- `resource reclamation`

## 实现提示

- 当 `duration_ms > timeout_ms` 时，`execute_job` 必须返回超时错误
- `check_deadlines` 扫描正在运行的任务，标记那些即将到达 SLA 截止时间的任务
- `cancel_job` 将任务标记为已取消，并设置 `resources_freed=true`
- `check_queue_timeouts` 取消等待时间超过 `max_queue_time_ms` 的任务
- 取消任务时务必释放已分配的资源，因为其他任务可能正在等待这些资源

## 测试用例

### 1. 执行带超时限制的任务

执行时间超过超时限制，任务应被判定为超时。

输入：

```json
{"src":"worker","dest":"scheduler","body":{"type":"execute_job","msg_id":1,"job_id":"job-123","timeout_ms":1000,"duration_ms":2000}}
```

期望输出：

```text
{"type": "job_timeout", "in_reply_to": 1, "job_id": "job-123", "reason": "Execution timeout exceeded"}
```

### 2. 检查 SLA 截止时间

应报告即将到达 SLA 截止时间的任务。

输入：

```json
{"src":"monitor","dest":"scheduler","body":{"type":"check_deadlines","msg_id":1}}
```

期望输出：

```text
{"type": "deadlines_checked", "in_reply_to": 1, "jobs_near_deadline": [{"job_id": "job-456", "minutes_until": 3}], "missed": []}
```

## 参考资料

- [Timeouts, Retries, and Backoff with Jitter](https://aws.amazon.com/builders-library/timeouts-retries-and-backoff-with-jitter/)：AWS 构建者库中关于超时策略的指南

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
