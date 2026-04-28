# Understand Byzantine Faults with Real-World Examples

Website: <https://builddistributedsystem.com/tracks/consensus/tasks/task-7-4-1-byzantine-faults>

Track: 6. The Consensus
Task order: 16
Short title: Byzantine Faults
Difficulty: intermediate
Subtrack: Byzantine Fault Tolerance

## Problem

What is a Byzantine fault? Unlike crash faults (node simply stops), Byzantine faults allow arbitrary misbehavior. A faulty node can lie, send contradictory messages, or selectively communicate.

Give 3 real-world examples and show why CFT algorithms fail:

```json
Request:  {"type": "classify_fault", "msg_id": 1, "scenario": "node_sends_different_values_to_different_peers"}
Response: {"type": "classify_fault_ok", "in_reply_to": 1, "fault_type": "byzantine", "cft_handles": false, "bft_handles": true, "example": "equivocation attack"}

Request:  {"type": "byzantine_examples", "msg_id": 2}
Response: {"type": "byzantine_examples_ok", "in_reply_to": 2, "examples": [
    {"name": "hardware_bit_flip", "description": "Memory corruption changes stored value silently", "fault_type": "byzantine"},
    {"name": "compromised_node", "description": "Attacker controls node, sends malicious messages", "fault_type": "byzantine"},
    {"name": "software_bug", "description": "Bug causes node to return wrong computation result", "fault_type": "byzantine"}
]}

Request:  {"type": "cft_failure_demo", "msg_id": 3, "algorithm": "raft", "byzantine_node": "n2", "behavior": "equivocation"}
Response: {"type": "cft_failure_demo_ok", "in_reply_to": 3, "consensus_reached": true, "value_correct": false, "reason": "raft_trusted_byzantine_node_response"}
```

## Concepts

- Byzantine fault
- crash fault
- malicious node
- bit flip
- CFT vs BFT

## Hints

- A Byzantine node can exhibit arbitrary behavior: lying, sending different messages to different nodes
- Crash faults are a subset of Byzantine faults (crash = silence, not lies)
- Real-world examples: hardware bit-flips, hacked nodes, software bugs returning wrong data
- CFT algorithms (Raft, Paxos) cannot handle Byzantine faults
- BFT requires N >= 3f+1 nodes to tolerate f Byzantine faults

## Test Cases

### 1. Classify equivocation as Byzantine

Input:

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"classify_fault","msg_id":2,"scenario":"node_sends_different_values_to_different_peers"}}
```

Expected output:

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
{"src": "n1", "dest": "c1", "body": {"type": "classify_fault_ok", "in_reply_to": 2, "fault_type": "byzantine", "cft_handles": false, "bft_handles": true, "msg_id": 1}}
```

### 2. List Byzantine fault examples

byzantine_examples_ok should contain at least 3 examples, all with fault_type: byzantine.

Input:

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"byzantine_examples","msg_id":2}}
```

Expected output:

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

## Resources

- [The Byzantine Generals Problem - Lamport](https://lamport.azurewebsites.net/pubs/byz.pdf): Original paper defining the Byzantine fault model

## Java Starter

The matching local starter file is:

```text
src/main/java/Main.java
```
