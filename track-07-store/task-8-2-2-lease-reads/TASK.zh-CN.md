# 实现 Lease-Based Reads

英文标题：Implement Lease-Based Reads
网页：<https://builddistributedsystem.com/tracks/store/tasks/task-8-2-2-lease-reads>

课程：7. 存储：线性一致 KV Store
任务序号：7
短标题：Lease Reads
难度：advanced
子主题：Read Optimization

## 中文导读

本题要求你完成 `实现 Lease-Based Reads`。

重点关注：`lease reads`、`clock assumption`、`zero network round trips`、`stale read risk`。

建议先按提示逐步实现：The Leader uses its lease to serve reads without any 网络 round trips。

协议字段、消息类型、输入输出格式请以本文件中的代码块和测试用例为准。

## 题目说明

Implement lease-based reads: the Leader uses its active lease to serve reads without 网络 round trips. Document the 时钟 assumption required.

```JSON
请求:  {"type": "lease_read", "msg_id": 1, "key": "x"}
响应: {"type": "lease_read_ok", "in_reply_to": 1, "value": "42", "lease_valid": true, "network_round_trips": 0}

请求:  {"type": "lease_read_config", "msg_id": 2, "lease_duration_ms": 3000, "election_timeout_ms": 5000, "max_clock_skew_ms": 500}
响应: {"type": "lease_read_config_ok", "in_reply_to": 2, "safe": true, "effective_lease_ms": 2500, "reason": "lease - clock_skew < election_timeout"}
```

## 涉及概念

- `lease reads`
- `clock assumption`
- `zero network round trips`
- `stale read risk`

## 实现提示

- The Leader uses its lease to serve reads without any 网络 round trips
- During the lease, the Leader is guaranteed to still be Leader
- Lease duration must be shorter than election 超时 to prevent stale reads
- Assumption: bounded 时钟 skew between 节点
- If clocks drift too much, a stale Leader may serve reads after a new Leader is elected

## 测试用例

### 1. Lease read，包含zero round trips

lease_read_ok should show network_round_trips: 0和lease_valid: true.

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1","n2","n3"]}}
{"src":"c1","dest":"n1","body":{"type":"lease_read","msg_id":2,"key":"x"}}
```

期望输出：

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

### 2. Safe lease configuration

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

- [CockroachDB - Follower Reads和Lease Reads](https://www.cockroachlabs.com/docs/stable/architecture/reads-and-writes-overview.html)：How CockroachDB implements lease-based reads用于low latency

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
