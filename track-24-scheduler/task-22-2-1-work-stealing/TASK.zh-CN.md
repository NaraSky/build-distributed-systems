# 实现工作窃取调度器

英文标题：Implement Work Stealing Scheduler
网页：<https://builddistributedsystem.com/tracks/scheduler/tasks/task-22-2-1-work-stealing>

课程：24. 任务调度器
任务序号：6
短标题：工作窃取
难度：高级
子主题：分布式任务分配

## 中文导读

这道题要求你实现工作窃取（Work Stealing）调度机制。在高并发场景下，所有节点都从同一个中央队列抢任务会造成严重的竞争瓶颈。工作窃取的做法是让每个节点维护自己的任务队列，空闲时主动去忙碌节点那里"偷"一个任务来做，从而在无需中央协调的情况下实现自动负载均衡。

## 题目说明

当成百上千个工作节点（Worker）同时争抢一个中央队列时，这个队列本身就成了性能瓶颈。工作窃取彻底消除了这个瓶颈：每个工作节点拥有自己的本地双端队列（Deque），独立处理自己队列中的任务。当某个节点做完了自己的所有任务，它就去一个忙碌节点的双端队列尾部"偷"一个任务过来。

你需要实现一个协调工作窃取的集群节点：

```json
// 空闲的 w3 从忙碌的工作节点窃取任务
{ "type": "steal_job", "msg_id": 1,
  "thief_worker": "w3", "busy_workers": ["w1","w2"] }
-> { "type": "job_stolen", "in_reply_to": 1,
    "thief": "w3", "victim": "w1",
    "job_id": "job2", "victim_queue_size": 2 }

// 检查整个集群是否空闲
{ "type": "check_cluster_state", "msg_id": 2 }
-> { "type": "cluster_state_ok", "in_reply_to": 2,
    "workers": {
      "w1": {"queue_size": 0, "state": "idle"},
      "w2": {"queue_size": 0, "state": "idle"},
      "w3": {"queue_size": 0, "state": "idle"}
    },
    "all_idle": true }
```

为什么要从队列尾部偷？因为队列的主人从头部取任务，而窃取者从尾部取，两者操作的是不同位置，几乎不会发生冲突。这种后进先出的窃取方式比从头部偷的竞争少大约 9 倍。

## 涉及概念

- work stealing
- deque
- LIFO stealing
- lock-free scheduling
- idle detection

## 实现提示

- 每个工作节点有自己的双端队列，从头部压入和弹出任务（利用后进先出特性提升缓存命中率）
- 空闲节点从随机选择的忙碌节点的队列尾部窃取一个任务
- 后进先出窃取：主人用头部，窃取者用尾部，两者很少冲突，竞争更少
- 当每个节点的队列都为空且没有正在执行的任务时，判定为全部空闲
- `steal_job` 从忙碌节点列表中随机选一个目标，取走其最后一个任务

## 测试用例

### 1. 工作窃取均衡负载

工作窃取应使各工作节点的利用率大致相等。

输入：

```json
{"src":"client","dest":"cluster","body":{"type":"init","msg_id":1,"workers":["w1","w2","w3"],"jobs_to_distribute":6}}
{"src":"client","dest":"cluster","body":{"type":"run_simulation","msg_id":2,"duration_ms":1000}}
```

期望输出：

```text
{"src": "cluster", "dest": "client", "body": {"type": "init_ok", "in_reply_to": 1}}
```

### 2. 从随机目标窃取

空闲节点应从随机选择的忙碌节点处窃取一个任务。

输入：

```json
{"src":"client","dest":"cluster","body":{"type":"steal_job","msg_id":1,"thief_worker":"w3","busy_workers":["w1","w2"]}}
```

期望输出：

```text
{"src": "cluster", "dest": "client", "body": {"type": "job_stolen", "in_reply_to": 1, "thief": "w3", "victim": "w1", "job_id": "job2", "victim_queue_size": 2}}
```

## 参考资料

- [Work Stealing](https://en.wikipedia.org/wiki/Work_stealing)：多线程和分布式系统中的工作窃取调度方法

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
