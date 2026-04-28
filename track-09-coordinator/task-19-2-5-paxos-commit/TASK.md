# Implement Paxos Commit Protocol

Website: <https://builddistributedsystem.com/tracks/coordinator/tasks/task-19-2-5-paxos-commit>

Track: 9. The Coordinator
Task order: 10
Short title: Paxos Commit
Difficulty: advanced
Subtrack: Three-Phase Commit (3PC)

## Problem

Paxos Commit replaces the single coordinator with a Paxos consensus group. Each participant's commit decision is reached through Paxos, eliminating the single point of failure.

**Architecture**:
- Each participant has its own Paxos instance deciding its commit/abort vote
- A proposer proposes "commit" or "abort" to each Paxos instance
- Once a value is chosen by Paxos, it cannot be undone
- No single coordinator failure point

**Paxos phases for commit**:
```
For each participant P:
  Phase 1a (Prepare):  proposer → acceptors: Prepare(1)
  Phase 1b (Promise):  acceptors → proposer: Promise(1, prev_value_if_any)
  Phase 2a (Accept):   proposer → acceptors: Accept(1, "commit")
  Phase 2b (Accepted): acceptors → proposer: Accepted(1, "commit")
```

**Example Paxos Commit**:
```json
Request:  {"type": "paxos_commit_begin", "msg_id": 1, "participants": ["p1", "p2", "p3"], "acceptors": ["a1", "a2", "a3"], "operations": [{"transfer": 100, "from": "a", "to": "b"}]}

// Phase 1 for p1's decision:
{"type": "prepare", "msg_id": 2, "proposal_id": 1, "participant": "p1"}
{"type": "promise", "in_reply_to": 2, "acceptor": "a1", "proposal_id": 1, "accepted_value": null}
{"type": "promise", "in_reply_to": 2, "acceptor": "a2", "proposal_id": 1, "accepted_value": null}
{"type": "promise", "in_reply_to": 2, "acceptor": "a3", "proposal_id": 1, "accepted_value": null}

// Phase 2 for p1's decision:
{"type": "accept", "msg_id": 3, "proposal_id": 1, "participant": "p1", "value": "commit"}
{"type": "accepted", "in_reply_to": 3, "acceptor": "a1", "proposal_id": 1, "value": "commit"}
{"type": "accepted", "in_reply_to": 3, "acceptor": "a2", "proposal_id": 1, "value": "commit"}
{"type": "accepted", "in_reply_to": 3, "acceptor": "a3", "proposal_id": 1, "value": "commit"}

// Repeat for p2, p3...
```

**Advantages over 2PC/3PC**:
- No single coordinator failure point
- Tolerates crash of any proposer (any proposer can retry)
- Non-blocking as long as a majority of acceptors is available

**Disadvantages**:
- Higher latency: 2 round trips per participant
- Higher message complexity: 4N messages per participant
- More complex implementation

## Concepts

- Paxos commit
- consensus-based commit
- no single point of failure
- acceptors
- proposers
- learners

## Hints

- Replace the coordinator with a Paxos group (acceptors)
- Each participant's vote is decided by its own Paxos instance
- Phase 1 (Prepare): proposer gets promises from acceptors
- Phase 2 (Accept): proposer sends value, acceptors accept if promised
- No single point of failure: any proposer can drive the protocol

## Test Cases

### 1. Successful Paxos commit

All participants should reach commit decision through Paxos consensus.

Input:

```json
{"src":"c0","dest":"paxos_coord","body":{"type":"init","msg_id":1,"participants":["p1","p2","p3"],"acceptors":["a1","a2","a3"]}}
{"src":"c1","dest":"paxos_coord","body":{"type":"paxos_commit_begin","msg_id":2,"participants":["p1","p2","p3"],"acceptors":["a1","a2","a3"],"operations":[{"transfer":100,"from":"a","to":"b"}]}}
```

Expected output:

```text
{"src": "paxos_coord", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

### 2. Proposer crash recovery

New proposer should take over and complete Paxos rounds for all participants.

Input:

```json
{"src":"c0","dest":"paxos_coord","body":{"type":"init","msg_id":1,"participants":["p1","p2"],"acceptors":["a1","a2","a3"]}}
{"src":"c1","dest":"paxos_coord","body":{"type":"paxos_commit_begin","msg_id":2,"participants":["p1","p2"],"acceptors":["a1","a2","a3"],"operations":[{"transfer":100,"from":"a","to":"b"}],"crash_proposer_after":"prepare"}}
{"src":"c2","dest":"paxos_coord","body":{"type":"recover_proposer","msg_id":3}}
```

Expected output:

```text
{"src": "paxos_coord", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

## Resources

- [Paxos Made Simple](https://www.microsoft.com/en-us/research/wp-content/uploads/2016/02/tr-2007-81.pdf): Original Lamport Paxos paper

## Java Starter

The matching local starter file is:

```text
src/main/java/Main.java
```
