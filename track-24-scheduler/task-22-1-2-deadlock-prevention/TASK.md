# Implement Deadlock Prevention in Scheduling

Website: <https://builddistributedsystem.com/tracks/scheduler/tasks/task-22-1-2-deadlock-prevention>

Track: 24. The Scheduler
Task order: 2
Short title: Deadlock Prevention
Difficulty: advanced
Subtrack: Centralized Job Scheduling

## Problem

Deadlock happens when two jobs each hold a resource the other needs, so neither can proceed. Prevention is better than detection: refuse any allocation that would leave the system in an unsafe state.

Implement a node that manages resource allocation with deadlock prevention:

```json
// Initialize resource pool
{ "type": "init", "msg_id": 1,
  "resources": {"total_cpu": 16, "total_memory": 64} }
-> { "type": "init_ok", "in_reply_to": 1 }

// Safe allocation: system remains in safe state
{ "type": "allocate_resources", "msg_id": 2,
  "job_id": "job1", "resources": {"cpu": 4, "memory": 16} }
-> { "type": "allocation_ok", "in_reply_to": 2,
    "job_id": "job1", "safe_state": true }

// Would exhaust resources -> unsafe -> deny
{ "type": "allocate_resources", "msg_id": 3,
  "job_id": "job2", "resources": {"cpu": 8, "memory": 32} }
-> denied

// Waiting too long -> preempt
{ "type": "allocate_resources", "msg_id": 4,
  "job_id": "job3", "resources": {"cpu": 16, "memory": 64}, "timeout_ms": 5000 }
-> { "type": "allocation_timeout", "in_reply_to": 4,
    "job_id": "job3", "action": "preempted" }

// Inspect wait-for graph
{ "type": "get_wait_graph", "msg_id": 5 }
-> { "type": "wait_graph_ok", "in_reply_to": 5,
    "graph": {"job1":["job3"],"job2":["job1"],"job3":["job2"]},
    "has_cycle": true }
```

## Concepts

- Banker's algorithm
- safe state
- wait-for graph
- preemption
- cycle detection

## Hints

- A system is in a safe state if there is an ordering in which all jobs can eventually complete
- Reject an allocation that would make the system unsafe (Banker's algorithm)
- Wait-for graph: edge A->B means A is waiting for a resource currently held by B
- A cycle in the wait-for graph means deadlock exists
- Preempt a job that has been waiting beyond timeout_ms and free its held resources

## Test Cases

### 1. Detect deadlock cycle

Allocating all remaining resources to job2 would create unsafe state and should be denied.

Input:

```json
{"src":"client","dest":"scheduler","body":{"type":"init","msg_id":1,"resources":{"total_cpu":16,"total_memory":64}}}
{"src":"client","dest":"scheduler","body":{"type":"allocate_resources","msg_id":2,"job_id":"job1","resources":{"cpu":8,"memory":32}}}
{"src":"client","dest":"scheduler","body":{"type":"allocate_resources","msg_id":3,"job_id":"job2","resources":{"cpu":8,"memory":32}}}
```

Expected output:

```text
{"src": "scheduler", "dest": "client", "body": {"type": "init_ok", "in_reply_to": 1}}
```

### 2. Safe state allocation

Allocation that leaves system in safe state should be granted.

Input:

```json
{"src":"client","dest":"scheduler","body":{"type":"allocate_resources","msg_id":1,"job_id":"job1","resources":{"cpu":4,"memory":16}}}
```

Expected output:

```text
{"src": "scheduler", "dest": "client", "body": {"type": "allocation_ok", "in_reply_to": 1, "job_id": "job1", "safe_state": true}}
```

## Resources

- [Banker's Algorithm](https://en.wikipedia.org/wiki/Banker%27s_algorithm): Dijkstra's algorithm for safe resource allocation

## Java Starter

The matching local starter file is:

```text
src/main/java/Main.java
```
