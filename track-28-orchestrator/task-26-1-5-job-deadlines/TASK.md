# Implement Job Deadlines and Timeouts

Website: <https://builddistributedsystem.com/tracks/orchestrator/tasks/task-26-1-5-job-deadlines>

Track: 28. The Orchestrator
Task order: 5
Short title: Deadlines
Difficulty: intermediate
Subtrack: Scheduling

## Problem

Without deadlines, a hung job can occupy resources indefinitely and starve everything else. Timeout enforcement cancels overdue jobs and reclaims their resources.

Implement a node that enforces three categories of time limit:

```json
// 1. Execution timeout: job runs longer than allowed
{ "type": "execute_job", "msg_id": 1,
  "job_id": "job-123", "timeout_ms": 1000, "duration_ms": 2000 }
-> { "type": "job_timeout", "in_reply_to": 1,
    "job_id": "job-123", "reason": "Execution timeout exceeded" }

// 2. SLA check: warn before a deadline is missed
{ "type": "check_deadlines", "msg_id": 2 }
-> { "type": "deadlines_checked", "in_reply_to": 2,
    "jobs_near_deadline": [{"job_id": "job-456", "minutes_until": 3}],
    "missed": [] }

// 3. Queue timeout: cancel jobs stuck waiting too long
{ "type": "check_queue_timeouts", "msg_id": 3,
  "max_queue_time_ms": 300000 }
-> { "type": "queue_timeouts_enforced", "in_reply_to": 3,
    "cancelled": 1, "reason": "Queue timeout exceeded" }
```

Cancelling a job for any reason must immediately free its allocated resources.

## Concepts

- deadline
- execution timeout
- SLA enforcement
- queue timeout
- resource reclamation

## Hints

- execute_job with duration_ms > timeout_ms must return job_timeout
- check_deadlines scans running jobs and flags those within a warning threshold of their SLA
- cancel_job marks the job cancelled and sets resources_freed=true
- check_queue_timeouts cancels jobs that have been waiting beyond max_queue_time_ms
- Always free allocated resources when cancelling — other jobs may be waiting for them

## Test Cases

### 1. Execute job with timeout

duration_ms exceeds timeout_ms so the job should be timed out.

Input:

```json
{"src":"worker","dest":"scheduler","body":{"type":"execute_job","msg_id":1,"job_id":"job-123","timeout_ms":1000,"duration_ms":2000}}
```

Expected output:

```text
{"type": "job_timeout", "in_reply_to": 1, "job_id": "job-123", "reason": "Execution timeout exceeded"}
```

### 2. Check SLA deadlines

Should report jobs approaching their SLA deadline.

Input:

```json
{"src":"monitor","dest":"scheduler","body":{"type":"check_deadlines","msg_id":1}}
```

Expected output:

```text
{"type": "deadlines_checked", "in_reply_to": 1, "jobs_near_deadline": [{"job_id": "job-456", "minutes_until": 3}], "missed": []}
```

## Resources

- [Timeouts, Retries, and Backoff with Jitter](https://aws.amazon.com/builders-library/timeouts-retries-and-backoff-with-jitter/): AWS builders library on timeout strategies

## Java Starter

The matching local starter file is:

```text
src/main/java/Main.java
```
