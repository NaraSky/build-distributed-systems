# 实现容错调度器

英文标题：Implement Fault-Tolerant Scheduler
网页：<https://builddistributedsystem.com/tracks/scheduler/tasks/task-22-2-3-scheduler-fault-tolerance>

课程：24. 任务调度器
任务序号：8
短标题：调度器容错
难度：高级
子主题：分布式任务分配

## 中文导读

这道题要求你实现一个能从崩溃中恢复的容错调度器。普通调度器崩溃后，所有正在进行的任务分配信息都会丢失。容错调度器的解决方案是：每次做决策之前先写预写日志（WAL），重启后回放日志就能恢复到崩溃前的状态，既不丢失信息也不会重复分配任务。

## 题目说明

调度器一旦崩溃，内存中的任务分配信息全部丢失。容错调度器通过预写日志（WAL，Write-Ahead Log）解决这个问题：在执行每一次任务分配之前，先把这个决策写入持久化的日志文件。重启后只需按顺序回放日志，就能精确重建崩溃前的内存状态，不会遗漏也不会重复。

你需要实现一个能经受崩溃并防止重复分配的节点：

```json
// 崩溃重启后，从预写日志恢复
{ "type": "scheduler_restart" }
-> { "type": "recovery_complete",
    "job_assignments": {"job1": "w1"},
    "pending_notifications": ["w1"] }

// 主节点崩溃 -> 从副本中选举新的领导者
{ "type": "leader_crash", "leader_id": "s1" }
-> { "type": "new_leader_elected",
    "old_leader": "s1", "new_leader": "s2", "term": 2 }

// 代数编号防止重复分配
assign job1->w1 (gen=1)  // 被接受
assign job1->w2 (gen=1)  // 同一代重复 -> 被拒绝
-> { "type": "assignment_rejected",
    "reason": "Job already assigned in generation 1",
    "existing_assignment": {"job_id": "job1", "worker": "w1"} }
```

代数编号（Generation Number）类似于"任期"的概念：在同一个任期内，一个任务只能被分配一次。如果收到的分配请求与当前任期内已有的分配冲突，就直接拒绝，从而避免重复分配。

## 涉及概念

- WAL
- crash recovery
- leader election
- generation numbers
- duplicate prevention

## 实现提示

- 预写日志：在内存中执行分配操作之前，先将每次分配写入日志
- 重启时，按顺序回放预写日志，重建内存中的分配映射
- 代数编号：如果同一代中该任务已被分配，则拒绝重复的分配消息
- 恢复完成后，向所有相关工作节点重新发送待确认的分配通知
- 领导者选举：存活的副本中编号最大的成为新的领导者

## 测试用例

### 1. 调度器崩溃恢复

重启后应从预写日志恢复分配信息，并列出需要通知的工作节点。

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

### 2. 崩溃后的领导者选举

s1 崩溃后应选举 s2 为新的领导者。

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

- [Write-Ahead Logging](https://martinfowler.com/articles/patterns-of-distributed-systems/wal.html)：Martin Fowler 关于预写日志模式的文章

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
