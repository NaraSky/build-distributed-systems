# Prove the N >= 3f+1 Byzantine Fault Threshold

Website: <https://builddistributedsystem.com/tracks/consensus/tasks/task-7-4-4-bft-threshold>

Track: 6. The Consensus
Task order: 19
Short title: BFT Threshold
Difficulty: advanced
Subtrack: Byzantine Fault Tolerance

## Problem

Prove that tolerating f Byzantine faults requires at least N >= 3f+1 nodes. Then verify empirically.

The proof:
- We need two quorums to overlap in at least f+1 nodes (to guarantee at least 1 honest overlap)
- Quorum size Q must satisfy: 2Q - N > f (overlap > f)
- Q must also be > N - f (must include more than all correct nodes that might not respond)
- Solving: N >= 3f + 1

```json
Request:  {"type": "bft_threshold", "msg_id": 1, "f": 1}
Response: {"type": "bft_threshold_ok", "in_reply_to": 1, "f": 1, "min_n": 4, "quorum_size": 3, "honest_in_quorum": 2, "safe": true}

Request:  {"type": "bft_threshold", "msg_id": 2, "f": 2}
Response: {"type": "bft_threshold_ok", "in_reply_to": 2, "f": 2, "min_n": 7, "quorum_size": 5, "honest_in_quorum": 3, "safe": true}

Request:  {"type": "bft_test_insufficient", "msg_id": 3, "n": 3, "f": 1}
Response: {"type": "bft_test_insufficient_ok", "in_reply_to": 3, "sufficient": false, "reason": "3 < 3*1+1 = 4", "attack_possible": true}
```

## Concepts

- fault threshold
- 3f+1
- impossibility result
- Byzantine quorum

## Hints

- With N nodes and f Byzantine faults, correct nodes = N - f
- A quorum must be > (N + f) / 2 to guarantee overlap with honest nodes
- For N = 3f, you get exactly 2f correct nodes, but 2f-1 may affirm and f Byzantines may lie
- At 3f+1, a quorum of 2f+1 guarantees f+1 honest nodes in every quorum
- Test empirically: f=1 needs N=4, f=2 needs N=7

## Test Cases

### 1. f=1 requires N=4

Input:

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"bft_threshold","msg_id":2,"f":1}}
```

Expected output:

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
{"src": "n1", "dest": "c1", "body": {"type": "bft_threshold_ok", "in_reply_to": 2, "f": 1, "min_n": 4, "quorum_size": 3, "honest_in_quorum": 2, "safe": true, "msg_id": 1}}
```

### 2. f=2 requires N=7

Input:

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"bft_threshold","msg_id":2,"f":2}}
```

Expected output:

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
{"src": "n1", "dest": "c1", "body": {"type": "bft_threshold_ok", "in_reply_to": 2, "f": 2, "min_n": 7, "quorum_size": 5, "honest_in_quorum": 3, "safe": true, "msg_id": 1}}
```

## Resources

- [Byzantine Fault Tolerance Bounds](https://decentralizedthoughts.github.io/2019-06-17-the-threshold-adversary/): Why 3f+1 is the minimum for BFT consensus

## Java Starter

The matching local starter file is:

```text
src/main/java/Main.java
```
