# Implement Resource Estimation and Provisioning

Website: <https://builddistributedsystem.com/tracks/scheduler/tasks/task-22-1-5-resource-estimation>

Track: 24. The Scheduler
Task order: 5
Short title: Resource Estimation
Difficulty: advanced
Subtrack: Centralized Job Scheduling

## Problem

Before scheduling a job, the scheduler needs to know how many resources it requires. Good estimation averages historical data for the same job type. Bin packing then places jobs on the fewest workers, and auto-scaling adjusts total capacity based on load.

Implement a node that estimates resources, packs jobs, and makes scaling decisions:

```json
// Estimate from historical jobs of the same type
{ "type": "submit_job", "msg_id": 1,
  "job": {"id":"job1","type":"render_video","params":{"resolution":"1080p"}},
  "estimate_resources": true }
-> { "type": "job_submitted", "in_reply_to": 1,
    "estimated_resources": {"cpu":4,"memory":16,"duration_min":15},
    "historical_jobs_analyzed": 10 }

// Bin pack 3 jobs onto minimum workers (8cpu/32gb each)
{ "type": "submit_jobs", "msg_id": 2,
  "jobs": [{"id":"j1","cpu":4,"memory":16},
            {"id":"j2","cpu":2,"memory":8},
            {"id":"j3","cpu":4,"memory":16}],
  "worker_capacity": {"cpu":8,"memory":32} }
-> { "type": "jobs_scheduled", "in_reply_to": 2,
    "workers_provisioned": 2, "packing_efficiency": 0.75 }

// High queue depth -> scale up
{ "type": "check_scaling", "msg_id": 3,
  "queue_depth": 50, "avg_wait_time_ms": 300000, "workers": 5 }
-> { "type": "scaling_action", "action": "scale_up",
    "current_workers": 5, "new_workers": 10,
    "reason": "Queue depth > threshold" }
```

## Concepts

- resource estimation
- bin packing
- auto-scaling
- historical analysis
- packing efficiency

## Hints

- Historical estimation: average cpu, memory, duration from the last 10 jobs of the same type
- Bin packing: pack jobs onto the fewest workers without exceeding per-worker capacity
- packing_efficiency = sum(job_resources) / (workers_provisioned * worker_capacity)
- Scale up when queue_depth exceeds a threshold and average wait time is high
- Scale down when all worker utilizations are below 20% and queue is empty

## Test Cases

### 1. Resource estimation from history

Should estimate resources by averaging similar historical jobs.

Input:

```json
{"src":"client","dest":"scheduler","body":{"type":"submit_job","msg_id":1,"job":{"id":"job1","type":"render_video","params":{"resolution":"1080p"}},"estimate_resources":true}}
```

Expected output:

```text
{"src": "scheduler", "dest": "client", "body": {"type": "job_submitted", "in_reply_to": 1, "estimated_resources": {"cpu": 4, "memory": 16, "duration_min": 15}, "historical_jobs_analyzed": 10}}
```

### 2. Bin packing efficiency

j1+j3 on worker1, j2 on worker2 = 2 workers, efficiency=0.75.

Input:

```json
{"src":"client","dest":"scheduler","body":{"type":"submit_jobs","msg_id":1,"jobs":[{"id":"j1","cpu":4,"memory":16},{"id":"j2","cpu":2,"memory":8},{"id":"j3","cpu":4,"memory":16}],"worker_capacity":{"cpu":8,"memory":32}}}
```

Expected output:

```text
{"src": "scheduler", "dest": "client", "body": {"type": "jobs_scheduled", "in_reply_to": 1, "workers_provisioned": 2, "packing_efficiency": 0.75}}
```

## Resources

- [Bin Packing Problem](https://en.wikipedia.org/wiki/Bin_packing_problem): Packing items into fewest bins — NP-hard but good heuristics exist

## Java Starter

The matching local starter file is:

```text
src/main/java/Main.java
```
