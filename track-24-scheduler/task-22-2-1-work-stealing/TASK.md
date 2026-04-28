# Implement Work Stealing Scheduler

Website: <https://builddistributedsystem.com/tracks/scheduler/tasks/task-22-2-1-work-stealing>

Track: 24. The Scheduler
Task order: 6
Short title: Work Stealing
Difficulty: advanced
Subtrack: Distributed Work Allocation

## Problem

A central queue becomes a bottleneck when hundreds of workers hammer it simultaneously. Work stealing eliminates it: each worker has its own local deque and processes jobs independently. When a worker runs out of work, it steals from the back of a busy worker's deque.

Implement a cluster node that coordinates work stealing:

```json
// Idle worker w3 steals from a busy worker
{ "type": "steal_job", "msg_id": 1,
  "thief_worker": "w3", "busy_workers": ["w1","w2"] }
-> { "type": "job_stolen", "in_reply_to": 1,
    "thief": "w3", "victim": "w1",
    "job_id": "job2", "victim_queue_size": 2 }

// Check if the whole cluster is idle
{ "type": "check_cluster_state", "msg_id": 2 }
-> { "type": "cluster_state_ok", "in_reply_to": 2,
    "workers": {
      "w1": {"queue_size": 0, "state": "idle"},
      "w2": {"queue_size": 0, "state": "idle"},
      "w3": {"queue_size": 0, "state": "idle"}
    },
    "all_idle": true }
```

LIFO stealing (take from the tail) has ~9x less contention than FIFO (take from the head) because the owner pops from the front while the thief takes from the back — they rarely touch the same position.

## Concepts

- work stealing
- deque
- LIFO stealing
- lock-free scheduling
- idle detection

## Hints

- Each worker has its own deque; it pushes and pops from the front (LIFO for cache locality)
- An idle worker steals one job from the back of a randomly chosen busy worker
- LIFO stealing: owner uses front, thief uses back — they rarely collide, so less contention
- Detect all-idle when every worker queue is empty and no jobs are in-flight
- steal_job picks a victim at random from busy_workers and takes their last job

## Test Cases

### 1. Work stealing balances load

Work stealing should produce roughly equal utilization across workers.

Input:

```json
{"src":"client","dest":"cluster","body":{"type":"init","msg_id":1,"workers":["w1","w2","w3"],"jobs_to_distribute":6}}
{"src":"client","dest":"cluster","body":{"type":"run_simulation","msg_id":2,"duration_ms":1000}}
```

Expected output:

```text
{"src": "cluster", "dest": "client", "body": {"type": "init_ok", "in_reply_to": 1}}
```

### 2. Steal from random victim

Idle worker should steal one job from a randomly chosen busy worker.

Input:

```json
{"src":"client","dest":"cluster","body":{"type":"steal_job","msg_id":1,"thief_worker":"w3","busy_workers":["w1","w2"]}}
```

Expected output:

```text
{"src": "cluster", "dest": "client", "body": {"type": "job_stolen", "in_reply_to": 1, "thief": "w3", "victim": "w1", "job_id": "job2", "victim_queue_size": 2}}
```

## Resources

- [Work Stealing](https://en.wikipedia.org/wiki/Work_stealing): Work stealing scheduling for multi-threaded and distributed systems

## Java Starter

The matching local starter file is:

```text
src/main/java/Main.java
```
