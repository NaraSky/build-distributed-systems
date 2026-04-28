# Apply Committed Entries to State Machine

Website: <https://builddistributedsystem.com/tracks/consensus/tasks/task-6-4-state-machine>

Track: 6. The Consensus
Task order: 4
Short title: State Machine
Difficulty: intermediate
Subtrack: Raft Log Replication

## Problem

Apply committed log entries to the state machine:

1. Track lastApplied - highest entry applied to state machine
2. When commitIndex > lastApplied, apply entries in order
3. State machine executes each command
4. Increment lastApplied after each application

The state machine must be deterministic - same commands produce same state.

## Concept Notes

### State Machine Replication

Raft replicates a log; the state machine interprets it. Each node applies the same commands in the same order, so all nodes converge to the same state. This is the foundation of replicated services.

### Apply Order

Entries must be applied in index order. Gaps are not allowed - if entry 5 is committed but entry 4 is not, wait. In practice, commitment proceeds in order anyway.

## Concepts

- state machine
- apply
- determinism

## Hints

- Apply entries in order
- Track lastApplied index
- State machine must be deterministic

## Test Cases

### 1. Apply entries in order

State machine applies both entries in order. Final state: {x:1, y:2}, lastApplied=2.

Input:

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c0","dest":"n1","body":{"type":"seed_committed_log","msg_id":2,"entries":[{"index":1,"term":1,"command":{"op":"put","key":"x","value":1}},{"index":2,"term":1,"command":{"op":"put","key":"y","value":2}}],"commit_index":2}}
{"src":"c0","dest":"n1","body":{"type":"get_state","msg_id":3}}
```

Expected output:

```text
{"src":"n1","dest":"c0","body":{"type":"init_ok","in_reply_to":1,"msg_id":0}}
{"src":"n1","dest":"c0","body":{"type":"seed_committed_log_ok","in_reply_to":2,"msg_id":1}}
{"src":"n1","dest":"c0","body":{"type":"state_reply","in_reply_to":3,"msg_id":2,"state":{"x":1,"y":2},"last_applied":2}}
```

## Java Starter

The matching local starter file is:

```text
src/main/java/Main.java
```
