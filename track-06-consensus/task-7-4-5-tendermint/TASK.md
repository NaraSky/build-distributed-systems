# Implement Tendermint-Style BFT Voting Rounds

Website: <https://builddistributedsystem.com/tracks/consensus/tasks/task-7-4-5-tendermint>

Track: 6. The Consensus
Task order: 20
Short title: Tendermint BFT
Difficulty: advanced
Subtrack: Byzantine Fault Tolerance

## Problem

Research and implement Tendermint-style BFT voting (used in Cosmos blockchain). Tendermint simplifies PBFT with clear round structure and a rotating proposer.

Round structure:
1. **Propose**: Round proposer broadcasts a block
2. **Prevote**: Each validator broadcasts prevote (for the block or nil)
3. **Precommit**: If 2/3+ prevotes for a block, broadcast precommit. If 2/3+ precommits, commit.

```json
Request:  {"type": "tendermint_propose", "msg_id": 1, "round": 0, "proposer": "v1", "block": {"height": 1, "txs": ["tx1", "tx2"]}}
Response: {"type": "tendermint_propose_ok", "in_reply_to": 1, "round": 0, "block_hash": "abc123"}

Request:  {"type": "tendermint_prevote", "msg_id": 2, "round": 0, "validator": "v2", "block_hash": "abc123"}
Response: {"type": "tendermint_prevote_ok", "in_reply_to": 2, "prevotes_for_block": 2, "total_prevotes": 3, "threshold": 3}

Request:  {"type": "tendermint_status", "msg_id": 3, "round": 0}
Response: {"type": "tendermint_status_ok", "in_reply_to": 3, "phase": "precommit", "block_committed": false, "prevote_count": 3, "precommit_count": 2}
```

## Concepts

- Tendermint
- Cosmos
- blockchain
- voting rounds
- lock mechanism

## Hints

- Tendermint simplifies PBFT by using rounds with a rotating proposer
- Each round has: Propose, Prevote, Precommit phases
- A block is committed when 2/3+ of validators precommit for it
- Validators lock on a value after precommitting (prevents equivocation across rounds)
- The lock is released only if a higher round proposes a different value with enough prevotes

## Test Cases

### 1. Proposer broadcasts block

tendermint_propose_ok should include round: 0 and a non-empty block_hash.

Input:

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1","n2","n3","n4"]}}
{"src":"c1","dest":"n1","body":{"type":"tendermint_propose","msg_id":2,"round":0,"proposer":"n1","block":{"height":1,"txs":["tx1"]}}}
```

Expected output:

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

### 2. Prevotes accumulate toward threshold

tendermint_prevote_ok should track prevotes_for_block count toward threshold of 2/3+.

Input:

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1","n2","n3","n4"]}}
{"src":"c1","dest":"n1","body":{"type":"tendermint_propose","msg_id":2,"round":0,"proposer":"n1","block":{"height":1,"txs":["tx1"]}}}
{"src":"c1","dest":"n1","body":{"type":"tendermint_prevote","msg_id":3,"round":0,"validator":"n2","block_hash":"abc"}}
```

Expected output:

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

## Resources

- [Tendermint: Byzantine Fault Tolerance in the Age of Blockchains](https://docs.tendermint.com/v0.34/introduction/what-is-tendermint.html): Tendermint BFT consensus used in Cosmos blockchain

## Java Starter

The matching local starter file is:

```text
src/main/java/Main.java
```
