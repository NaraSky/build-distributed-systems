# 实现基于租约的读操作

英文标题：Implement Lease-Based Reads
网页：<https://builddistributedsystem.com/tracks/store/tasks/task-8-2-2-lease-reads>

课程：7. 存储：线性一致键值存储
任务序号：7
短标题：Lease Reads
难度：高级
子主题：读优化

## 中文导读

这道题要求你实现基于租约（Lease）的读操作。与 ReadIndex 方案不同，租约读在租约有效期内完全不需要任何网络通信就能处理读请求，延迟极低。但这种方案依赖于节点之间的时钟偏差有界，需要你理解其中的权衡取舍。

## 题目说明

实现基于租约的读操作：领导者在持有有效租约期间，可以不经过任何网络通信直接处理读请求。同时需要记录这种方案所依赖的时钟假设。

```json
Request:  {"type": "lease_read", "msg_id": 1, "key": "x"}
Response: {"type": "lease_read_ok", "in_reply_to": 1, "value": "42", "lease_valid": true, "network_round_trips": 0}

Request:  {"type": "lease_read_config", "msg_id": 2, "lease_duration_ms": 3000, "election_timeout_ms": 5000, "max_clock_skew_ms": 500}
Response: {"type": "lease_read_config_ok", "in_reply_to": 2, "safe": true, "effective_lease_ms": 2500, "reason": "lease - clock_skew < election_timeout"}
```

## 涉及概念

- `lease reads`
- `clock assumption`
- `zero network round trips`
- `stale read risk`

## 实现提示

- 领导者利用租约在不进行任何网络通信的情况下直接处理读请求
- 在租约有效期内，领导者可以确信自己仍然是领导者
- 租约时长必须短于选举超时时间，否则可能读到过时数据
- 前提假设：节点之间的时钟偏差是有界的
- 如果时钟漂移过大，旧的领导者可能在新领导者已经选出后仍然处理读请求，导致返回过时数据

## 测试用例

### 1. 租约读实现零网络通信

验证 lease_read_ok 响应中 network_round_trips 为 0 且 lease_valid 为 true。

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1","n2","n3"]}}
{"src":"c1","dest":"n1","body":{"type":"lease_read","msg_id":2,"key":"x"}}
```

期望输出：

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

### 2. 安全的租约配置

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"lease_read_config","msg_id":2,"lease_duration_ms":3000,"election_timeout_ms":5000,"max_clock_skew_ms":500}}
```

期望输出：

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
{"src": "n1", "dest": "c1", "body": {"type": "lease_read_config_ok", "in_reply_to": 2, "safe": true, "effective_lease_ms": 2500, "msg_id": 1}}
```

## 参考资料

- [CockroachDB - Follower Reads and Lease Reads](https://www.cockroachlabs.com/docs/stable/architecture/reads-and-writes-overview.html)：CockroachDB 如何通过租约读实现低延迟

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
