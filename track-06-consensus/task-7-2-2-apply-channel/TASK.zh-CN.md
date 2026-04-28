# 实现 the Apply Channel用于State Machine

英文标题：Implement the Apply Channel用于State Machine
网页：<https://builddistributedsystem.com/tracks/consensus/tasks/task-7-2-2-apply-channel>

课程：6. 共识：Raft 与日志复制
任务序号：7
短标题：Apply Channel
难度：intermediate
子主题：Commitment和Application

## 中文导读

本题要求你完成 `实现 the Apply Channel用于State Machine`。

重点关注：`apply channel`、`state machine`、`committed entries`、`deterministic replay`。

建议先按提示逐步实现：Committed entries flow into an apply channel in order。

协议字段、消息类型、输入输出格式请以本文件中的代码块和测试用例为准。

## 题目说明

Implement an apply channel that feeds committed 日志 entries to the state machine. The state machine is a simple key-value store that processes `Put`, `Get`,和`Delete` commands.

```JSON
请求:  {"type": "apply_entries", "msg_id": 1, "entries": [
    {"索引": 1, "term": 1, "command": {"op": "put", "key": "x", "value": "1"}},
    {"索引": 2, "term": 1, "command": {"op": "put", "key": "y", "value": "2"}},
    {"索引": 3, "term": 1, "command": {"op": "get", "key": "x"}}
]}
响应: {"type": "apply_entries_ok", "in_reply_to": 1, "results": [
    {"索引": 1, "result": "ok"},
    {"索引": 2, "result": "ok"},
    {"索引": 3, "result": "1"}
], "last_applied": 3}

请求:  {"type": "get_state", "msg_id": 2}
响应: {"type": "get_state_ok", "in_reply_to": 2, "state": {"x": "1", "y": "2"}, "last_applied": 3}
```

## 涉及概念

- `apply channel`
- `state machine`
- `committed entries`
- `deterministic replay`

## 实现提示

- Committed entries flow into an apply channel in order
- The state machine reads from the channel和applies commands sequentially
- Applied entries must never be re-applied (track lastApplied 索引)
- The state machine must be deterministic: same commands = same state
- Commands flow: 客户端 -> Leader 日志 -> replicated -> committed -> applied

## 测试用例

### 1. Apply put entries builds state

get_state_ok should show state: {"x": "hello"}, last_applied: 1.

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"apply_entries","msg_id":2,"entries":[{"index":1,"term":1,"command":{"op":"put","key":"x","value":"hello"}}]}}
{"src":"c1","dest":"n1","body":{"type":"get_state","msg_id":3}}
```

期望输出：

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

### 2. Apply get returns current value

apply_entries_ok results: 索引 1 result: ok, 索引 2 result: "42".

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"apply_entries","msg_id":2,"entries":[{"index":1,"term":1,"command":{"op":"put","key":"x","value":"42"}},{"index":2,"term":1,"command":{"op":"get","key":"x"}}]}}
```

期望输出：

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

## 参考资料

- [State Machine Replication](https://en.wikipedia.org/wiki/State_machine_replication)：How replicated state machines process deterministic commands from a 日志

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
