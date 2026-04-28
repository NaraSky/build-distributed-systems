# Prevent Split Votes Through Term Management

Website: <https://builddistributedsystem.com/tracks/elector/tasks/task-5-5-split-vote>

Track: 5. The Elector
Task order: 5
Short title: Term Management
Difficulty: advanced
Subtrack: Raft Leader Election

## Problem

Handle split votes where no candidate receives a majority. Candidates increment their term and retry. Proper term management ensures the cluster eventually elects a leader.

## Concept Notes

### Term Management

The term acts as a logical clock. Higher terms always win. When a node sees a higher term, it immediately becomes a follower. This prevents stale leaders from causing inconsistency.

## Concepts

- term
- split vote
- election retry

## Hints

- Increment term when starting election
- Step down if see higher term
- Retry election on timeout

## Test Cases

### 1. Increment term on new election

Node increments term from 1→2 when starting election, becomes candidate, votes for itself.

Input:

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1","n2","n3"]}}
{"src":"c0","dest":"n1","body":{"type":"set_term","msg_id":2,"term":1}}
{"src":"c0","dest":"n1","body":{"type":"trigger_election_timeout","msg_id":3}}
{"src":"c0","dest":"n1","body":{"type":"get_state","msg_id":4}}
```

Expected output:

```text
{"src":"n1","dest":"c0","body":{"type":"init_ok","in_reply_to":1,"msg_id":0}}
{"src":"n1","dest":"c0","body":{"type":"set_term_ok","in_reply_to":2,"msg_id":1}}
{"src":"n1","dest":"c0","body":{"type":"trigger_election_timeout_ok","in_reply_to":3,"msg_id":2}}
{"src":"n1","dest":"c0","body":{"type":"state_reply","in_reply_to":4,"msg_id":3,"state":"candidate","term":2}}
```

## Java Starter

The matching local starter file is:

```text
src/main/java/Main.java
```
