# Implement Fault-Tolerant Scheduler

Website: <https://builddistributedsystem.com/tracks/scheduler/tasks/task-22-2-3-scheduler-fault-tolerance>

Track: 24. The Scheduler
Task order: 8
Short title: Fault Tolerance
Difficulty: advanced
Subtrack: Distributed Work Allocation

## Problem

A scheduler that crashes loses all in-flight job assignments. A fault-tolerant scheduler writes every decision to a WAL before acting, so it can replay the log on restart and recover exactly where it left off without re-assigning jobs twice.

Implement a node that survives crashes and prevents duplicate assignments:

```json
// After crash and restart, recover from WAL
{ "type": "scheduler_restart" }
-> { "type": "recovery_complete",
    "job_assignments": {"job1": "w1"},
    "pending_notifications": ["w1"] }

// Primary crashes -> elect new leader from replicas
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

## Concepts

- WAL
- crash recovery
- leader election
- generation numbers
- duplicate prevention

## Hints

- WAL: write every assignment to the log before applying it in memory
- On restart, replay the WAL sequentially to rebuild the in-memory assignment map
- Generation numbers (epochs): reject an assignment message if the same job is already assigned in that generation
- After recovery, resend pending assignment notifications to all affected workers
- Leader election: highest-ID surviving replica becomes the new leader

## Test Cases

### 1. Scheduler crash recovery

After restart, should recover assignments from WAL and list workers needing notifications.

Input:

```json
{"src":"client","dest":"scheduler","body":{"type":"init","msg_id":1,"replicas":["s1","s2","s3"]}}
{"type":"assign_job","job_id":"job1","worker_id":"w1"}
{"type":"scheduler_crash"}
{"type":"scheduler_restart"}
```

Expected output:

```text
{"type": "recovery_complete", "job_assignments": {"job1": "w1"}, "pending_notifications": ["w1"]}
```

### 2. Leader election after crash

Should elect s2 as new leader after s1 crashes.

Input:

```json
{"src":"client","dest":"scheduler_cluster","body":{"type":"init","msg_id":1,"replicas":["s1","s2","s3"]}}
{"type":"leader_crash","leader_id":"s1"}
```

Expected output:

```text
{"type": "new_leader_elected", "old_leader": "s1", "new_leader": "s2", "term": 2}
```

## Resources

- [Write-Ahead Logging](https://martinfowler.com/articles/patterns-of-distributed-systems/wal.html): Martin Fowler's write-ahead log pattern

## Java Starter

The matching local starter file is:

```text
src/main/java/Main.java
```
