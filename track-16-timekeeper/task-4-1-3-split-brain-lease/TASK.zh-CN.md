# Simulate Split-Brain Caused by 时钟 Drift

英文标题：Simulate Split-Brain Caused by Clock Drift
网页：<https://builddistributedsystem.com/tracks/timekeeper/tasks/task-4-1-3-split-brain-lease>

课程：16. 时间守卫：逻辑时钟
任务序号：3
短标题：Split-Brain Lease
难度：advanced
子主题：Physical Time和Its Failures

## 中文导读

本题要求你完成 `Simulate Split-Brain Caused by 时钟 Drift`。

重点关注：`split-brain`、`lease`、`clock drift`、`leader election`。

建议先按提示逐步实现：A lease grants leadership用于a duration based on local 时钟。

协议字段、消息类型、输入输出格式请以本文件中的代码块和测试用例为准。

## 题目说明

Time-based leases break when clocks drift. Two 节点 can both believe they hold a valid lease simultaneously, causing **split-brain**.

Implement lease management，包含时钟 drift simulation:

```JSON
请求:  {"type": "acquire_lease", "msg_id": 1, "duration_ms": 5000}
响应: {"type": "acquire_lease_ok", "in_reply_to": 1, "expires_at": 1234572000}

请求:  {"type": "check_lease", "msg_id": 2}
响应: {"type": "check_lease_ok", "in_reply_to": 2, "valid": true, "remaining_ms": 3000}
```

## 涉及概念

- `split-brain`
- `lease`
- `clock drift`
- `leader election`

## 实现提示

- A lease grants leadership用于a duration based on local 时钟
- If two 节点 clocks drift apart, both may think their lease is valid
- This is the fundamental problem，包含time-based distributed locks
- Track lease state和detect overlapping valid leases
- Simulate by giving each 节点 a different 时钟 offset

## 测试用例

### 1. Acquire lease returns expires_at

acquire_lease_ok，包含expires_at > 0.

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"acquire_lease","msg_id":2,"duration_ms":5000}}
```

期望输出：

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

### 2. Check lease shows valid

check_lease_ok should have valid=true和remaining_ms > 0.

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"acquire_lease","msg_id":2,"duration_ms":60000}}
{"src":"c1","dest":"n1","body":{"type":"check_lease","msg_id":3}}
```

期望输出：

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

## 参考资料

- [How to do distributed locking](https://martin.kleppmann.com/2016/02/08/how-to-do-distributed-locking.html)：Kleppmann on time-based distributed locks和their 故障 modes

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
