# 实现 Multi-Paxos用于an Infinite 日志

英文标题：Implement Multi-Paxos用于an Infinite Log
网页：<https://builddistributedsystem.com/tracks/consensus/tasks/task-7-3-4-multi-paxos>

课程：6. 共识：Raft 与日志复制
任务序号：14
短标题：Multi-Paxos
难度：advanced
子主题：Paxos

## 中文导读

本题要求你完成 `实现 Multi-Paxos用于an Infinite 日志`。

重点关注：`Multi-Paxos`、`infinite log`、`Phase 1 skip`、`stable leader`。

建议先按提示逐步实现：Multi-Paxos runs a separate Paxos instance用于each 日志 slot。

协议字段、消息类型、输入输出格式请以本文件中的代码块和测试用例为准。

## 题目说明

Extend single-decree Paxos to Multi-Paxos: an infinite 日志 where each slot is a separate Paxos instance.

Key optimization: once leadership is established, skip Phase 1用于subsequent slots. Only run Phase 2 (Accept) directly.

```JSON
请求:  {"type": "multi_paxos_propose", "msg_id": 1, "slot": 1, "value": "set x=1"}
响应: {"type": "multi_paxos_propose_ok", "in_reply_to": 1, "slot": 1, "phase1_skipped": false, "chosen": true, "value": "set x=1"}

请求:  {"type": "multi_paxos_propose", "msg_id": 2, "slot": 2, "value": "set y=2"}
响应: {"type": "multi_paxos_propose_ok", "in_reply_to": 2, "slot": 2, "phase1_skipped": true, "chosen": true, "value": "set y=2"}

请求:  {"type": "multi_paxos_log", "msg_id": 3}
响应: {"type": "multi_paxos_log_ok", "in_reply_to": 3, "日志": [
    {"slot": 1, "value": "set x=1", "status": "chosen"},
    {"slot": 2, "value": "set y=2", "status": "chosen"}
]}
```

## 涉及概念

- `Multi-Paxos`
- `infinite log`
- `Phase 1 skip`
- `stable leader`

## 实现提示

- Multi-Paxos runs a separate Paxos instance用于each 日志 slot
- Optimization: once a Leader is stable, skip Phase 1用于subsequent slots
- The Leader only needs Phase 2 (Accept/Accepted)用于new entries
- If the Leader changes, Phase 1 must be re-run用于the next slot
- This is essentially how Raft works but，包含Paxos terminology

## 测试用例

### 1. First slot requires Phase 1

multi_paxos_propose_ok should show phase1_skipped: false用于the first slot.

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"multi_paxos_propose","msg_id":2,"slot":1,"value":"cmd1"}}
```

期望输出：

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

### 2. Subsequent slots skip Phase 1

Second propose should show phase1_skipped: true since Leader is stable.

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"multi_paxos_propose","msg_id":2,"slot":1,"value":"cmd1"}}
{"src":"c1","dest":"n1","body":{"type":"multi_paxos_propose","msg_id":3,"slot":2,"value":"cmd2"}}
```

期望输出：

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

## 参考资料

- [Paxos Made Live - Google](https://research.google/pubs/pub33002/)：How Google implements Multi-Paxos in production (Chubby)

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
