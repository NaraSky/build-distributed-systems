# 实现 Tendermint 风格的拜占庭容错投票

网页：<https://builddistributedsystem.com/tracks/consensus/tasks/task-7-4-5-tendermint>

课程：6. 共识
任务序号：20
短标题：Tendermint BFT
难度：高级
子主题：拜占庭容错

## 中文导读

这道题要求你研究并实现 Tendermint 风格的拜占庭容错（BFT，Byzantine Fault Tolerance）投票机制，这是 Cosmos 区块链背后的共识算法。Tendermint 可以看作实用拜占庭容错（PBFT）的现代简化版：它把复杂的协议流程整理成了清晰的"轮次"结构，每轮由一个固定的提议者发起，经过三个阶段的投票最终达成共识。

## 题目说明

Tendermint 是一种拜占庭容错共识算法，广泛应用于 Cosmos 区块链生态。与传统的实用拜占庭容错协议相比，Tendermint 引入了更清晰的轮次结构和轮换提议者机制，使得协议更容易理解和实现。

每一轮投票分为三个阶段：

1. **提议阶段**：当轮的提议者向所有验证者（Validator）广播一个区块（Block）
2. **预投票阶段**：每个验证者对收到的区块进行审查，然后广播自己的预投票——要么投给该区块，要么投空票表示不认可
3. **预提交阶段**：如果超过三分之二的验证者对同一个区块投了赞成的预投票，则进入预提交。当超过三分之二的验证者发出了预提交消息，该区块被正式提交到链上

Tendermint 采用三分之二多数而非简单多数作为投票门槛，这与拜占庭容错理论中 `3f+1` 的节点要求相对应：即使存在恶意节点，只要恶意节点数量不超过总数的三分之一，协议仍然能保证安全。

验证者在预提交某个值之后会被"锁定"在这个值上，在后续轮次中不能投给其他值。这个锁定机制防止了恶意节点利用多轮投票来制造前后矛盾的结果。只有当更高轮次中有足够多的预投票支持了另一个值时，锁定才会被解除。

```json
Request:  {"type": "tendermint_propose", "msg_id": 1, "round": 0, "proposer": "v1", "block": {"height": 1, "txs": ["tx1", "tx2"]}}
Response: {"type": "tendermint_propose_ok", "in_reply_to": 1, "round": 0, "block_hash": "abc123"}

Request:  {"type": "tendermint_prevote", "msg_id": 2, "round": 0, "validator": "v2", "block_hash": "abc123"}
Response: {"type": "tendermint_prevote_ok", "in_reply_to": 2, "prevotes_for_block": 2, "total_prevotes": 3, "threshold": 3}

Request:  {"type": "tendermint_status", "msg_id": 3, "round": 0}
Response: {"type": "tendermint_status_ok", "in_reply_to": 3, "phase": "precommit", "block_committed": false, "prevote_count": 3, "precommit_count": 2}
```

## 涉及概念

- Tendermint
- Cosmos
- blockchain
- voting rounds
- lock mechanism

## 实现提示

- Tendermint 通过轮次机制和轮换提议者来简化拜占庭容错协议
- 每轮包含三个阶段：提议、预投票、预提交
- 当超过三分之二的验证者对同一个区块预提交时，该区块被正式提交
- 验证者在预提交后会锁定在该值上，防止跨轮次投出矛盾的票
- 只有当更高轮次提出了不同的值且获得了足够多的预投票支持时，锁定才会被解除

## 测试用例

### 1. 提议者广播区块

验证：响应中应包含轮次编号 0 和一个非空的区块哈希值。

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1","n2","n3","n4"]}}
{"src":"c1","dest":"n1","body":{"type":"tendermint_propose","msg_id":2,"round":0,"proposer":"n1","block":{"height":1,"txs":["tx1"]}}}
```

期望输出：

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

### 2. 预投票逐步累积至门槛

验证：响应中应追踪预投票的计数，以及距离三分之二门槛的进度。

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

- [Tendermint: Byzantine Fault Tolerance in the Age of Blockchains](https://docs.tendermint.com/v0.34/introduction/what-is-tendermint.html)：Tendermint 拜占庭容错共识协议介绍，应用于 Cosmos 区块链

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
