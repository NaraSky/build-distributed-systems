# 实现 a Distributed Lock使用HLC时间戳

英文标题：Implement a Distributed Lock使用HLC时间戳
网页：<https://builddistributedsystem.com/tracks/timekeeper/tasks/task-4-4-3-hlc-lock>

课程：16. 时间守卫：逻辑时钟
任务序号：18
短标题：HLC Lock
难度：advanced
子主题：混合逻辑 Clocks

## 中文导读

本题要求你完成 `实现 a Distributed Lock使用HLC时间戳`。

重点关注：`distributed lock`、`HLC timestamp`、`request queue`、`priority ordering`。

建议先按提示逐步实现：Each lock 请求 is stamped，包含the requester HLC timestamp。

协议字段、消息类型、输入输出格式请以本文件中的代码块和测试用例为准。

## 题目说明

Build a distributed lock where the lock is granted based on HLC timestamps. The process，包含the lowest HLC timestamp in the 请求 队列 gets the lock. This gives a total ordering that respects causality.

Tie-breaking: compare `(pt, c, node_id)` lexicographically.

Implement handlers:

```JSON
请求:  {"type": "lock_request", "msg_id": 1, "resource": "db_write", "requester": "n1", "hlc_pt": 1000, "hlc_c": 0}
响应: {"type": "lock_request_ok", "in_reply_to": 1, "position": 1, "granted": true}

请求:  {"type": "lock_request", "msg_id": 2, "resource": "db_write", "requester": "n2", "hlc_pt": 999, "hlc_c": 0}
响应: {"type": "lock_request_ok", "in_reply_to": 2, "position": 1, "granted": false, "reason": "lock_held_by_n1"}

请求:  {"type": "lock_release", "msg_id": 3, "resource": "db_write", "requester": "n1"}
响应: {"type": "lock_release_ok", "in_reply_to": 3, "next_holder": "n2"}

请求:  {"type": "lock_status", "msg_id": 4, "resource": "db_write"}
响应: {"type": "lock_status_ok", "in_reply_to": 4, "holder": "n2", "queue_size": 0}
```

## 涉及概念

- `distributed lock`
- `HLC timestamp`
- `request queue`
- `priority ordering`

## 实现提示

- Each lock 请求 is stamped，包含the requester HLC timestamp
- The lock is granted to the 请求，包含the lowest HLC timestamp
- Use (pt, c, node_id) as a total order to break ties
- Maintain a sorted 队列 of pending lock requests
- Release removes from the 队列和grants to the next lowest

## 测试用例

### 1. First request grants the lock

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

### 2. Second request queues behind held lock

Second lock_request_ok should show granted: false. lock_status_ok should show holder: n1, queue_size: 1.

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

- [Distributed Locking，包含Timestamps](https://martin.kleppmann.com/2016/02/08/how-to-do-distributed-locking.html)：Martin Kleppmann on correctness of distributed lock implementations

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
