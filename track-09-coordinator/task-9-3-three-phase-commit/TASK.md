# Implement Three-Phase Commit

Website: <https://builddistributedsystem.com/tracks/coordinator/tasks/task-9-3-three-phase-commit>

Track: 9. The Coordinator
Task order: 3
Short title: 3PC
Difficulty: advanced
Subtrack: Two-Phase Commit

## Problem

3PC adds PRE-COMMIT phase. If coordinator fails after PRE-COMMIT, participants can commit safely.

## Concept Notes

### Three-Phase Commit

3PC reduces blocking by adding PRE-COMMIT. Participants in PRE-COMMIT know decision was commit if coordinator fails.

## Concepts

- 3PC
- non-blocking
- pre-commit

## Hints

- Add PRE-COMMIT phase
- PRE-COMMIT indicates intent to commit
- Participants can proceed without coordinator

## Test Cases

### 1. Phase 1: Prepare

Coordinator n1 sends prepare to all participants (n2, n3, n4). All vote YES.

Input:

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1","n2","n3","n4"]}}
{"src":"c1","dest":"n1","body":{"type":"3pc_prepare","msg_id":2,"tx_id":"tx1","participants":["n2","n3","n4"],"operations":[{"key":"x","value":10}]}}
```

Expected output:

```text
{"src":"n1","dest":"c0","body":{"type":"init_ok","in_reply_to":1,"msg_id":0}}
{"src":"n1","dest":"c1","body":{"type":"3pc_prepare_ok","in_reply_to":2,"msg_id":1,"tx_id":"tx1","votes":{"n2":"yes","n3":"yes","n4":"yes"}}}
```

## Java Starter

The matching local starter file is:

```text
src/main/java/Main.java
```
