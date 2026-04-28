# Implement Node States (Leader, Follower, Candidate)

Website: <https://builddistributedsystem.com/tracks/elector/tasks/task-5-1-node-states>

Track: 5. The Elector
Task order: 1
Short title: Node States
Difficulty: intermediate
Subtrack: Raft Leader Election

## Problem

Implement the three states from Raft: Leader, Follower, and Candidate. Each node starts as a Follower. Candidates request votes. Leaders coordinate the cluster.

## Concept Notes

### Raft Roles

In Raft, every node is in one of three states: Follower (passive, responds to leaders), Candidate (seeking to become leader), or Leader (handles all client requests). This clear state machine simplifies reasoning about the protocol.

## Concepts

- state machine
- leader election
- Raft roles

## Hints

- Define an enum for states
- All nodes start as followers
- State transitions happen on specific events

## Test Cases

### 1. Node starts as follower

Input:

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1","n2","n3"]}}
{"src":"c0","dest":"n1","body":{"type":"get_state","msg_id":2}}
```

Expected output:

```text
{"src":"n1","dest":"c0","body":{"type":"init_ok","in_reply_to":1,"msg_id":0}}
{"src":"n1","dest":"c0","body":{"type":"state_reply","in_reply_to":2,"msg_id":1,"state":"follower","term":0}}
```

## Resources

- [Raft Paper](https://raft.github.io/raft.pdf): In Search of an Understandable Consensus Algorithm

## Java Starter

The matching local starter file is:

```text
src/main/java/Main.java
```
