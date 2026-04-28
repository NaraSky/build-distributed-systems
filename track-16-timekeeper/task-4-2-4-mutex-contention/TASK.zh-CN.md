# Simulate并发Mutex Requests from Multiple Nodes

英文标题：Simulate并发Mutex Requests from Multiple Nodes
网页：<https://builddistributedsystem.com/tracks/timekeeper/tasks/task-4-2-4-mutex-contention>

课程：16. 时间守卫：逻辑时钟
任务序号：9
短标题：Mutex Contention
难度：advanced
子主题：Lamport Clocks

## 中文导读

本题要求你完成 `Simulate并发Mutex Requests from Multiple Nodes`。

重点关注：`contention`、`fairness`、`wait time`、`queue ordering`。

建议先按提示逐步实现：When multiple 节点 请求 simultaneously, the one，包含the lowest (ts, node_id) wins。

协议字段、消息类型、输入输出格式请以本文件中的代码块和测试用例为准。

## 题目说明

Simulate 5 节点 all requesting the mutex simultaneously. With Lamport's algorithm, only one can hold it at a time. The 请求，包含the lowest (timestamp, node_id) pair wins.

Your task is to process multiple lock requests和verify mutual exclusion:

```JSON
请求:  {"type": "multi_request", "msg_id": 1, "requests": [
    {"节点": "n1", "ts": 3}, {"节点": "n2", "ts": 1}, {"节点": "n3", "ts": 3},
    {"节点": "n4", "ts": 2}, {"节点": "n5", "ts": 1}
]}
响应: {"type": "multi_request_ok", "in_reply_to": 1, "grant_order": ["n2","n5","n4","n1","n3"],
           "violations": 0}
```

Also implement a `release_lock` handler:
```JSON
请求:  {"type": "release_lock", "msg_id": 2, "节点": "n2"}
响应: {"type": "release_lock_ok", "in_reply_to": 2, "next_holder": "n5"}
```

## 涉及概念

- `contention`
- `fairness`
- `wait time`
- `queue ordering`

## 实现提示

- When multiple 节点 请求 simultaneously, the one，包含the lowest (ts, node_id) wins
- Track how long each 节点 waits before acquiring the lock
- Verify mutual exclusion: only one holder at a time
- After release, the next 节点 in the 队列 should be able to acquire
- Report average和max wait times across all requests

## 测试用例

### 1. Multi request orders by (ts, node_id)

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

### 2. Single request gets immediate grant

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

- [Mutual Exclusion in Distributed Systems](https://www.cs.helsinki.fi/group/cosco/Teaching/2012/DS-lect/Lect09.pdf)：Lecture on distributed mutual exclusion和contention handling

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
