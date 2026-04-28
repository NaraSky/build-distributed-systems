# Compare Raft vs Multi-Paxos

Website: <https://builddistributedsystem.com/tracks/consensus/tasks/task-7-3-5-raft-vs-paxos>

Track: 6. The Consensus
Task order: 15
Short title: Raft vs Paxos
Difficulty: intermediate
Subtrack: Paxos

## Problem

Compare Raft and Multi-Paxos across multiple dimensions. Both solve the same problem (replicated log) but make different design tradeoffs.

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

## Concepts

- Raft
- Multi-Paxos
- message complexity
- leader change cost
- understandability

## Hints

- Raft restricts log to be leader-driven with no holes; Paxos allows out-of-order slots
- Raft leader change: new leader must replicate all uncommitted entries
- Paxos leader change: only need Phase 1 for the next slot (cheaper)
- Raft is designed for understandability; Paxos is designed for generality
- Production systems: etcd uses Raft, Google Chubby uses Multi-Paxos

## Test Cases

### 1. Side-by-side comparison

compare_consensus_ok should show comparison object with raft and multi_paxos entries.

Input:

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"compare_consensus","msg_id":2}}
```

Expected output:

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

### 2. Raft leader change cost scales with uncommitted

Raft messages needed should scale with uncommitted_entries * (cluster_size - 1).

Input:

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"simulate_leader_change_cost","msg_id":2,"protocol":"raft","uncommitted_entries":50,"cluster_size":5}}
```

Expected output:

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

## Resources

- [Paxos vs Raft: Have We Reached Consensus on Distributed Consensus?](https://arxiv.org/abs/2004.05074): Academic comparison of Paxos and Raft design tradeoffs

## Java Starter

The matching local starter file is:

```text
src/main/java/Main.java
```
