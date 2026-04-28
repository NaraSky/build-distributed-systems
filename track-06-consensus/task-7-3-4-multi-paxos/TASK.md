# Implement Multi-Paxos for an Infinite Log

Website: <https://builddistributedsystem.com/tracks/consensus/tasks/task-7-3-4-multi-paxos>

Track: 6. The Consensus
Task order: 14
Short title: Multi-Paxos
Difficulty: advanced
Subtrack: Paxos

## Problem

Extend single-decree Paxos to Multi-Paxos: an infinite log where each slot is a separate Paxos instance.

Key optimization: once leadership is established, skip Phase 1 for subsequent slots. Only run Phase 2 (Accept) directly.

```json
Request:  {"type": "multi_paxos_propose", "msg_id": 1, "slot": 1, "value": "set x=1"}
Response: {"type": "multi_paxos_propose_ok", "in_reply_to": 1, "slot": 1, "phase1_skipped": false, "chosen": true, "value": "set x=1"}

Request:  {"type": "multi_paxos_propose", "msg_id": 2, "slot": 2, "value": "set y=2"}
Response: {"type": "multi_paxos_propose_ok", "in_reply_to": 2, "slot": 2, "phase1_skipped": true, "chosen": true, "value": "set y=2"}

Request:  {"type": "multi_paxos_log", "msg_id": 3}
Response: {"type": "multi_paxos_log_ok", "in_reply_to": 3, "log": [
    {"slot": 1, "value": "set x=1", "status": "chosen"},
    {"slot": 2, "value": "set y=2", "status": "chosen"}
]}
```

## Concepts

- Multi-Paxos
- infinite log
- Phase 1 skip
- stable leader

## Hints

- Multi-Paxos runs a separate Paxos instance for each log slot
- Optimization: once a leader is stable, skip Phase 1 for subsequent slots
- The leader only needs Phase 2 (Accept/Accepted) for new entries
- If the leader changes, Phase 1 must be re-run for the next slot
- This is essentially how Raft works but with Paxos terminology

## Test Cases

### 1. First slot requires Phase 1

multi_paxos_propose_ok should show phase1_skipped: false for the first slot.

Input:

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"multi_paxos_propose","msg_id":2,"slot":1,"value":"cmd1"}}
```

Expected output:

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

### 2. Subsequent slots skip Phase 1

Second propose should show phase1_skipped: true since leader is stable.

Input:

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"multi_paxos_propose","msg_id":2,"slot":1,"value":"cmd1"}}
{"src":"c1","dest":"n1","body":{"type":"multi_paxos_propose","msg_id":3,"slot":2,"value":"cmd2"}}
```

Expected output:

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

## Resources

- [Paxos Made Live - Google](https://research.google/pubs/pub33002/): How Google implements Multi-Paxos in production (Chubby)

## Java Starter

The matching local starter file is:

```text
src/main/java/Main.java
```
