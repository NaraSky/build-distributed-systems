# Implement Resource Management for Jobs

Website: <https://builddistributedsystem.com/tracks/orchestrator/tasks/task-26-1-3-resource-management>

Track: 28. The Orchestrator
Task order: 3
Short title: Resource Management
Difficulty: intermediate
Subtrack: Scheduling

## Problem

Jobs compete for finite resources like CPU, memory, and GPU. Resource management tracks what is available, grants allocations when possible, and queues jobs that would exceed capacity.

Implement a node that manages a shared resource pool:

```json
// Allocate resources (succeeds if enough available)
{ "type": "allocate", "msg_id": 1,
  "requirements": [{"type": "cpu", "amount": 2},
                   {"type": "memory", "amount": 4}] }
-> { "type": "allocated", "in_reply_to": 1,
    "allocation_id": "<uuid>",
    "resources": {"cpu": 2, "memory": 4} }

// Not enough GPU -> queue the job
{ "type": "allocate", "msg_id": 2,
  "requirements": [{"type": "gpu", "amount": 4}] }
-> { "type": "queued", "in_reply_to": 2,
    "reason": "Insufficient resources",
    "available": {"gpu": 2}, "required": 4 }

// Release resources when job finishes
{ "type": "release", "msg_id": 3,
  "allocation_id": "alloc-123", "job_status": "completed" }
-> { "type": "released", "in_reply_to": 3,
    "allocation_id": "alloc-123",
    "resources_freed": {"cpu": 2, "memory": 4} }

// Submit 3 jobs with a concurrency cap of 2
{ "type": "submit_job", "msg_id": 4,
  "category": "heavy", "concurrency_limit": 2, "jobs": 3 }
-> { "type": "jobs_submitted", "in_reply_to": 4,
    "queued": 1, "running": 2, "waiting": 1 }
```

## Concepts

- resource allocation
- resource pool
- job queuing
- concurrency limit
- fairness

## Hints

- Track a pool of available resources; subtract on allocate, restore on release
- If requested amount exceeds available, return queued with available and required amounts
- concurrency_limit caps how many jobs of a category run simultaneously; queue the rest
- release returns which resources were freed using the allocation_id as the key
- After a release, check if any queued jobs can now be allocated

## Test Cases

### 1. Allocate resources for job

Should allocate requested CPU and memory.

Input:

```json
{"src":"scheduler","dest":"resources","body":{"type":"allocate","msg_id":1,"requirements":[{"type":"cpu","amount":2},{"type":"memory","amount":4}]}}
```

Expected output:

```text
{"type": "allocated", "in_reply_to": 1, "allocation_id": ".*", "resources": {"cpu": 2, "memory": 4}}
```

### 2. Queue job when resources unavailable

Insufficient GPU should queue the job.

Input:

```json
{"src":"scheduler","dest":"resources","body":{"type":"allocate","msg_id":1,"requirements":[{"type":"gpu","amount":4}]}}
```

Expected output:

```text
{"type": "queued", "in_reply_to": 1, "reason": "Insufficient resources", "available": {"gpu": 2}, "required": 4}
```

## Resources

- [Kubernetes Resource Management](https://kubernetes.io/docs/concepts/configuration/manage-resources-containers/): Resource requests and limits in production orchestration

## Java Starter

The matching local starter file is:

```text
src/main/java/Main.java
```
