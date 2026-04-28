# Implement Job Scheduling System

Website: <https://builddistributedsystem.com/tracks/orchestrator/tasks/task-26-1-1-job-scheduling>

Track: 28. The Orchestrator
Task order: 1
Short title: Job Scheduling
Difficulty: intermediate
Subtrack: Scheduling

## Problem

A job scheduler runs tasks at a specific time or on a recurring schedule without the caller waiting. It is the backbone of background work: sending emails, cleaning up data, generating reports.

Implement a node that manages job scheduling and execution:

```json
// Schedule a one-time job to run after a delay
{ "type": "schedule_job", "msg_id": 1,
  "task": "send-email", "payload": {"to": "user@example.com"},
  "delay_ms": 60000 }
-> { "type": "job_scheduled", "in_reply_to": 1,
    "job_id": "<uuid>", "scheduled_at": "<iso-timestamp>" }

// Schedule a recurring job using a cron expression
{ "type": "schedule_job", "msg_id": 2,
  "task": "cleanup", "cron": "0 0 * * *", "payload": {"days": 30} }
-> { "type": "job_scheduled", "in_reply_to": 2,
    "job_id": "<uuid>", "next_run": "<iso-timestamp>" }

// Execute all jobs due at or before this time
{ "type": "execute_jobs", "msg_id": 3,
  "current_time": "2024-01-15T09:00:00Z" }
-> { "type": "jobs_executed", "in_reply_to": 3,
    "count": 2, "jobs": ["job-123", "job-456"] }

// Retry a failed job with exponential backoff
{ "type": "execute_job", "msg_id": 4,
  "job_id": "job-123", "force_fail": true }
-> { "type": "job_failed", "in_reply_to": 4,
    "job_id": "job-123", "retry_scheduled": true, "backoff_ms": 2000 }
```

Retry backoff: `base_ms * 2^attempt`. Stop retrying after max_attempts is reached.

## Concepts

- job scheduling
- cron expressions
- delayed execution
- exponential backoff
- retry policy

## Hints

- schedule_job with delay_ms schedules a one-time job to run after the delay
- schedule_job with cron schedules a recurring job; parse the cron expression to compute next_run
- execute_jobs finds all jobs whose scheduled_at <= current_time and runs them
- On job failure, schedule a retry using exponential backoff: backoff = base_ms * 2^attempt
- Each job must get a unique generated job_id returned in the response

## Test Cases

### 1. Schedule one-time job

Should schedule job and return a job_id with scheduled_at timestamp.

Input:

```json
{"src":"client","dest":"scheduler","body":{"type":"schedule_job","msg_id":1,"task":"send-email","payload":{"to":"user@example.com"},"delay_ms":60000}}
```

Expected output:

```text
{"type": "job_scheduled", "in_reply_to": 1, "job_id": ".*", "scheduled_at": ".*"}
```

### 2. Schedule recurring job with cron

Should parse cron expression and return next_run time.

Input:

```json
{"src":"client","dest":"scheduler","body":{"type":"schedule_job","msg_id":1,"task":"cleanup","cron":"0 0 * * *","payload":{"days":30}}}
```

Expected output:

```text
{"type": "job_scheduled", "in_reply_to": 1, "job_id": ".*", "next_run": ".*"}
```

## Resources

- [Cron Expression Reference](https://crontab.guru/): Interactive cron expression editor and reference

## Java Starter

The matching local starter file is:

```text
src/main/java/Main.java
```
