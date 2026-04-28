# Detect and Handle Equivocation Attacks

Website: <https://builddistributedsystem.com/tracks/consensus/tasks/task-7-4-3-equivocation-defense>

Track: 6. The Consensus
Task order: 18
Short title: Equivocation Defense
Difficulty: advanced
Subtrack: Byzantine Fault Tolerance

## Problem

Simulate a Byzantine node that sends contradictory messages to different peers (equivocation). Show that PBFT correctly handles this.

```json
Request:  {"type": "simulate_equivocation", "msg_id": 1, "byzantine_node": "n2", "sequence": 1, "messages_sent": {
    "to_n1": {"prepare": {"value": "A"}},
    "to_n3": {"prepare": {"value": "B"}},
    "to_n4": {"prepare": {"value": "A"}}
}}
Response: {"type": "simulate_equivocation_ok", "in_reply_to": 1, "equivocation_detected": true, "evidence": {"node": "n2", "conflicting_values": ["A", "B"]}, "consensus_safe": true, "chosen_value": "A", "reason": "majority_agreed_on_A"}

Request:  {"type": "equivocation_report", "msg_id": 2}
Response: {"type": "equivocation_report_ok", "in_reply_to": 2, "byzantine_nodes_detected": ["n2"], "total_equivocations": 1}
```

## Concepts

- equivocation
- contradictory messages
- evidence collection
- Byzantine detection

## Hints

- Equivocation: a Byzantine node sends different messages to different peers
- Detection: peers compare received messages and find contradictions
- Evidence: two signed messages from the same node with different values for the same sequence
- PBFT handles this because 2f+1 matching messages are required for commit
- The contradictory node is effectively ignored when it cannot produce enough matching messages

## Test Cases

### 1. Equivocation is detected

simulate_equivocation_ok should show equivocation_detected: true and consensus_safe: true.

Input:

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1","n2","n3","n4"]}}
{"src":"c1","dest":"n1","body":{"type":"simulate_equivocation","msg_id":2,"byzantine_node":"n2","sequence":1,"messages_sent":{"to_n1":{"prepare":{"value":"A"}},"to_n3":{"prepare":{"value":"B"}},"to_n4":{"prepare":{"value":"A"}}}}}
```

Expected output:

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

### 2. Equivocation report lists Byzantine nodes

equivocation_report_ok should list n2 in byzantine_nodes_detected.

Input:

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1","n2","n3","n4"]}}
{"src":"c1","dest":"n1","body":{"type":"simulate_equivocation","msg_id":2,"byzantine_node":"n2","sequence":1,"messages_sent":{"to_n1":{"prepare":{"value":"X"}},"to_n3":{"prepare":{"value":"Y"}},"to_n4":{"prepare":{"value":"X"}}}}}
{"src":"c1","dest":"n1","body":{"type":"equivocation_report","msg_id":3}}
```

Expected output:

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

## Resources

- [Equivocation and BFT](https://decentralizedthoughts.github.io/2019-12-22-what-is-a-byzantine-agreement-problem/): How equivocation attacks work and how BFT protocols defend against them

## Java Starter

The matching local starter file is:

```text
src/main/java/Main.java
```
