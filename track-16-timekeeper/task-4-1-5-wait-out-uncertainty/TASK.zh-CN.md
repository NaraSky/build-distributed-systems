# Wait-Out-Uncertainty用于External Consistency

英文标题：Wait-Out-Uncertainty用于External Consistency
网页：<https://builddistributedsystem.com/tracks/timekeeper/tasks/task-4-1-5-wait-out-uncertainty>

课程：16. 时间守卫：逻辑时钟
任务序号：5
短标题：Wait Uncertainty
难度：advanced
子主题：Physical Time和Its Failures

## 中文导读

本题要求你完成 `Wait-Out-Uncertainty用于External Consistency`。

重点关注：`external consistency`、`commit wait`、`Spanner`、`linearizability`。

建议先按提示逐步实现：Before committing, wait until TrueTime.now().earliest > commit_timestamp。

协议字段、消息类型、输入输出格式请以本文件中的代码块和测试用例为准。

## 题目说明

Spanner achieves external consistency by waiting out the uncertainty window: before committing a 事务 at timestamp T, wait until `TrueTime.now().earliest > T`. This guarantees causally-later transactions see this commit.

Implement a `commit` handler，包含wait-out-uncertainty:
```JSON
请求:  {"type": "commit", "msg_id": 1, "key": "x", "value": "v1"}
响应: {"type": "commit_ok", "in_reply_to": 1, "commit_ts": 1234567, "wait_ms": 7}

请求:  {"type": "commit_stats", "msg_id": 2}
响应: {"type": "commit_stats_ok", "in_reply_to": 2, "total_commits": 5, "total_wait_ms": 35, "avg_wait_ms": 7}
```

## 涉及概念

- `external consistency`
- `commit wait`
- `Spanner`
- `linearizability`

## 实现提示

- Before committing, wait until TrueTime.now().earliest > commit_timestamp
- This guarantees that any future read will see this commit
- The wait duration equals the uncertainty window
- This is how Spanner achieves external consistency without locks
- Track total wait time用于performance analysis

## 测试用例

### 1. Commit stores value

commit_ok，包含commit_ts和wait_ms, then kv_read_ok，包含value=v1.

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

### 2. Commit stats，包含no commits

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

- [Spanner Commit Wait](https://cloud.google.com/spanner/docs/true-time-external-consistency)：Google Cloud documentation on TrueTime commit wait

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
