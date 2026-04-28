# Implement Paxos Phase 2 (Accept/Accepted)

Website: <https://builddistributedsystem.com/tracks/consensus/tasks/task-7-3-2-accept-phase>

Track: 6. The Consensus
Task order: 12
Short title: Paxos Phase 2
Difficulty: advanced
Subtrack: Paxos

## Problem

Implement Phase 2 of Paxos. After getting a majority of promises in Phase 1, the proposer sends `Accept(n, v)` to acceptors.

Value selection rule: if any promise included a previously accepted value, the proposer MUST use the value with the highest accepted_n. Otherwise, the proposer chooses freely.

```json
Request:  {"type": "paxos_accept", "msg_id": 1, "proposal_n": 5, "value": "consensus_value"}
Response: {"type": "paxos_accepted", "in_reply_to": 1, "accepted": true, "proposal_n": 5, "value": "consensus_value"}

Request:  {"type": "paxos_accept", "msg_id": 2, "proposal_n": 3, "value": "late_value"}
Response: {"type": "paxos_accepted", "in_reply_to": 2, "accepted": false, "reason": "promised_higher", "highest_promised": 5}

Request:  {"type": "paxos_chosen", "msg_id": 3}
Response: {"type": "paxos_chosen_ok", "in_reply_to": 3, "value": "consensus_value", "chosen_at_n": 5}
```

## Concepts

- Paxos
- Accept
- Accepted
- value selection
- consensus

## Hints

- Phase 2: Proposer sends Accept(n, v) to acceptors
- v = highest accepted_value from Phase 1 promises, or proposer choice if none
- Acceptors accept if n >= highest_promised
- Once a majority accepts, the value is chosen (consensus reached)
- A chosen value can never be changed by future proposals

## Test Cases

### 1. Accept succeeds after promise

Input:

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"paxos_prepare","msg_id":2,"proposal_n":5}}
{"src":"c1","dest":"n1","body":{"type":"paxos_accept","msg_id":3,"proposal_n":5,"value":"hello"}}
```

Expected output:

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
{"src": "n1", "dest": "c1", "body": {"type": "paxos_promise", "in_reply_to": 2, "promised": true, "accepted_n": null, "accepted_value": null, "msg_id": 1}}
{"src": "n1", "dest": "c1", "body": {"type": "paxos_accepted", "in_reply_to": 3, "accepted": true, "proposal_n": 5, "value": "hello", "msg_id": 2}}
```

### 2. Accept rejected for lower proposal

Input:

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"paxos_prepare","msg_id":2,"proposal_n":5}}
{"src":"c1","dest":"n1","body":{"type":"paxos_accept","msg_id":3,"proposal_n":3,"value":"old"}}
```

Expected output:

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
{"src": "n1", "dest": "c1", "body": {"type": "paxos_promise", "in_reply_to": 2, "promised": true, "accepted_n": null, "accepted_value": null, "msg_id": 1}}
{"src": "n1", "dest": "c1", "body": {"type": "paxos_accepted", "in_reply_to": 3, "accepted": false, "highest_promised": 5, "msg_id": 2}}
```

## Resources

- [Understanding Paxos](https://www.cs.rutgers.edu/~pxk/417/notes/paxos.html): Step-by-step walkthrough of the Paxos protocol phases

## Java Starter

The matching local starter file is:

```text
src/main/java/Main.java
```
