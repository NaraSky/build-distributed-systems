# 模拟多节点并发互斥请求

英文标题：Simulate Concurrent Mutex Requests from Multiple Nodes
网页：<https://builddistributedsystem.com/tracks/timekeeper/tasks/task-4-2-4-mutex-contention>

课程：16. 时间守卫：逻辑时钟
任务序号：9
短标题：互斥竞争
难度：高级
子主题：Lamport 时钟

## 中文导读

这道题模拟的是一个高竞争场景：5 个节点同时请求互斥锁。在 Lamport 算法中，同一时刻只能有一个节点持有锁，那么当多个请求同时到达时，谁先获得锁？答案是按 `(时间戳, 节点编号)` 排序——时间戳最小的优先，时间戳相同则节点编号小的优先。通过这道题，你可以直观感受分布式互斥中的竞争和公平性问题。

## 题目说明

模拟 5 个节点同时请求互斥锁的场景。在 Lamport 算法下，同一时刻只有一个节点可以持有锁。拥有最小 `(时间戳, 节点编号)` 对的请求会最先获得锁。

你的任务是处理多个加锁请求，并验证互斥性：

```json
Request:  {"type": "multi_request", "msg_id": 1, "requests": [
    {"node": "n1", "ts": 3}, {"node": "n2", "ts": 1}, {"node": "n3", "ts": 3},
    {"node": "n4", "ts": 2}, {"node": "n5", "ts": 1}
]}
Response: {"type": "multi_request_ok", "in_reply_to": 1, "grant_order": ["n2","n5","n4","n1","n3"],
           "violations": 0}
```

同时实现 `release_lock` 消息处理器：
```json
Request:  {"type": "release_lock", "msg_id": 2, "node": "n2"}
Response: {"type": "release_lock_ok", "in_reply_to": 2, "next_holder": "n5"}
```

## 涉及概念

- `contention`
- `fairness`
- `wait time`
- `queue ordering`

## 实现提示

- 当多个节点同时请求锁时，拥有最小 `(时间戳, 节点编号)` 的节点优先获得锁
- 跟踪每个节点从请求到获得锁的等待时间
- 验证互斥性：任意时刻只有一个节点持有锁
- 释放锁后，队列中的下一个节点应自动获得锁
- 统计并报告所有请求的平均和最大等待时间

## 测试用例

### 1. 批量请求按 (时间戳, 节点编号) 排序

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"multi_request","msg_id":2,"requests":[{"node":"n1","ts":3},{"node":"n2","ts":1},{"node":"n3","ts":3},{"node":"n4","ts":2},{"node":"n5","ts":1}]}}
```

期望输出：

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
{"src": "n1", "dest": "c1", "body": {"type": "multi_request_ok", "in_reply_to": 2, "grant_order": ["n2", "n5", "n4", "n1", "n3"], "violations": 0, "msg_id": 1}}
```

### 2. 单个请求立即获得锁

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"multi_request","msg_id":2,"requests":[{"node":"n1","ts":1}]}}
```

期望输出：

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
{"src": "n1", "dest": "c1", "body": {"type": "multi_request_ok", "in_reply_to": 2, "grant_order": ["n1"], "violations": 0, "msg_id": 1}}
```

## 参考资料

- [Mutual Exclusion in Distributed Systems](https://www.cs.helsinki.fi/group/cosco/Teaching/2012/DS-lect/Lect09.pdf)：关于分布式互斥与竞争处理的课程讲义

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
