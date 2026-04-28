# 实现公平调度

英文标题：Implement Fair Job Scheduling
网页：<https://builddistributedsystem.com/tracks/scheduler/tasks/task-22-1-3-fair-scheduling>

课程：24. 任务调度器
任务序号：3
短标题：公平调度
难度：高级
子主题：集中式任务调度

## 中文导读

这道题要求你实现公平调度（Fair Scheduling）机制。纯粹按优先级调度会导致"饥饿"问题：低优先级任务可能永远排不上。公平调度通过老化提升、多级反馈队列等机制解决这个问题，就像排队时等太久的人可以插到前面，确保每个人最终都能被服务到。

## 题目说明

纯优先级调度会导致饥饿（Starvation）：如果高优先级任务不断到来，低优先级任务可能永远等不到执行。公平调度通过老化（Aging）、多级反馈队列（MLFQ）和租户公平份额上限来防止这种情况。

实现一个同时应用以上三种公平机制的节点：

```json
// 老化：等待超过 10 分钟的低优先级任务获得优先级提升
submit: low_job(priority=1, submit_time=0)
submit: high_job(priority=10, submit_time=600)
{ "type": "schedule", "current_time": 601 }
-> { "type": "scheduled", "job_id": "low_job",
    "reason": "Aging increased priority to 2" }

// 多级反馈队列降级：计算密集型任务超过了 16ms 的时间片
{ "type": "job_quantum_exceeded",
  "job_id": "cpu_bound_job", "runtime_ms": 20 }
-> { "type": "job_preempted",
    "job_id": "cpu_bound_job", "action": "demote_to_lower_queue" }

// 多级反馈队列升级：IO 密集型任务在时间片用完前主动让出
{ "type": "job_io_blocked",
  "job_id": "io_job", "runtime_ms": 4 }
-> { "type": "job_promoted",
    "job_id": "io_job", "action": "promote_to_higher_queue" }
```

规则：老化每等待 10 分钟优先级加 1。时间片为 16ms。在时间片的 25% 之前因 IO 阻塞则触发升级。

## 涉及概念

- starvation prevention
- aging
- MLFQ
- time quantum
- I/O-bound promotion
- fair share

## 实现提示

- 老化：任务每等待 10 分钟，有效优先级加 1
- 多级反馈队列降级：运行时间超过时间片的任务，降到下一个更低优先级的队列
- 多级反馈队列升级：在时间片用完之前主动因 IO 阻塞的任务，升到上一个更高优先级的队列
- 公平份额：每个租户最多只能使用其占总容量比例的资源，不论提交了多少任务
- 有效优先级 = 基础优先级 + floor(等待时间分钟数 / 10)

## 测试用例

### 1. 老化防止饥饿

等待超过 10 分钟的 `low_job` 应通过老化机制获得优先级提升。

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

### 2. 时间片抢占

超过时间片的计算密集型任务应被降级到更低优先级的队列。

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

- [MLFQ Scheduling](https://pages.cs.wisc.edu/~remzi/OSTEP/cpu-sched-mlfq.pdf)：操作系统教材中关于多级反馈队列调度的章节

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
