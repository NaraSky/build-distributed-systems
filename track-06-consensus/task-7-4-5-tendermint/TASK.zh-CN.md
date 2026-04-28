# 实现 Tendermint-Style BFT Voting Rounds

英文标题：Implement Tendermint-Style BFT Voting Rounds
网页：<https://builddistributedsystem.com/tracks/consensus/tasks/task-7-4-5-tendermint>

课程：6. 共识：Raft 与日志复制
任务序号：20
短标题：Tendermint BFT
难度：advanced
子主题：Byzantine Fault Tolerance

## 中文导读

本题要求你完成 `实现 Tendermint-Style BFT Voting Rounds`。

重点关注：`Tendermint`、`Cosmos`、`blockchain`、`voting rounds`、`lock mechanism`。

建议先按提示逐步实现：Tendermint simplifies PBFT by使用rounds，包含a rotating proposer。

协议字段、消息类型、输入输出格式请以本文件中的代码块和测试用例为准。

## 题目说明

Research和implement Tendermint-style BFT voting (used in Cosmos blockchain). Tendermint simplifies PBFT，包含clear round structure和a rotating proposer.

Round structure:
1. **Propose**: Round proposer broadcasts a block
2. **Prevote**: Each validator broadcasts prevote (for the block or nil)
3. **Precommit**: If 2/3+ prevotes用于a block, 广播 precommit. If 2/3+ precommits, commit.

```JSON
请求:  {"type": "tendermint_propose", "msg_id": 1, "round": 0, "proposer": "v1", "block": {"height": 1, "txs": ["tx1", "tx2"]}}
响应: {"type": "tendermint_propose_ok", "in_reply_to": 1, "round": 0, "block_hash": "abc123"}

请求:  {"type": "tendermint_prevote", "msg_id": 2, "round": 0, "validator": "v2", "block_hash": "abc123"}
响应: {"type": "tendermint_prevote_ok", "in_reply_to": 2, "prevotes_for_block": 2, "total_prevotes": 3, "threshold": 3}

请求:  {"type": "tendermint_status", "msg_id": 3, "round": 0}
响应: {"type": "tendermint_status_ok", "in_reply_to": 3, "phase": "precommit", "block_committed": false, "prevote_count": 3, "precommit_count": 2}
```

## 涉及概念

- `Tendermint`
- `Cosmos`
- `blockchain`
- `voting rounds`
- `lock mechanism`

## 实现提示

- Tendermint simplifies PBFT by使用rounds，包含a rotating proposer
- Each round has: Propose, Prevote, Precommit phases
- A block is committed when 2/3+ of validators precommit用于it
- Validators lock on a value after precommitting (prevents equivocation across rounds)
- The lock is released only if a higher round proposes a different value，包含enough prevotes

## 测试用例

### 1. Proposer broadcasts block

tendermint_propose_ok should include round: 0和a non-empty block_hash.

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1","n2","n3","n4"]}}
{"src":"c1","dest":"n1","body":{"type":"tendermint_propose","msg_id":2,"round":0,"proposer":"n1","block":{"height":1,"txs":["tx1"]}}}
```

期望输出：

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

### 2. Prevotes accumulate toward threshold

tendermint_prevote_ok should track prevotes_for_block count toward threshold of 2/3+.

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1","n2","n3","n4"]}}
{"src":"c1","dest":"n1","body":{"type":"tendermint_propose","msg_id":2,"round":0,"proposer":"n1","block":{"height":1,"txs":["tx1"]}}}
{"src":"c1","dest":"n1","body":{"type":"tendermint_prevote","msg_id":3,"round":0,"validator":"n2","block_hash":"abc"}}
```

期望输出：

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

## 参考资料

- [Tendermint: Byzantine Fault Tolerance in the Age of Blockchains](https://docs.tendermint.com/v0.34/introduction/what-is-tendermint.html)：Tendermint BFT 共识 used in Cosmos blockchain

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
