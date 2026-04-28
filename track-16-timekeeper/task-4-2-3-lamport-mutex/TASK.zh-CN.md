# 实现 Distributed Mutual Exclusion，包含Lamport Clocks

英文标题：Implement Distributed Mutual Exclusion，包含Lamport Clocks
网页：<https://builddistributedsystem.com/tracks/timekeeper/tasks/task-4-2-3-lamport-mutex>

课程：16. 时间守卫：逻辑时钟
任务序号：8
短标题：Lamport Mutex
难度：advanced
子主题：Lamport Clocks

## 中文导读

本题要求你完成 `实现 Distributed Mutual Exclusion，包含Lamport Clocks`。

重点关注：`distributed mutex`、`Lamport mutex`、`request queue`、`total ordering`。

建议先按提示逐步实现：Each 节点 maintains a priority 队列 of lock requests sorted by Lamport timestamp。

协议字段、消息类型、输入输出格式请以本文件中的代码块和测试用例为准。

## 题目说明

Lamport's mutual exclusion algorithm uses Lamport clocks to totally order lock requests. Each 节点 maintains a 请求 队列 sorted by (timestamp, node_id).

**Protocol:**
1. To **请求** the lock: 广播 a 请求(ts, node_id) to all other 节点, add to local 队列
2. On receiving 请求: add to 队列, send REPLY
3. To **enter critical section**: your 请求 must be at the head of the 队列 AND you must have received REPLY from every other 节点
4. To **release**: remove from 队列, 广播 RELEASE

Implement:
```JSON
请求:  {"type": "request_lock", "msg_id": 1}
响应: {"type": "request_lock_ok", "in_reply_to": 1, "position": 1, "ts": 1}

请求:  {"type": "lock_status", "msg_id": 2}
响应: {"type": "lock_status_ok", "in_reply_to": 2, "holding": false, "queue_size": 1, "队列": [{"ts": 1, "节点": "n1"}]}
```

## 涉及概念

- `distributed mutex`
- `Lamport mutex`
- `request queue`
- `total ordering`

## 实现提示

- Each 节点 maintains a priority 队列 of lock requests sorted by Lamport timestamp
- To 请求: 广播 请求 to all 节点, add self to 队列
- To release: 广播 RELEASE to all 节点, remove self from 队列
- A 节点 can enter CS when: its 请求 is at the head AND it has received replies from all others
- Use (timestamp, node_id) pairs用于total ordering to break ties

## 测试用例

### 1. Request lock adds to 队列

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

### 2. Lock status，包含empty 队列

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

- [Distributed Mutual Exclusion Algorithms](https://www.cs.uic.edu/~ajayk/Chapter9.pdf)：Overview of distributed mutex algorithms including Lamport

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
