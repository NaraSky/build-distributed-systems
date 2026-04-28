# Apply Committed Entries to State Machine

英文标题：Apply Committed Entries to State Machine
网页：<https://builddistributedsystem.com/tracks/consensus/tasks/task-6-4-state-machine>

课程：6. 共识：Raft 与日志复制
任务序号：4
短标题：State Machine
难度：intermediate
子主题：Raft 日志 复制

## 中文导读

本题要求你完成 `Apply Committed Entries to State Machine`。

重点关注：`state machine`、`apply`、`determinism`。

建议先按提示逐步实现：Apply entries in order。

协议字段、消息类型、输入输出格式请以本文件中的代码块和测试用例为准。

## 题目说明

Apply committed 日志 entries to the state machine:

1. Track lastApplied - highest entry applied to state machine
2. When commitIndex > lastApplied, apply entries in order
3. State machine executes each command
4. Increment lastApplied after each application

The state machine must be deterministic - same commands produce same state.

## 概念说明

### State Machine 复制

Raft replicates a 日志; the state machine interprets it. Each 节点 applies the same commands in the same order, so all 节点 converge to the same state. This is the foundation of replicated services.

### Apply Order

Entries must be applied in 索引 order. Gaps are not allowed - if entry 5 is committed but entry 4 is not, wait. In practice, commitment proceeds in order anyway.

## 涉及概念

- `state machine`
- `apply`
- `determinism`

## 实现提示

- Apply entries in order
- Track lastApplied 索引
- State machine must be deterministic

## 测试用例

### 1. Apply entries in order

State machine applies both entries in order. Final state: {x:1, y:2}, lastApplied=2.

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c0","dest":"n1","body":{"type":"seed_committed_log","msg_id":2,"entries":[{"index":1,"term":1,"command":{"op":"put","key":"x","value":1}},{"index":2,"term":1,"command":{"op":"put","key":"y","value":2}}],"commit_index":2}}
{"src":"c0","dest":"n1","body":{"type":"get_state","msg_id":3}}
```

期望输出：

```text
{"src":"n1","dest":"c0","body":{"type":"init_ok","in_reply_to":1,"msg_id":0}}
{"src":"n1","dest":"c0","body":{"type":"seed_committed_log_ok","in_reply_to":2,"msg_id":1}}
{"src":"n1","dest":"c0","body":{"type":"state_reply","in_reply_to":3,"msg_id":2,"state":{"x":1,"y":2},"last_applied":2}}
```

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
