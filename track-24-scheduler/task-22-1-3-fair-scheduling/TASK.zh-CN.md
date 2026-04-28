# 实现 Fair Job Scheduling

英文标题：Implement Fair Job Scheduling
网页：<https://builddistributedsystem.com/tracks/scheduler/tasks/task-22-1-3-fair-scheduling>

课程：24. 调度器：任务调度
任务序号：3
短标题：Fair Scheduling
难度：advanced
子主题：Centralized Job Scheduling

## 中文导读

本题要求你完成 `实现 Fair Job Scheduling`。

重点关注：`starvation prevention`、`aging`、`MLFQ`、`time quantum`、`I/O-bound promotion`。

建议先按提示逐步实现：Aging: add +1 to effective priority用于every 10 minutes a job has been waiting。

协议字段、消息类型、输入输出格式请以本文件中的代码块和测试用例为准。

## 题目说明

Pure priority scheduling causes starvation: low-priority jobs may wait forever if high-priority jobs keep arriving. Fair scheduling prevents this through aging, multi-level feedback queues (MLFQ),和per-tenant fair share caps.

Implement a 节点 that applies all three fairness mechanisms:

```JSON
// Aging: low-priority job waiting 10+ min gets a priority boost
submit: low_job(priority=1, submit_time=0)
submit: high_job(priority=10, submit_time=600)
{ "type": "schedule", "current_time": 601 }
-> { "type": "scheduled", "job_id": "low_job",
    "reason": "Aging increased priority to 2" }

// MLFQ demotion: CPU-bound job exceeds its 16ms quantum
{ "type": "job_quantum_exceeded",
  "job_id": "cpu_bound_job", "runtime_ms": 20 }
-> { "type": "job_preempted",
    "job_id": "cpu_bound_job", "action": "demote_to_lower_queue" }

// MLFQ promotion: I/O-bound job blocks well before quantum expires
{ "type": "job_io_blocked",
  "job_id": "io_job", "runtime_ms": 4 }
-> { "type": "job_promoted",
    "job_id": "io_job", "action": "promote_to_higher_queue" }
```

Rules: aging adds +1 per 10 min wait. Quantum = 16ms. Blocking用于I/O before 25% of quantum triggers promotion.

## 涉及概念

- `starvation prevention`
- `aging`
- `MLFQ`
- `time quantum`
- `I/O-bound promotion`
- `fair share`

## 实现提示

- Aging: add +1 to effective priority用于every 10 minutes a job has been waiting
- MLFQ demotion: a job that runs past its quantum drops to the next lower priority 队列
- MLFQ promotion: a job that voluntarily blocks用于I/O before the quantum expires moves up one 队列
- Fair share: each tenant gets at most their fraction of total capacity regardless of job count
- Effective priority = base_priority + floor(wait_time_minutes / 10)

## 测试用例

### 1. Aging prevents starvation

low_job waiting 10+ minutes should have priority boosted via aging.

输入：

```json
{"src":"client","dest":"scheduler","body":{"type":"submit_job","msg_id":1,"job":{"id":"low_job","priority":1,"submit_time":0}}}
{"src":"client","dest":"scheduler","body":{"type":"submit_job","msg_id":2,"job":{"id":"high_job","priority":10,"submit_time":600}}}
{"src":"client","dest":"scheduler","body":{"type":"schedule","msg_id":3,"current_time":601}}
```

期望输出：

```text
{"src": "scheduler", "dest": "client", "body": {"type": "scheduled", "in_reply_to": 3, "job_id": "low_job", "reason": "Aging increased priority to 2"}}
```

### 2. Time quantum preemption

CPU-bound job exceeding quantum should be demoted to lower priority 队列.

输入：

```json
{"src":"client","dest":"scheduler","body":{"type":"submit_job","msg_id":1,"job":{"id":"cpu_bound_job","priority":5,"quantum_ms":16}}}
{"src":"client","dest":"scheduler","body":{"type":"start_job","msg_id":2,"job_id":"cpu_bound_job"}}
{"src":"client","dest":"scheduler","body":{"type":"job_quantum_exceeded","msg_id":3,"job_id":"cpu_bound_job","runtime_ms":20}}
```

期望输出：

```text
{"src": "scheduler", "dest": "client", "body": {"type": "job_preempted", "in_reply_to": 3, "job_id": "cpu_bound_job", "action": "demote_to_lower_queue"}}
```

## 参考资料

- [MLFQ Scheduling](https://pages.cs.wisc.edu/~remzi/OSTEP/cpu-sched-mlfq.pdf)：Multi-Level Feedback 队列 scheduling from OSTEP

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
