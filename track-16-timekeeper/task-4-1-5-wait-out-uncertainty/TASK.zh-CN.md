# 等待不确定性窗口以实现外部一致性

英文标题：Wait-Out-Uncertainty for External Consistency
网页：<https://builddistributedsystem.com/tracks/timekeeper/tasks/task-4-1-5-wait-out-uncertainty>

课程：16. 时间守卫：逻辑时钟
任务序号：5
短标题：等待不确定性
难度：高级
子主题：物理时间及其缺陷

## 中文导读

这道题让你实现 Spanner 的"提交等待"机制。核心思想很简单：在提交事务时，不要立刻返回，而是等一小段时间，直到你确定所有后来的事务都能看到你的提交。这段等待时间就是 TrueTime 的不确定性窗口。虽然等待会增加延迟，但它换来了外部一致性（External Consistency）——这是比线性一致性更强的保证。

## 题目说明

Spanner 通过"等待不确定性窗口"来实现外部一致性：在以时间戳 T 提交事务之前，必须等到 `TrueTime.now().earliest > T`，这样就能保证因果关系上更晚的事务一定能看到这次提交。

实现一个带有"等待不确定性"机制的 `commit` 消息处理器：
```json
Request:  {"type": "commit", "msg_id": 1, "key": "x", "value": "v1"}
Response: {"type": "commit_ok", "in_reply_to": 1, "commit_ts": 1234567, "wait_ms": 7}

Request:  {"type": "commit_stats", "msg_id": 2}
Response: {"type": "commit_stats_ok", "in_reply_to": 2, "total_commits": 5, "total_wait_ms": 35, "avg_wait_ms": 7}
```

## 涉及概念

- `external consistency`
- `commit wait`
- `Spanner`
- `linearizability`

## 实现提示

- 提交前，必须等待到 `TrueTime.now().earliest > commit_timestamp`
- 这保证了未来的任何读操作都能看到这次提交
- 等待时长等于不确定性窗口的大小
- 这就是 Spanner 在不使用锁的情况下实现外部一致性的方式
- 记录总等待时间，便于进行性能分析

## 测试用例

### 1. 提交并存储值

返回的 `commit_ok` 中应包含 `commit_ts` 和 `wait_ms`，随后通过 `kv_read_ok` 读取到 `value=v1`。

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"commit","msg_id":2,"key":"x","value":"v1"}}
{"src":"c1","dest":"n1","body":{"type":"kv_read","msg_id":3,"key":"x"}}
```

期望输出：

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

### 2. 无提交时查询统计信息

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"commit_stats","msg_id":2}}
```

期望输出：

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
{"src": "n1", "dest": "c1", "body": {"type": "commit_stats_ok", "total_commits": 0, "total_wait_ms": 0, "avg_wait_ms": 0, "in_reply_to": 2, "msg_id": 1}}
```

## 参考资料

- [Spanner Commit Wait](https://cloud.google.com/spanner/docs/true-time-external-consistency)：关于 TrueTime 提交等待机制的 Google Cloud 文档

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
