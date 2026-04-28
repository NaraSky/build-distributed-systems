# 实现 Fault-Tolerant 调度器

英文标题：Implement Fault-Tolerant Scheduler
网页：<https://builddistributedsystem.com/tracks/scheduler/tasks/task-22-2-3-scheduler-fault-tolerance>

课程：24. 调度器：任务调度
任务序号：8
短标题：Fault Tolerance
难度：advanced
子主题：Distributed Work Allocation

## 中文导读

本题要求你完成 `实现 Fault-Tolerant 调度器`。

重点关注：`WAL`、`crash recovery`、`leader election`、`generation numbers`、`duplicate prevention`。

建议先按提示逐步实现：WAL: write every assignment to the 日志 before applying it in memory。

协议字段、消息类型、输入输出格式请以本文件中的代码块和测试用例为准。

## 题目说明

A scheduler that crashes loses all in-flight job assignments. A 故障-tolerant scheduler writes every decision to a WAL before acting, so it can replay the 日志 on restart和recover exactly where it left off without re-assigning jobs twice.

Implement a 节点 that survives crashes和prevents duplicate assignments:

```JSON
// After crash和restart, recover from WAL
{ "type": "scheduler_restart" }
-> { "type": "recovery_complete",
    "job_assignments": {"job1": "w1"},
    "pending_notifications": ["w1"] }

// Primary crashes -> elect new Leader from replicas
{ "type": "leader_crash", "leader_id": "s1" }
-> { "type": "new_leader_elected",
    "old_leader": "s1", "new_leader": "s2", "term": 2 }

// Generation number prevents duplicate assignment
assign job1->w1 (gen=1)  // accepted
assign job1->w2 (gen=1)  // duplicate same generation -> rejected
-> { "type": "assignment_rejected",
    "reason": "Job already assigned in generation 1",
    "existing_assignment": {"job_id": "job1", "worker": "w1"} }
```

## 涉及概念

- `WAL`
- `crash recovery`
- `leader election`
- `generation numbers`
- `duplicate prevention`

## 实现提示

- WAL: write every assignment to the 日志 before applying it in memory
- On restart, replay the WAL sequentially to rebuild the in-memory assignment map
- Generation numbers (epochs): reject an assignment 消息 if the same job is already assigned in that generation
- After recovery, resend pending assignment notifications to all affected workers
- Leader election: highest-ID surviving replica becomes the new Leader

## 测试用例

### 1. 调度器 crash recovery

After restart, should recover assignments from WAL和list workers needing notifications.

输入：

```json
{"src":"client","dest":"scheduler","body":{"type":"init","msg_id":1,"replicas":["s1","s2","s3"]}}
{"type":"assign_job","job_id":"job1","worker_id":"w1"}
{"type":"scheduler_crash"}
{"type":"scheduler_restart"}
```

期望输出：

```text
{"type": "recovery_complete", "job_assignments": {"job1": "w1"}, "pending_notifications": ["w1"]}
```

### 2. Leader 选举 after crash

Should elect s2 as new Leader after s1 crashes.

输入：

```json
{"src":"client","dest":"scheduler_cluster","body":{"type":"init","msg_id":1,"replicas":["s1","s2","s3"]}}
{"type":"leader_crash","leader_id":"s1"}
```

期望输出：

```text
{"type": "new_leader_elected", "old_leader": "s1", "new_leader": "s2", "term": 2}
```

## 参考资料

- [Write-Ahead Logging](https://martinfowler.com/articles/patterns-of-distributed-systems/wal.html)：Martin Fowler's write-ahead 日志 pattern

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
