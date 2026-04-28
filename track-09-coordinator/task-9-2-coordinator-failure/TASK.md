# Handle Coordinator Failure

Website: <https://builddistributedsystem.com/tracks/coordinator/tasks/task-9-2-coordinator-failure>

Track: 9. The Coordinator
Task order: 2
Short title: Coordinator Failure
Difficulty: advanced
Subtrack: Two-Phase Commit

## Problem

Handle coordinator failures: log PREPARE before sending, log COMMIT/ABORT decision, recover from log.

## Concept Notes

### Write-Ahead Logging

Log decision before sending. On recovery, read log to resume. Participants in PREPARED are blocked until decision known.

## Concepts

- failure recovery
- blocking
- write-ahead log

## Hints

- Log before sending messages
- Recovery reads log state
- Participants query coordinator for decision

## Test Cases

### 1. Log transaction state before prepare

Coordinator writes decision to durable log (with fsync) BEFORE sending PREPARE/COMMIT/ABORT to participants

Input:

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
```

Expected output:

```text
{"src":"n1","dest":"c0","body":{"type":"init_ok","in_reply_to":1,"msg_id":0}}
```

## Java Starter

The matching local starter file is:

```text
src/main/java/Main.java
```
