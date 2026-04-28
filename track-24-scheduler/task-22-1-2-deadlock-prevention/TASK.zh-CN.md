# 实现 Deadlock Prevention in Scheduling

英文标题：Implement Deadlock Prevention in Scheduling
网页：<https://builddistributedsystem.com/tracks/scheduler/tasks/task-22-1-2-deadlock-prevention>

课程：24. 调度器：任务调度
任务序号：2
短标题：Deadlock Prevention
难度：advanced
子主题：Centralized Job Scheduling

## 中文导读

本题要求你完成 `实现 Deadlock Prevention in Scheduling`。

重点关注：`Banker's algorithm`、`safe state`、`wait-for graph`、`preemption`、`cycle detection`。

建议先按提示逐步实现：A system is in a safe state if there is an ordering in which all jobs can eventually complete。

协议字段、消息类型、输入输出格式请以本文件中的代码块和测试用例为准。

## 题目说明

Deadlock happens when two jobs each hold a resource the other needs, so neither can proceed. Prevention is better than detection: refuse any allocation that would leave the system in an unsafe state.

Implement a 节点 that manages resource allocation，包含deadlock prevention:

```JSON
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

## 涉及概念

- `Banker's algorithm`
- `safe state`
- `wait-for graph`
- `preemption`
- `cycle detection`

## 实现提示

- A system is in a safe state if there is an ordering in which all jobs can eventually complete
- Reject an allocation that would make the system unsafe (Banker's algorithm)
- Wait-for graph: edge A->B means A is waiting用于a resource currently held by B
- A cycle in the wait-for graph means deadlock exists
- Preempt a job that has been waiting beyond timeout_ms和free its held resources

## 测试用例

### 1. Detect deadlock cycle

Allocating all remaining resources to job2 would create unsafe state和should be denied.

输入：

```json
{"src":"client","dest":"scheduler","body":{"type":"init","msg_id":1,"resources":{"total_cpu":16,"total_memory":64}}}
{"src":"client","dest":"scheduler","body":{"type":"allocate_resources","msg_id":2,"job_id":"job1","resources":{"cpu":8,"memory":32}}}
{"src":"client","dest":"scheduler","body":{"type":"allocate_resources","msg_id":3,"job_id":"job2","resources":{"cpu":8,"memory":32}}}
```

期望输出：

```text
{"src": "scheduler", "dest": "client", "body": {"type": "init_ok", "in_reply_to": 1}}
```

### 2. Safe state allocation

Allocation that leaves system in safe state should be granted.

输入：

```json
{"src":"client","dest":"scheduler","body":{"type":"allocate_resources","msg_id":1,"job_id":"job1","resources":{"cpu":4,"memory":16}}}
```

期望输出：

```text
{"src": "scheduler", "dest": "client", "body": {"type": "allocation_ok", "in_reply_to": 1, "job_id": "job1", "safe_state": true}}
```

## 参考资料

- [Banker's Algorithm](https://en.wikipedia.org/wiki/Banker%27s_algorithm)：Dijkstra's algorithm用于safe resource allocation

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
