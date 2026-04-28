# 实现 Single-Decree Paxos Phase 1 (Prepare/Promise)

英文标题：Implement Single-Decree Paxos Phase 1 (Prepare/Promise)
网页：<https://builddistributedsystem.com/tracks/consensus/tasks/task-7-3-1-single-decree>

课程：6. 共识：Raft 与日志复制
任务序号：11
短标题：Paxos Phase 1
难度：advanced
子主题：Paxos

## 中文导读

本题要求你完成 `实现 Single-Decree Paxos Phase 1 (Prepare/Promise)`。

重点关注：`Paxos`、`single-decree`、`Prepare`、`Promise`、`proposal number`。

建议先按提示逐步实现：Phase 1: Proposer picks a unique proposal number n和sends Prepare(n) to acceptors。

协议字段、消息类型、输入输出格式请以本文件中的代码块和测试用例为准。

## 题目说明

Implement Phase 1 of single-decree Paxos (agree on one value).

Phase 1 (Prepare/Promise):
1. Proposer selects a unique proposal number `n`
2. Proposer sends `Prepare(n)` to all acceptors
3. Each acceptor: if `n > highest_promised`, set `highest_promised = n`和reply `Promise(n, accepted_value, accepted_n)`
4. If `n <= highest_promised`, reject

```JSON
请求:  {"type": "paxos_prepare", "msg_id": 1, "proposal_n": 1}
响应: {"type": "paxos_promise", "in_reply_to": 1, "promised": true, "accepted_n": null, "accepted_value": null}

请求:  {"type": "paxos_prepare", "msg_id": 2, "proposal_n": 5}
响应: {"type": "paxos_promise", "in_reply_to": 2, "promised": true, "accepted_n": null, "accepted_value": null}

请求:  {"type": "paxos_prepare", "msg_id": 3, "proposal_n": 3}
响应: {"type": "paxos_promise", "in_reply_to": 3, "promised": false, "reason": "already_promised_higher", "highest_promised": 5}
```

## 涉及概念

- `Paxos`
- `single-decree`
- `Prepare`
- `Promise`
- `proposal number`

## 实现提示

- Phase 1: Proposer picks a unique proposal number n和sends Prepare(n) to acceptors
- Acceptors respond，包含Promise(n, previously_accepted_value) if n > their highest seen
- If acceptor has already promised a higher n, it rejects the Prepare
- Proposal numbers must be globally unique (use node_id + sequence)
- A proposer needs promises from a majority to proceed to Phase 2

## 测试用例

### 1. First prepare is always promised

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"paxos_prepare","msg_id":2,"proposal_n":1}}
```

期望输出：

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
{"src": "n1", "dest": "c1", "body": {"type": "paxos_promise", "in_reply_to": 2, "promised": true, "accepted_n": null, "accepted_value": null, "msg_id": 1}}
```

### 2. Higher proposal supersedes lower

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"paxos_prepare","msg_id":2,"proposal_n":5}}
{"src":"c1","dest":"n1","body":{"type":"paxos_prepare","msg_id":3,"proposal_n":3}}
```

期望输出：

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
{"src": "n1", "dest": "c1", "body": {"type": "paxos_promise", "in_reply_to": 2, "promised": true, "accepted_n": null, "accepted_value": null, "msg_id": 1}}
{"src": "n1", "dest": "c1", "body": {"type": "paxos_promise", "in_reply_to": 3, "promised": false, "highest_promised": 5, "msg_id": 2}}
```

## 参考资料

- [Paxos Made Simple - Lamport](https://lamport.azurewebsites.net/pubs/paxos-simple.pdf)：Leslie Lamport simplified explanation of the Paxos algorithm

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
