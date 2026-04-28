# 实现 Work Stealing 调度器

英文标题：Implement Work Stealing Scheduler
网页：<https://builddistributedsystem.com/tracks/scheduler/tasks/task-22-2-1-work-stealing>

课程：24. 调度器：任务调度
任务序号：6
短标题：Work Stealing
难度：advanced
子主题：Distributed Work Allocation

## 中文导读

本题要求你完成 `实现 Work Stealing 调度器`。

重点关注：`work stealing`、`deque`、`LIFO stealing`、`lock-free scheduling`、`idle detection`。

建议先按提示逐步实现：Each worker has its own deque; it pushes和pops from the front (LIFO用于缓存 locality)。

协议字段、消息类型、输入输出格式请以本文件中的代码块和测试用例为准。

## 题目说明

A central 队列 becomes a bottleneck when hundreds of workers hammer it simultaneously. Work stealing eliminates it: each worker has its own local deque和processes jobs independently. When a worker runs out of work, it steals from the back of a busy worker's deque.

Implement a 集群 节点 that coordinates work stealing:

```JSON
// Idle worker w3 steals from a busy worker
{ "type": "steal_job", "msg_id": 1,
  "thief_worker": "w3", "busy_workers": ["w1","w2"] }
-> { "type": "job_stolen", "in_reply_to": 1,
    "thief": "w3", "victim": "w1",
    "job_id": "job2", "victim_queue_size": 2 }

// Check if the whole 集群 is idle
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

## 涉及概念

- `work stealing`
- `deque`
- `LIFO stealing`
- `lock-free scheduling`
- `idle detection`

## 实现提示

- Each worker has its own deque; it pushes和pops from the front (LIFO用于缓存 locality)
- An idle worker steals one job from the back of a randomly chosen busy worker
- LIFO stealing: owner uses front, thief uses back — they rarely collide, so less contention
- Detect all-idle when every worker 队列 is empty和no jobs are in-flight
- steal_job picks a victim at random from busy_workers和takes their last job

## 测试用例

### 1. Work stealing balances load

Work stealing should produce roughly equal utilization across workers.

输入：

```json
{"src":"client","dest":"cluster","body":{"type":"init","msg_id":1,"workers":["w1","w2","w3"],"jobs_to_distribute":6}}
{"src":"client","dest":"cluster","body":{"type":"run_simulation","msg_id":2,"duration_ms":1000}}
```

期望输出：

```text
{"src": "cluster", "dest": "client", "body": {"type": "init_ok", "in_reply_to": 1}}
```

### 2. Steal from random victim

Idle worker should steal one job from a randomly chosen busy worker.

输入：

```json
{"src":"client","dest":"cluster","body":{"type":"steal_job","msg_id":1,"thief_worker":"w3","busy_workers":["w1","w2"]}}
```

期望输出：

```text
{"src": "cluster", "dest": "client", "body": {"type": "job_stolen", "in_reply_to": 1, "thief": "w3", "victim": "w1", "job_id": "job2", "victim_queue_size": 2}}
```

## 参考资料

- [Work Stealing](https://en.wikipedia.org/wiki/Work_stealing)：Work stealing scheduling用于multi-threaded和分布式系统

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
