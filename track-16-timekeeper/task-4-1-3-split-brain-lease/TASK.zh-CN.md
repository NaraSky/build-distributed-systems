# 模拟时钟漂移导致的脑裂问题

英文标题：Simulate Split-Brain Caused by Clock Drift
网页：<https://builddistributedsystem.com/tracks/timekeeper/tasks/task-4-1-3-split-brain-lease>

课程：16. 时间守卫：逻辑时钟
任务序号：3
短标题：脑裂与租约
难度：高级
子主题：物理时间及其缺陷

## 中文导读

这道题让你亲手模拟分布式系统中一个经典的灾难场景——脑裂（Split-Brain）。想象两个节点（Node）各自持有一个基于本地时钟的租约（Lease），当两台机器的时钟发生漂移时，它们可能同时认为自己的租约有效，从而都以为自己是"领导者"。这就是为什么基于时间的分布式锁天然不可靠，理解这一点对学习分布式系统至关重要。

## 题目说明

基于时间的租约机制在时钟漂移（Clock Drift）时会失效。当两个节点的时钟不同步时，它们可能同时认为自己持有有效的租约，从而导致**脑裂**。

你需要实现带有时钟漂移模拟功能的租约管理：

```json
Request:  {"type": "acquire_lease", "msg_id": 1, "duration_ms": 5000}
Response: {"type": "acquire_lease_ok", "in_reply_to": 1, "expires_at": 1234572000}

Request:  {"type": "check_lease", "msg_id": 2}
Response: {"type": "check_lease_ok", "in_reply_to": 2, "valid": true, "remaining_ms": 3000}
```

## 涉及概念

- `split-brain`
- `lease`
- `clock drift`
- `leader election`

## 实现提示

- 租约基于本地时钟授予一段时间的领导权
- 如果两个节点的时钟发生漂移，它们可能同时认为自己的租约有效
- 这是基于时间的分布式锁的根本性问题
- 需要跟踪租约状态，并检测是否存在重叠的有效租约
- 可以通过给每个节点设置不同的时钟偏移量来模拟时钟漂移

## 测试用例

### 1. 获取租约并返回过期时间

返回的 `acquire_lease_ok` 中应包含 `expires_at > 0`。

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"acquire_lease","msg_id":2,"duration_ms":5000}}
```

期望输出：

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

### 2. 检查租约显示有效

返回的 `check_lease_ok` 中应包含 `valid=true` 且 `remaining_ms > 0`。

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

- [How to do distributed locking](https://martin.kleppmann.com/2016/02/08/how-to-do-distributed-locking.html)：Martin Kleppmann 关于基于时间的分布式锁及其失败模式的分析

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
