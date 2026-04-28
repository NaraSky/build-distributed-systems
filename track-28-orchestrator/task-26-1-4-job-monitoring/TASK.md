# Implement Job Monitoring and Observability

Website: <https://builddistributedsystem.com/tracks/orchestrator/tasks/task-26-1-4-job-monitoring>

Track: 28. The Orchestrator
Task order: 4
Short title: Job Monitoring
Difficulty: intermediate
Subtrack: Scheduling

## Problem

Job monitoring gives operators visibility into what is running, how long it takes, and when things go wrong. Without it, a failed job can go undetected for hours.

Implement a node that tracks job lifecycle events and exposes aggregate statistics:

```json
// Record a status update with progress percentage
{ "type": "update_status", "msg_id": 1,
  "job_id": "job-123", "status": "running", "progress": 25 }
-> { "type": "status_updated", "in_reply_to": 1,
    "job_id": "job-123", "status": "running", "progress": 25 }

// Record completion with timing and resource metrics
{ "type": "job_completed", "msg_id": 2,
  "job_id": "job-123", "duration_ms": 60000,
  "resource_usage": {"cpu_percent": 75, "memory_mb": 1024} }
-> { "type": "job_completed", "in_reply_to": 2,
    "job_id": "job-123", "duration_ms": 60000,
    "resource_usage": {"cpu_percent": 75, "memory_mb": 1024} }

// Job fails after max retries -> send an alert
{ "type": "job_failed", "msg_id": 3,
  "job_id": "job-123", "error": "Connection timeout", "retries": 3 }
-> { "type": "alert_sent", "in_reply_to": 3,
    "job_id": "job-123",
    "alert": "Job failed after 3 retries: Connection timeout" }

// Aggregate statistics across all tracked jobs
{ "type": "get_stats", "msg_id": 4 }
-> { "type": "job_stats", "in_reply_to": 4,
    "total": 100, "completed": 85, "failed": 5, "avg_duration_ms": 5000 }
```

## Concepts

- job monitoring
- status tracking
- alerting
- metrics aggregation
- observability

## Hints

- update_status stores the current status and progress (0-100) for a job_id
- job_completed records duration_ms and resource_usage alongside the job record
- Fire an alert only when a job fails after exhausting all retries
- get_stats aggregates totals across all jobs: count by status and average duration_ms
- Progress is a percentage 0-100 representing how far through execution the job is

## Test Cases

### 1. Track job status updates

Should record and acknowledge job status and progress.

Input:

```json
{"src":"worker","dest":"monitor","body":{"type":"update_status","msg_id":1,"job_id":"job-123","status":"running","progress":25}}
```

Expected output:

```text
{"type": "status_updated", "in_reply_to": 1, "job_id": "job-123", "status": "running", "progress": 25}
```

### 2. Record job completion with metrics

Should record duration and resource usage.

Input:

```json
{"src":"worker","dest":"monitor","body":{"type":"job_completed","msg_id":1,"job_id":"job-123","duration_ms":60000,"resource_usage":{"cpu_percent":75,"memory_mb":1024}}}
```

Expected output:

```text
{"type": "job_completed", "in_reply_to": 1, "job_id": "job-123", "duration_ms": 60000, "resource_usage": {"cpu_percent": 75, "memory_mb": 1024}}
```

## Resources

- [The Four Golden Signals](https://sre.google/sre-book/monitoring-distributed-systems/): Google SRE guide on monitoring: latency, traffic, errors, saturation

## Java Starter

The matching local starter file is:

```text
src/main/java/Main.java
```
