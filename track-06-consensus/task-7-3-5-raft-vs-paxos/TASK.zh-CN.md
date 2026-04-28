# Compare Raft vs Multi-Paxos

英文标题：Compare Raft vs Multi-Paxos
网页：<https://builddistributedsystem.com/tracks/consensus/tasks/task-7-3-5-raft-vs-paxos>

课程：6. 共识：Raft 与日志复制
任务序号：15
短标题：Raft vs Paxos
难度：intermediate
子主题：Paxos

## 中文导读

本题要求你完成 `Compare Raft vs Multi-Paxos`。

重点关注：`Raft`、`Multi-Paxos`、`message complexity`、`leader change cost`、`understandability`。

建议先按提示逐步实现：Raft restricts 日志 to be Leader-driven，包含no holes; Paxos allows out-of-order slots。

协议字段、消息类型、输入输出格式请以本文件中的代码块和测试用例为准。

## 题目说明

Compare Raft和Multi-Paxos across multiple dimensions. Both solve the same problem (replicated 日志) but make different design tradeoffs.

```JSON
请求:  {"type": "compare_consensus", "msg_id": 1}
响应: {"type": "compare_consensus_ok", "in_reply_to": 1, "comparison": {
    "raft": {"leader_change_cost": "O(uncommitted_entries)", "log_gaps": false, "understandability": "high", "production_users": ["etcd", "TiKV", "CockroachDB"]},
    "multi_paxos": {"leader_change_cost": "O(1) per slot", "log_gaps": true, "understandability": "low", "production_users": ["Chubby", "Spanner", "Megastore"]}
}}

请求:  {"type": "simulate_leader_change_cost", "msg_id": 2, "protocol": "raft", "uncommitted_entries": 50, "cluster_size": 5}
响应: {"type": "simulate_leader_change_cost_ok", "in_reply_to": 2, "messages_needed": 200, "rounds_needed": 50}

请求:  {"type": "simulate_leader_change_cost", "msg_id": 3, "protocol": "multi_paxos", "uncommitted_entries": 50, "cluster_size": 5}
响应: {"type": "simulate_leader_change_cost_ok", "in_reply_to": 3, "messages_needed": 8, "rounds_needed": 1}
```

## 涉及概念

- `Raft`
- `Multi-Paxos`
- `message complexity`
- `leader change cost`
- `understandability`

## 实现提示

- Raft restricts 日志 to be Leader-driven，包含no holes; Paxos allows out-of-order slots
- Raft Leader change: new Leader must replicate all uncommitted entries
- Paxos Leader change: only need Phase 1用于the next slot (cheaper)
- Raft is designed用于understandability; Paxos is designed用于generality
- Production systems: etcd uses Raft, Google Chubby uses Multi-Paxos

## 测试用例

### 1. Side-by-side comparison

compare_consensus_ok should show comparison object，包含raft和multi_paxos entries.

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"compare_consensus","msg_id":2}}
```

期望输出：

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

### 2. Raft Leader change cost scales，包含uncommitted

Raft 消息 needed should scale，包含uncommitted_entries * (cluster_size - 1).

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"simulate_leader_change_cost","msg_id":2,"protocol":"raft","uncommitted_entries":50,"cluster_size":5}}
```

期望输出：

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

## 参考资料

- [Paxos vs Raft: Have We Reached Consensus on Distributed Consensus?](https://arxiv.org/abs/2004.05074)：Academic comparison of Paxos和Raft design tradeoffs

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
