# 实现 Paxos Commit Protocol

英文标题：Implement Paxos Commit Protocol
网页：<https://builddistributedsystem.com/tracks/coordinator/tasks/task-19-2-5-paxos-commit>

课程：9. 协调器：分布式事务
任务序号：10
短标题：Paxos Commit
难度：advanced
子主题：Three-Phase Commit (3PC)

## 中文导读

本题要求你完成 `实现 Paxos Commit Protocol`。

重点关注：`Paxos commit`、`consensus-based commit`、`no single point of failure`、`acceptors`、`proposers`。

建议先按提示逐步实现：Replace the coordinator，包含a Paxos group (acceptors)。

协议字段、消息类型、输入输出格式请以本文件中的代码块和测试用例为准。

## 题目说明

Paxos Commit replaces the single coordinator，包含a Paxos 共识 group. Each participant's commit decision is reached through Paxos, eliminating the single point of 故障.

**Architecture**:
- Each participant has its own Paxos instance deciding its commit/abort vote
- A proposer proposes "commit" or "abort" to each Paxos instance
- Once a value is chosen by Paxos, it cannot be undone
- No single coordinator 故障 point

**Paxos phases用于commit**:
```
For each participant P:
  Phase 1a (Prepare):  proposer → acceptors: Prepare(1)
  Phase 1b (Promise):  acceptors → proposer: Promise(1, prev_value_if_any)
  Phase 2a (Accept):   proposer → acceptors: Accept(1, "commit")
  Phase 2b (Accepted): acceptors → proposer: Accepted(1, "commit")
```

**Example Paxos Commit**:
```JSON
请求:  {"type": "paxos_commit_begin", "msg_id": 1, "participants": ["p1", "p2", "p3"], "acceptors": ["a1", "a2", "a3"], "operations": [{"transfer": 100, "from": "a", "to": "b"}]}

// Phase 1用于p1's decision:
{"type": "prepare", "msg_id": 2, "proposal_id": 1, "participant": "p1"}
{"type": "promise", "in_reply_to": 2, "acceptor": "a1", "proposal_id": 1, "accepted_value": null}
{"type": "promise", "in_reply_to": 2, "acceptor": "a2", "proposal_id": 1, "accepted_value": null}
{"type": "promise", "in_reply_to": 2, "acceptor": "a3", "proposal_id": 1, "accepted_value": null}

// Phase 2用于p1's decision:
{"type": "accept", "msg_id": 3, "proposal_id": 1, "participant": "p1", "value": "commit"}
{"type": "accepted", "in_reply_to": 3, "acceptor": "a1", "proposal_id": 1, "value": "commit"}
{"type": "accepted", "in_reply_to": 3, "acceptor": "a2", "proposal_id": 1, "value": "commit"}
{"type": "accepted", "in_reply_to": 3, "acceptor": "a3", "proposal_id": 1, "value": "commit"}

// Repeat用于p2, p3...
```

**Advantages over 2PC/3PC**:
- No single coordinator 故障 point
- Tolerates crash of any proposer (any proposer can 重试)
- Non-blocking as long as a majority of acceptors is available

**Disadvantages**:
- Higher latency: 2 round trips per participant
- Higher 消息 complexity: 4N 消息 per participant
- More complex implementation

## 涉及概念

- `Paxos commit`
- `consensus-based commit`
- `no single point of failure`
- `acceptors`
- `proposers`
- `learners`

## 实现提示

- Replace the coordinator，包含a Paxos group (acceptors)
- Each participant's vote is decided by its own Paxos instance
- Phase 1 (Prepare): proposer gets promises from acceptors
- Phase 2 (Accept): proposer sends value, acceptors accept if promised
- No single point of 故障: any proposer can drive the protocol

## 测试用例

### 1. Successful Paxos commit

All participants should reach commit decision through Paxos 共识.

输入：

```json
{"src":"c0","dest":"paxos_coord","body":{"type":"init","msg_id":1,"participants":["p1","p2","p3"],"acceptors":["a1","a2","a3"]}}
{"src":"c1","dest":"paxos_coord","body":{"type":"paxos_commit_begin","msg_id":2,"participants":["p1","p2","p3"],"acceptors":["a1","a2","a3"],"operations":[{"transfer":100,"from":"a","to":"b"}]}}
```

期望输出：

```text
{"src": "paxos_coord", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

### 2. Proposer crash recovery

New proposer should take over和complete Paxos rounds用于all participants.

输入：

```json
{"src":"c0","dest":"paxos_coord","body":{"type":"init","msg_id":1,"participants":["p1","p2"],"acceptors":["a1","a2","a3"]}}
{"src":"c1","dest":"paxos_coord","body":{"type":"paxos_commit_begin","msg_id":2,"participants":["p1","p2"],"acceptors":["a1","a2","a3"],"operations":[{"transfer":100,"from":"a","to":"b"}],"crash_proposer_after":"prepare"}}
{"src":"c2","dest":"paxos_coord","body":{"type":"recover_proposer","msg_id":3}}
```

期望输出：

```text
{"src": "paxos_coord", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

## 参考资料

- [Paxos Made Simple](https://www.microsoft.com/en-us/research/wp-content/uploads/2016/02/tr-2007-81.pdf)：Original Lamport Paxos paper

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
