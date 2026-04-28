# Implement Two-Phase Commit

Website: <https://builddistributedsystem.com/tracks/coordinator/tasks/task-9-1-two-phase-commit>

Track: 9. The Coordinator
Task order: 1
Short title: 2PC
Difficulty: advanced
Subtrack: Two-Phase Commit

## Problem

Implement 2PC: Phase 1 sends PREPARE, collects votes. Phase 2 sends COMMIT if all YES, else ABORT.

## Concept Notes

### Two-Phase Commit

2PC ensures all-or-nothing across nodes. The blocking problem: if coordinator crashes after PREPARE, participants are stuck.

## Concepts

- 2PC
- atomic commit
- prepare-commit

## Hints

- Phase 1: Prepare - ask all participants
- Phase 2: Commit/Abort based on votes
- Log decisions for recovery

## Test Cases

### 1. All participants vote yes

Coordinator sends PREPARE to all participants (p1, p2, p3). All vote YES. Coordinator decides COMMIT and sends to all.

Input:

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
```

Expected output:

```text
{"src":"n1","dest":"c0","body":{"type":"init_ok","in_reply_to":1,"msg_id":0}}
```

## Resources

- [DDIA Chapter 9](https://dataintensive.net/): Consistency and Consensus

## Java Starter

The matching local starter file is:

```text
src/main/java/Main.java
```
