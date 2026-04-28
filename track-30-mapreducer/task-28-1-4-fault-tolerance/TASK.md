# Implement Fault Tolerance in MapReduce

Website: <https://builddistributedsystem.com/tracks/mapreducer/tasks/task-28-1-4-fault-tolerance>

Track: 30. The MapReducer
Task order: 4
Short title: Fault Tolerance
Difficulty: advanced
Subtrack: MapReduce Fundamentals

## Problem

Long-running MapReduce jobs will inevitably encounter worker failures. Fault tolerance means detecting failures quickly and retrying the affected tasks on healthy workers without restarting the entire job.

Your node (the master) must handle these messages:

```json
// Record a heartbeat from a worker
{ "type": "heartbeat", "msg_id": 1, "worker_id": "w1", "timestamp": 1700000000000 }
→ { "type": "heartbeat_ok", "in_reply_to": 1 }

// Check which workers have timed out (no heartbeat for > timeout_ms)
{ "type": "check_failures", "msg_id": 2, "timeout_ms": 5000, "now": 1700000010000 }
→ { "type": "failures_detected", "in_reply_to": 2, "failed_workers": ["w2"] }

// Reassign all tasks from a failed worker to a healthy one
{ "type": "reassign", "msg_id": 3, "failed_worker": "w2", "healthy_worker": "w3",
  "tasks": [{"id": "t1", "chunk": ["hello world"]}] }
→ { "type": "reassigned", "in_reply_to": 3, "reassigned_tasks": ["t1"] }
```

A worker is considered failed when `now - last_heartbeat_timestamp > timeout_ms`. Tasks assigned to failed workers are retried — they are idempotent, so running them again on a different worker is always safe.

## Concepts

- fault tolerance
- worker failure
- task retry
- heartbeat
- speculative execution
- idempotence

## Hints

- A worker is failed if now - last_heartbeat > timeout_ms
- On failure, find all tasks assigned to that worker and re-queue them
- Tasks must be idempotent: re-running produces the same result
- Speculative execution: if a task is running too long, start it on a second worker
- Use task attempts counter; drop the result from the slower duplicate

## Test Cases

### 1. Record heartbeat

Should acknowledge heartbeat from worker.

Input:

```json
{"src":"w1","dest":"master","body":{"type":"heartbeat","msg_id":1,"worker_id":"w1","timestamp":1700000000000}}
```

Expected output:

```text
{"type": "heartbeat_ok", "in_reply_to": 1}
```

### 2. Detect timed-out worker

10s elapsed > 5s timeout, so w1 should be failed.

Input:

```json
{"src":"w1","dest":"master","body":{"type":"heartbeat","msg_id":1,"worker_id":"w1","timestamp":1700000000000}}
{"src":"monitor","dest":"master","body":{"type":"check_failures","msg_id":2,"timeout_ms":5000,"now":1700000010000}}
```

Expected output:

```text
{"type": "heartbeat_ok", "in_reply_to": 1}
{"type": "failures_detected", "in_reply_to": 2, "failed_workers": ["w1"]}
```

## Resources

- [MapReduce: Simplified Data Processing on Large Clusters](https://research.google/pubs/pub62/): Section 3.3 covers fault tolerance in the original paper

## Java Starter

The matching local starter file is:

```text
src/main/java/Main.java
```
