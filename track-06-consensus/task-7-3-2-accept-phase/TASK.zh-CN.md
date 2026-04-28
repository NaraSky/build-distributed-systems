# 实现 Paxos Phase 2 (Accept/Accepted)

英文标题：Implement Paxos Phase 2 (Accept/Accepted)
网页：<https://builddistributedsystem.com/tracks/consensus/tasks/task-7-3-2-accept-phase>

课程：6. 共识：Raft 与日志复制
任务序号：12
短标题：Paxos Phase 2
难度：advanced
子主题：Paxos

## 中文导读

本题要求你完成 `实现 Paxos Phase 2 (Accept/Accepted)`。

重点关注：`Paxos`、`Accept`、`Accepted`、`value selection`、`consensus`。

建议先按提示逐步实现：Phase 2: Proposer sends Accept(n, v) to acceptors。

协议字段、消息类型、输入输出格式请以本文件中的代码块和测试用例为准。

## 题目说明

Implement Phase 2 of Paxos. After getting a majority of promises in Phase 1, the proposer sends `Accept(n, v)` to acceptors.

Value selection rule: if any promise included a previously accepted value, the proposer MUST use the value，包含the highest accepted_n. Otherwise, the proposer chooses freely.

```JSON
请求:  {"type": "paxos_accept", "msg_id": 1, "proposal_n": 5, "value": "consensus_value"}
响应: {"type": "paxos_accepted", "in_reply_to": 1, "accepted": true, "proposal_n": 5, "value": "consensus_value"}

请求:  {"type": "paxos_accept", "msg_id": 2, "proposal_n": 3, "value": "late_value"}
响应: {"type": "paxos_accepted", "in_reply_to": 2, "accepted": false, "reason": "promised_higher", "highest_promised": 5}

请求:  {"type": "paxos_chosen", "msg_id": 3}
响应: {"type": "paxos_chosen_ok", "in_reply_to": 3, "value": "consensus_value", "chosen_at_n": 5}
```

## 涉及概念

- `Paxos`
- `Accept`
- `Accepted`
- `value selection`
- `consensus`

## 实现提示

- Phase 2: Proposer sends Accept(n, v) to acceptors
- v = highest accepted_value from Phase 1 promises, or proposer choice if none
- Acceptors accept if n >= highest_promised
- Once a majority accepts, the value is chosen (共识 reached)
- A chosen value can never be changed by future proposals

## 测试用例

### 1. Accept succeeds after promise

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"paxos_prepare","msg_id":2,"proposal_n":5}}
{"src":"c1","dest":"n1","body":{"type":"paxos_accept","msg_id":3,"proposal_n":5,"value":"hello"}}
```

期望输出：

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
{"src": "n1", "dest": "c1", "body": {"type": "paxos_promise", "in_reply_to": 2, "promised": true, "accepted_n": null, "accepted_value": null, "msg_id": 1}}
{"src": "n1", "dest": "c1", "body": {"type": "paxos_accepted", "in_reply_to": 3, "accepted": true, "proposal_n": 5, "value": "hello", "msg_id": 2}}
```

### 2. Accept rejected用于lower proposal

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"paxos_prepare","msg_id":2,"proposal_n":5}}
{"src":"c1","dest":"n1","body":{"type":"paxos_accept","msg_id":3,"proposal_n":3,"value":"old"}}
```

期望输出：

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
{"src": "n1", "dest": "c1", "body": {"type": "paxos_promise", "in_reply_to": 2, "promised": true, "accepted_n": null, "accepted_value": null, "msg_id": 1}}
{"src": "n1", "dest": "c1", "body": {"type": "paxos_accepted", "in_reply_to": 3, "accepted": false, "highest_promised": 5, "msg_id": 2}}
```

## 参考资料

- [Understanding Paxos](https://www.cs.rutgers.edu/~pxk/417/notes/paxos.html)：Step-by-step walkthrough of the Paxos protocol phases

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
