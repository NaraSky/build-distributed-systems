# Implement Single-Decree Paxos Phase 1 (Prepare/Promise)

Website: <https://builddistributedsystem.com/tracks/consensus/tasks/task-7-3-1-single-decree>

Track: 6. The Consensus
Task order: 11
Short title: Paxos Phase 1
Difficulty: advanced
Subtrack: Paxos

## Problem

Implement Phase 1 of single-decree Paxos (agree on one value).

Phase 1 (Prepare/Promise):
1. Proposer selects a unique proposal number `n`
2. Proposer sends `Prepare(n)` to all acceptors
3. Each acceptor: if `n > highest_promised`, set `highest_promised = n` and reply `Promise(n, accepted_value, accepted_n)`
4. If `n <= highest_promised`, reject

```json
Request:  {"type": "paxos_prepare", "msg_id": 1, "proposal_n": 1}
Response: {"type": "paxos_promise", "in_reply_to": 1, "promised": true, "accepted_n": null, "accepted_value": null}

Request:  {"type": "paxos_prepare", "msg_id": 2, "proposal_n": 5}
Response: {"type": "paxos_promise", "in_reply_to": 2, "promised": true, "accepted_n": null, "accepted_value": null}

Request:  {"type": "paxos_prepare", "msg_id": 3, "proposal_n": 3}
Response: {"type": "paxos_promise", "in_reply_to": 3, "promised": false, "reason": "already_promised_higher", "highest_promised": 5}
```

## Concepts

- Paxos
- single-decree
- Prepare
- Promise
- proposal number

## Hints

- Phase 1: Proposer picks a unique proposal number n and sends Prepare(n) to acceptors
- Acceptors respond with Promise(n, previously_accepted_value) if n > their highest seen
- If acceptor has already promised a higher n, it rejects the Prepare
- Proposal numbers must be globally unique (use node_id + sequence)
- A proposer needs promises from a majority to proceed to Phase 2

## Test Cases

### 1. First prepare is always promised

Input:

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"paxos_prepare","msg_id":2,"proposal_n":1}}
```

Expected output:

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
{"src": "n1", "dest": "c1", "body": {"type": "paxos_promise", "in_reply_to": 2, "promised": true, "accepted_n": null, "accepted_value": null, "msg_id": 1}}
```

### 2. Higher proposal supersedes lower

Input:

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"paxos_prepare","msg_id":2,"proposal_n":5}}
{"src":"c1","dest":"n1","body":{"type":"paxos_prepare","msg_id":3,"proposal_n":3}}
```

Expected output:

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
{"src": "n1", "dest": "c1", "body": {"type": "paxos_promise", "in_reply_to": 2, "promised": true, "accepted_n": null, "accepted_value": null, "msg_id": 1}}
{"src": "n1", "dest": "c1", "body": {"type": "paxos_promise", "in_reply_to": 3, "promised": false, "highest_promised": 5, "msg_id": 2}}
```

## Resources

- [Paxos Made Simple - Lamport](https://lamport.azurewebsites.net/pubs/paxos-simple.pdf): Leslie Lamport simplified explanation of the Paxos algorithm

## Java Starter

The matching local starter file is:

```text
src/main/java/Main.java
```
