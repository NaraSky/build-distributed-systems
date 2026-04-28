# Implement Fair Job Scheduling

Website: <https://builddistributedsystem.com/tracks/scheduler/tasks/task-22-1-3-fair-scheduling>

Track: 24. The Scheduler
Task order: 3
Short title: Fair Scheduling
Difficulty: advanced
Subtrack: Centralized Job Scheduling

## Problem

Pure priority scheduling causes starvation: low-priority jobs may wait forever if high-priority jobs keep arriving. Fair scheduling prevents this through aging, multi-level feedback queues (MLFQ), and per-tenant fair share caps.

Implement a node that applies all three fairness mechanisms:

```json
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

Rules: aging adds +1 per 10 min wait. Quantum = 16ms. Blocking for I/O before 25% of quantum triggers promotion.

## Concepts

- starvation prevention
- aging
- MLFQ
- time quantum
- I/O-bound promotion
- fair share

## Hints

- Aging: add +1 to effective priority for every 10 minutes a job has been waiting
- MLFQ demotion: a job that runs past its quantum drops to the next lower priority queue
- MLFQ promotion: a job that voluntarily blocks for I/O before the quantum expires moves up one queue
- Fair share: each tenant gets at most their fraction of total capacity regardless of job count
- Effective priority = base_priority + floor(wait_time_minutes / 10)

## Test Cases

### 1. Aging prevents starvation

low_job waiting 10+ minutes should have priority boosted via aging.

Input:

```json
{"src":"client","dest":"scheduler","body":{"type":"submit_job","msg_id":1,"job":{"id":"low_job","priority":1,"submit_time":0}}}
{"src":"client","dest":"scheduler","body":{"type":"submit_job","msg_id":2,"job":{"id":"high_job","priority":10,"submit_time":600}}}
{"src":"client","dest":"scheduler","body":{"type":"schedule","msg_id":3,"current_time":601}}
```

Expected output:

```text
{"src": "scheduler", "dest": "client", "body": {"type": "scheduled", "in_reply_to": 3, "job_id": "low_job", "reason": "Aging increased priority to 2"}}
```

### 2. Time quantum preemption

CPU-bound job exceeding quantum should be demoted to lower priority queue.

Input:

```json
{"src":"client","dest":"scheduler","body":{"type":"submit_job","msg_id":1,"job":{"id":"cpu_bound_job","priority":5,"quantum_ms":16}}}
{"src":"client","dest":"scheduler","body":{"type":"start_job","msg_id":2,"job_id":"cpu_bound_job"}}
{"src":"client","dest":"scheduler","body":{"type":"job_quantum_exceeded","msg_id":3,"job_id":"cpu_bound_job","runtime_ms":20}}
```

Expected output:

```text
{"src": "scheduler", "dest": "client", "body": {"type": "job_preempted", "in_reply_to": 3, "job_id": "cpu_bound_job", "action": "demote_to_lower_queue"}}
```

## Resources

- [MLFQ Scheduling](https://pages.cs.wisc.edu/~remzi/OSTEP/cpu-sched-mlfq.pdf): Multi-Level Feedback Queue scheduling from OSTEP

## Java Starter

The matching local starter file is:

```text
src/main/java/Main.java
```
