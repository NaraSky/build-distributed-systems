# Implement Centralized Job Scheduler

Website: <https://builddistributedsystem.com/tracks/scheduler/tasks/task-22-1-1-centralized-scheduler>

Track: 24. The Scheduler
Task order: 1
Short title: Centralized Scheduler
Difficulty: intermediate
Subtrack: Centralized Job Scheduling

## Problem

A centralized scheduler is the single authority that receives all job submissions, maintains a priority queue, and dispatches work to available workers. When a worker fails, it reassigns its jobs without the client noticing.

Implement a node that acts as the central scheduler:

```json
// Initialize with available workers
{ "type": "init", "msg_id": 1,
  "workers": ["worker-1", "worker-2", "worker-3"] }
-> { "type": "init_ok", "in_reply_to": 1 }

// Submit a job; higher priority runs first
{ "type": "submit_job", "msg_id": 2,
  "job": {"id": "job1", "priority": 10, "type": "process_data"} }
-> [assigned to an available worker]

// Three jobs: priority 20 runs before 10 before 1
{ "type": "submit_job", ..., "job": {"id": "high_job", "priority": 20} }
-> { "type": "job_submitted", "job_id": "high_job" }

// Worker crashes -> scheduler reassigns its jobs
{ "type": "worker_failed", "worker_id": "worker-1" }
-> { "type": "job_reassigned",
    "job_id": "job1", "old_worker": "worker-1", "new_worker": "worker-2" }

// Inspect current queue state
{ "type": "get_queue_status", "msg_id": 1 }
-> { "type": "queue_status_ok", "in_reply_to": 1,
    "pending_jobs": 5, "running_jobs": 3, "workers_available": 2 }
```

## Concepts

- priority queue
- worker assignment
- job dispatch
- failure handling
- queue status

## Hints

- Maintain a max-heap of pending jobs; higher priority number = runs first
- On submit_job, assign immediately if a worker is free; otherwise enqueue
- On worker_failed, find all jobs running on that worker and reassign to another
- get_queue_status counts pending (queued but not assigned) vs running (assigned) separately
- Track a worker -> job mapping so you can reassign on failure

## Test Cases

### 1. Submit and schedule job

Job should be submitted and assigned to an available worker.

Input:

```json
{"src":"client","dest":"scheduler","body":{"type":"init","msg_id":1,"workers":["worker-1","worker-2","worker-3"]}}
{"src":"client","dest":"scheduler","body":{"type":"submit_job","msg_id":2,"job":{"id":"job1","type":"process_data","priority":10,"params":{"data":"abc"}}}}
```

Expected output:

```text
{"src": "scheduler", "dest": "client", "body": {"type": "init_ok", "in_reply_to": 1}}
```

### 2. Priority scheduling order

high_job (priority 20) should be scheduled first.

Input:

```json
{"src":"client","dest":"scheduler","body":{"type":"submit_job","msg_id":1,"job":{"id":"low_job","priority":1}}}
{"src":"client","dest":"scheduler","body":{"type":"submit_job","msg_id":2,"job":{"id":"high_job","priority":20}}}
{"src":"client","dest":"scheduler","body":{"type":"submit_job","msg_id":3,"job":{"id":"med_job","priority":10}}}
```

Expected output:

```text
{"src": "scheduler", "dest": "client", "body": {"type": "job_submitted", "in_reply_to": 2, "job_id": "high_job"}}
```

## Resources

- [Job Scheduling Algorithms](https://en.wikipedia.org/wiki/Job-shop_scheduling): Overview of job scheduling approaches

## Java Starter

The matching local starter file is:

```text
src/main/java/Main.java
```
