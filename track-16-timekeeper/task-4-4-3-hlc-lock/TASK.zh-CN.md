# 基于混合逻辑时钟实现分布式锁

英文标题：Implement a Distributed Lock Using HLC Timestamps
网页：<https://builddistributedsystem.com/tracks/timekeeper/tasks/task-4-4-3-hlc-lock>

课程：16. 时间守卫：逻辑时钟
任务序号：18
短标题：HLC 分布式锁
难度：高级
子主题：混合逻辑时钟

## 中文导读

本题要求你构建一个基于 HLC 时间戳的分布式锁。锁按照请求的 HLC 时间戳排序，时间戳最小的请求优先获得锁。这种方式提供了一个尊重因果关系的全序，是分布式系统中资源互斥访问的经典实现方案。

## 题目说明

构建一个分布式锁，锁的授予基于 HLC 时间戳。在请求队列中，拥有最小 HLC 时间戳的进程获得锁。这种方式提供了一个尊重因果关系的全序排列。

平局打破规则：按 `(pt, c, node_id)` 进行字典序比较。

请实现以下处理器：

```json
Request:  {"type": "lock_request", "msg_id": 1, "resource": "db_write", "requester": "n1", "hlc_pt": 1000, "hlc_c": 0}
Response: {"type": "lock_request_ok", "in_reply_to": 1, "position": 1, "granted": true}

Request:  {"type": "lock_request", "msg_id": 2, "resource": "db_write", "requester": "n2", "hlc_pt": 999, "hlc_c": 0}
Response: {"type": "lock_request_ok", "in_reply_to": 2, "position": 1, "granted": false, "reason": "lock_held_by_n1"}

Request:  {"type": "lock_release", "msg_id": 3, "resource": "db_write", "requester": "n1"}
Response: {"type": "lock_release_ok", "in_reply_to": 3, "next_holder": "n2"}

Request:  {"type": "lock_status", "msg_id": 4, "resource": "db_write"}
Response: {"type": "lock_status_ok", "in_reply_to": 4, "holder": "n2", "queue_size": 0}
```

## 涉及概念

- `distributed lock`
- `HLC timestamp`
- `request queue`
- `priority ordering`

## 实现提示

- 每个锁请求都附带请求者的 HLC 时间戳
- 锁会授予给拥有最小 HLC 时间戳的请求
- 使用 (pt, c, node_id) 作为全序来打破平局
- 维护一个按时间戳排序的等待队列
- 释放锁时，从队列中移除当前持有者，并将锁授予时间戳最小的下一个请求

## 测试用例

### 1. 第一个请求获得锁

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"lock_request","msg_id":2,"resource":"r1","requester":"n1","hlc_pt":1000,"hlc_c":0}}
```

期望输出：

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
{"src": "n1", "dest": "c1", "body": {"type": "lock_request_ok", "in_reply_to": 2, "position": 1, "granted": true, "msg_id": 1}}
```

### 2. 第二个请求在已持有的锁后面排队

第二个 `lock_request_ok` 应显示 granted 为 false。`lock_status_ok` 应显示 holder 为 n1，queue_size 为 1。

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"lock_request","msg_id":2,"resource":"r1","requester":"n1","hlc_pt":1000,"hlc_c":0}}
{"src":"c1","dest":"n1","body":{"type":"lock_request","msg_id":3,"resource":"r1","requester":"n2","hlc_pt":999,"hlc_c":0}}
{"src":"c1","dest":"n1","body":{"type":"lock_status","msg_id":4,"resource":"r1"}}
```

期望输出：

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
{"src": "n1", "dest": "c1", "body": {"type": "lock_request_ok", "in_reply_to": 2, "position": 1, "granted": true, "msg_id": 1}}
```

## 参考资料

- [Distributed Locking with Timestamps](https://martin.kleppmann.com/2016/02/08/how-to-do-distributed-locking.html)：Martin Kleppmann 关于分布式锁实现正确性的讨论

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
