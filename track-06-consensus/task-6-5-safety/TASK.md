# Implement Election Restriction for Safety

Website: <https://builddistributedsystem.com/tracks/consensus/tasks/task-6-5-safety>

Track: 6. The Consensus
Task order: 5
Short title: Safety
Difficulty: advanced
Subtrack: Raft Log Replication

## Problem

Implement the Election Restriction to ensure safety:

A candidate must have an "up-to-date" log to win election:
1. Voter compares own log to candidate's
2. If candidate lastLogTerm > voter lastLogTerm: candidate is ahead
3. If same term, compare lastLogIndex
4. Only grant vote if candidate is at least as up-to-date

This ensures the elected leader has all committed entries.

## Concept Notes

### Election Restriction

This is the key safety property of Raft. By only electing candidates with up-to-date logs, we ensure no committed entries are lost. The leader completeness property follows from this.

### Comparison Logic

Higher term always wins. If same term, longer log wins. This captures "more up-to-date" precisely. A leader elected under these rules has everything committed before it.

## Concepts

- election restriction
- safety
- up-to-date

## Hints

- Voter checks candidate log is up-to-date
- Compare last log term first, then index
- Reject vote if candidate log is behind

## Test Cases

### 1. Grant vote to higher term

Input:

```json
{"src":"c0","dest":"n2","body":{"type":"init","msg_id":1,"node_id":"n2","node_ids":["n1","n2","n3"]}}
{"src":"c0","dest":"n2","body":{"type":"set_term","msg_id":2,"term":2}}
{"src":"n1","dest":"n2","body":{"type":"request_vote","msg_id":3,"term":3,"candidate_id":"n1","last_log_index":0,"last_log_term":0}}
```

Expected output:

```text
{"src":"n2","dest":"c0","body":{"type":"init_ok","in_reply_to":1,"msg_id":0}}
{"src":"n2","dest":"c0","body":{"type":"set_term_ok","in_reply_to":2,"msg_id":1}}
{"src":"n2","dest":"n1","body":{"type":"request_vote_ok","in_reply_to":3,"msg_id":2,"term":3,"vote_granted":true}}
```

## Resources

- [Raft Safety](https://raft.github.io/raft.pdf): Raft paper section on safety

## Java Starter

The matching local starter file is:

```text
src/main/java/Main.java
```
