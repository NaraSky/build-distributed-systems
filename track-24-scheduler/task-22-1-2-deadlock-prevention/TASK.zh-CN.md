# 实现调度中的死锁预防

英文标题：Implement Deadlock Prevention in Scheduling
网页：<https://builddistributedsystem.com/tracks/scheduler/tasks/task-22-1-2-deadlock-prevention>

课程：24. 任务调度器
任务序号：2
短标题：死锁预防
难度：高级
子主题：集中式任务调度

## 中文导读

这道题要求你实现死锁预防（Deadlock Prevention）机制。死锁就像两个人各拿着对方需要的东西互不相让，谁也走不了。预防胜于检测：在分配资源前先判断是否安全，如果会导致不安全状态就直接拒绝，从根源上避免死锁发生。

## 题目说明

死锁（Deadlock）发生在两个任务互相持有对方所需的资源，导致双方都无法继续执行。预防优于检测：拒绝任何会使系统进入不安全状态的资源分配请求。

实现一个管理资源分配并预防死锁的节点：

```json
// 初始化资源池
{ "type": "init", "msg_id": 1,
  "resources": {"total_cpu": 16, "total_memory": 64} }
-> { "type": "init_ok", "in_reply_to": 1 }

// 安全分配：系统仍处于安全状态
{ "type": "allocate_resources", "msg_id": 2,
  "job_id": "job1", "resources": {"cpu": 4, "memory": 16} }
-> { "type": "allocation_ok", "in_reply_to": 2,
    "job_id": "job1", "safe_state": true }

// 会耗尽资源 -> 不安全 -> 拒绝
{ "type": "allocate_resources", "msg_id": 3,
  "job_id": "job2", "resources": {"cpu": 8, "memory": 32} }
-> denied

// 等待超时 -> 抢占
{ "type": "allocate_resources", "msg_id": 4,
  "job_id": "job3", "resources": {"cpu": 16, "memory": 64}, "timeout_ms": 5000 }
-> { "type": "allocation_timeout", "in_reply_to": 4,
    "job_id": "job3", "action": "preempted" }

// 查看等待图
{ "type": "get_wait_graph", "msg_id": 5 }
-> { "type": "wait_graph_ok", "in_reply_to": 5,
    "graph": {"job1":["job3"],"job2":["job1"],"job3":["job2"]},
    "has_cycle": true }
```

## 涉及概念

- Banker's algorithm
- safe state
- wait-for graph
- preemption
- cycle detection

## 实现提示

- 安全状态是指存在一种调度顺序，使得所有任务最终都能完成
- 如果某次分配会使系统进入不安全状态，则拒绝该请求（银行家算法）
- 等待图（Wait-for Graph）：边 A->B 表示 A 正在等待 B 当前持有的资源
- 等待图中如果出现环，说明存在死锁
- 对于等待超过 `timeout_ms` 的任务，执行抢占并释放其持有的资源

## 测试用例

### 1. 检测死锁环路

将所有剩余资源分配给 job2 会使系统进入不安全状态，应被拒绝。

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

### 2. 安全状态下的分配

不会导致不安全状态的资源分配应被批准。

输入：

```json
{"src":"client","dest":"scheduler","body":{"type":"allocate_resources","msg_id":1,"job_id":"job1","resources":{"cpu":4,"memory":16}}}
```

期望输出：

```text
{"src": "scheduler", "dest": "client", "body": {"type": "allocation_ok", "in_reply_to": 1, "job_id": "job1", "safe_state": true}}
```

## 参考资料

- [Banker's Algorithm](https://en.wikipedia.org/wiki/Banker%27s_algorithm)：Dijkstra 提出的安全资源分配算法

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
