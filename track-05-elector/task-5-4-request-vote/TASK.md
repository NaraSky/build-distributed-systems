# Handle RequestVote RPC

Website: <https://builddistributedsystem.com/tracks/elector/tasks/task-5-4-request-vote>

Track: 5. The Elector
Task order: 4
Short title: RequestVote
Difficulty: advanced
Subtrack: Raft Leader Election

## Problem

Implement the RequestVote RPC. Candidates request votes from other nodes. Nodes grant their vote if the candidate's term is current and they have not already voted in this term.

## Concept Notes

### Vote Granting

A node grants its vote if: the candidate term is at least as recent as its own, and it has not voted for another candidate in this term. This ensures at most one leader per term.

## Concepts

- voting
- term comparison
- vote granting

## Hints

- Grant vote if candidate term >= current term
- Only vote once per term
- Update term if candidate has higher term

## Test Cases

### 1. Grant vote to same term candidate

Input:

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1","n2","n3"]}}
{"src":"c0","dest":"n1","body":{"type":"set_term","msg_id":2,"term":2}}
{"src":"n2","dest":"n1","body":{"type":"request_vote","msg_id":3,"term":2,"candidate_id":"n2","last_log_index":0,"last_log_term":0}}
```

Expected output:

```text
{"src":"n1","dest":"c0","body":{"type":"init_ok","in_reply_to":1,"msg_id":0}}
{"src":"n1","dest":"c0","body":{"type":"set_term_ok","in_reply_to":2,"msg_id":1}}
{"src":"n1","dest":"n2","body":{"type":"request_vote_ok","in_reply_to":3,"msg_id":2,"term":2,"vote_granted":true}}
```

## Resources

- [Raft Lecture](https://www.youtube.com/watch?v=YbZ3zDzDnrw): MIT 6.824 Raft lecture by Robert Morris

## Java Starter

The matching local starter file is:

```text
src/main/java/Main.java
```
