# 对比 Raft 和 Multi-Paxos

英文标题：Compare Raft vs Multi-Paxos
网页：<https://builddistributedsystem.com/tracks/consensus/tasks/task-7-3-5-raft-vs-paxos>

课程：6. 共识
任务序号：15
短标题：Raft vs Paxos
难度：进阶
子主题：Paxos

## 中文导读

本题要求你从多个维度对比 Raft 和 Multi-Paxos 两种共识协议。它们解决的是同一个问题——复制日志，但在设计上做了不同的取舍。通过这道题，你将理解为什么有些系统选择了 Raft（如 etcd），而另一些选择了 Multi-Paxos（如 Google Chubby），以及它们各自的优缺点。

## 题目说明

从多个维度对比 Raft 和 Multi-Paxos。两者解决的是相同的问题（复制日志），但做了不同的设计取舍。

```json
Request:  {"type": "compare_consensus", "msg_id": 1}
Response: {"type": "compare_consensus_ok", "in_reply_to": 1, "comparison": {
    "raft": {"leader_change_cost": "O(uncommitted_entries)", "log_gaps": false, "understandability": "high", "production_users": ["etcd", "TiKV", "CockroachDB"]},
    "multi_paxos": {"leader_change_cost": "O(1) per slot", "log_gaps": true, "understandability": "low", "production_users": ["Chubby", "Spanner", "Megastore"]}
}}

Request:  {"type": "simulate_leader_change_cost", "msg_id": 2, "protocol": "raft", "uncommitted_entries": 50, "cluster_size": 5}
Response: {"type": "simulate_leader_change_cost_ok", "in_reply_to": 2, "messages_needed": 200, "rounds_needed": 50}

Request:  {"type": "simulate_leader_change_cost", "msg_id": 3, "protocol": "multi_paxos", "uncommitted_entries": 50, "cluster_size": 5}
Response: {"type": "simulate_leader_change_cost_ok", "in_reply_to": 3, "messages_needed": 8, "rounds_needed": 1}
```

## 概念说明

**日志空洞问题**：Raft 要求日志是连续的、没有空洞的，就像排队一样必须一个接一个。而 Paxos 允许日志中出现"空位"，不同的槽位可以乱序确认。Raft 的做法更容易理解和实现，但 Paxos 的方式在某些场景下更灵活。

**领导者切换开销**：当旧领导者下线、新领导者上任时，Raft 需要把所有未提交的日志条目都重新复制一遍，成本与未提交条目数量成正比。而 Multi-Paxos 只需要对下一个槽位重新执行第一阶段，开销小得多。

## 涉及概念

- `Raft`
- `Multi-Paxos`
- `message complexity`
- `leader change cost`
- `understandability`

## 实现提示

- Raft 要求日志由领导者驱动且不能有空洞；Paxos 允许槽位乱序提交
- Raft 的领导者切换：新领导者必须复制所有未提交的日志条目
- Paxos 的领导者切换：只需对下一个槽位执行第一阶段，代价更小
- Raft 的设计目标是易于理解；Paxos 的设计目标是通用性
- 生产系统中，etcd 使用 Raft，Google Chubby 使用 Multi-Paxos

## 测试用例

### 1. 并排对比两种协议

验证说明：响应中应包含 `raft` 和 `multi_paxos` 两个条目的对比信息。

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"compare_consensus","msg_id":2}}
```

期望输出：

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

### 2. Raft 领导者切换开销随未提交条目数增长

验证说明：Raft 所需的消息数应与 `uncommitted_entries * (cluster_size - 1)` 成正比。

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

- [Paxos vs Raft: Have We Reached Consensus on Distributed Consensus?](https://arxiv.org/abs/2004.05074)：学术界对 Paxos 和 Raft 设计取舍的系统性对比

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
