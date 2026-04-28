# Prove Paxos Safety: Chosen Values Are Immutable

Website: <https://builddistributedsystem.com/tracks/consensus/tasks/task-7-3-3-paxos-safety>

Track: 6. The Consensus
Task order: 13
Short title: Paxos Safety
Difficulty: advanced
Subtrack: Paxos

## Problem

Prove that once a value is chosen in Paxos, all future proposals will also choose the same value. This is the core safety property.

Implement a simulation that demonstrates this:

```json
Request:  {"type": "paxos_safety_test", "msg_id": 1, "nodes": 5, "chosen_value": "v1", "chosen_at_n": 3, "new_proposal_n": 7}
Response: {"type": "paxos_safety_test_ok", "in_reply_to": 1, "new_proposal_value": "v1", "forced_by_promise": true, "promise_source": "n2", "safe": true}

Request:  {"type": "paxos_invariant_check", "msg_id": 2, "proposals": [
    {"n": 1, "value": "a", "accepted_by": ["n1", "n2"]},
    {"n": 3, "value": "b", "accepted_by": ["n2", "n3", "n4"]},
    {"n": 5, "value": "b", "accepted_by": ["n3", "n4", "n5"]}
]}
Response: {"type": "paxos_invariant_check_ok", "in_reply_to": 2, "chosen_value": "b", "chosen_at_n": 3, "all_subsequent_match": true, "safe": true}
```

## Concepts

- safety proof
- invariant
- chosen value
- consensus immutability

## Hints

- Once a value v is chosen at proposal n, any future Accept(n2, v2) where n2 > n must have v2 = v
- The proof uses induction on proposal numbers
- Key insight: any higher proposal must hear about v in Phase 1 from a majority
- Two majorities always overlap, so at least one acceptor in the new quorum accepted v
- The proposer is forced to use v (the highest accepted value from promises)

## Test Cases

### 1. New proposal forced to use chosen value

paxos_safety_test_ok should show new_proposal_value: "v1", forced_by_promise: true, safe: true.

Input:

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"paxos_safety_test","msg_id":2,"nodes":5,"chosen_value":"v1","chosen_at_n":3,"new_proposal_n":7}}
```

Expected output:

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

### 2. Invariant holds across multiple proposals

chosen_value: "b" at n:3 (first majority). all_subsequent_match: true since n:5 also chose "b".

Input:

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"paxos_invariant_check","msg_id":2,"proposals":[{"n":1,"value":"a","accepted_by":["n1","n2"]},{"n":3,"value":"b","accepted_by":["n2","n3","n4"]},{"n":5,"value":"b","accepted_by":["n3","n4","n5"]}]}}
```

Expected output:

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

## Resources

- [Paxos Made Simple - Safety Proof](https://lamport.azurewebsites.net/pubs/paxos-simple.pdf): Lamport proof that Paxos safety invariant holds across all proposals

## Java Starter

The matching local starter file is:

```text
src/main/java/Main.java
```
