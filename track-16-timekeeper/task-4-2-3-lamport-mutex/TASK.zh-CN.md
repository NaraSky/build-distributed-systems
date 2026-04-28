# 基于 Lamport 时钟实现分布式互斥

英文标题：Implement Distributed Mutual Exclusion with Lamport Clocks
网页：<https://builddistributedsystem.com/tracks/timekeeper/tasks/task-4-2-3-lamport-mutex>

课程：16. 时间守卫：逻辑时钟
任务序号：8
短标题：Lamport 互斥
难度：高级
子主题：Lamport 时钟

## 中文导读

这道题让你实现 Lamport 的分布式互斥算法。在分布式系统中，没有共享内存，也没有全局锁，如何保证同一时刻只有一个节点进入临界区？Lamport 的方案是：利用逻辑时钟为所有加锁请求排出一个全局顺序，每个节点维护一个按时间戳排序的请求队列，只有排在队首且收到所有其他节点回复的节点才能进入临界区。

## 题目说明

Lamport 互斥算法利用 Lamport 时钟对加锁请求进行全序排列。每个节点维护一个按 `(时间戳, 节点编号)` 排序的请求队列。

**协议流程：**
1. **请求加锁**：向所有其他节点广播 `REQUEST(ts, node_id)`，同时将请求加入本地队列
2. **收到请求**：将对方的请求加入队列，发送 `REPLY` 回复
3. **进入临界区**：当且仅当自己的请求在队列头部，且已收到所有其他节点的 `REPLY`
4. **释放锁**：从队列中移除自己的请求，向所有其他节点广播 `RELEASE`

实现以下消息处理器：
```json
Request:  {"type": "request_lock", "msg_id": 1}
Response: {"type": "request_lock_ok", "in_reply_to": 1, "position": 1, "ts": 1}

Request:  {"type": "lock_status", "msg_id": 2}
Response: {"type": "lock_status_ok", "in_reply_to": 2, "holding": false, "queue_size": 1, "queue": [{"ts": 1, "node": "n1"}]}
```

## 涉及概念

- `distributed mutex`
- `Lamport mutex`
- `request queue`
- `total ordering`

## 实现提示

- 每个节点维护一个优先级队列，按 Lamport 时间戳对加锁请求排序
- 请求加锁时：向所有节点广播请求，并将自己加入队列
- 释放锁时：向所有节点广播释放消息，并将自己从队列中移除
- 进入临界区的条件：自己的请求在队首，且已收到所有其他节点的回复
- 使用 `(时间戳, 节点编号)` 作为排序键来打破时间戳相同的平局

## 测试用例

### 1. 请求加锁后加入队列

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"request_lock","msg_id":2}}
{"src":"c1","dest":"n1","body":{"type":"lock_status","msg_id":3}}
```

期望输出：

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
{"src": "n1", "dest": "c1", "body": {"type": "request_lock_ok", "in_reply_to": 2, "position": 1, "ts": 1, "msg_id": 1}}
{"src": "n1", "dest": "c1", "body": {"type": "lock_status_ok", "in_reply_to": 3, "holding": true, "queue_size": 1, "queue": [{"ts": 1, "node": "n1"}], "msg_id": 2}}
```

### 2. 队列为空时查询锁状态

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"lock_status","msg_id":2}}
```

期望输出：

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
{"src": "n1", "dest": "c1", "body": {"type": "lock_status_ok", "in_reply_to": 2, "holding": false, "queue_size": 0, "queue": [], "msg_id": 1}}
```

## 参考资料

- [Distributed Mutual Exclusion Algorithms](https://www.cs.uic.edu/~ajayk/Chapter9.pdf)：分布式互斥算法综述，包括 Lamport 算法

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
