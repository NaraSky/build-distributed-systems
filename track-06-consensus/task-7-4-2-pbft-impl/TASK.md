# Implement Simplified PBFT with 4 Nodes

Website: <https://builddistributedsystem.com/tracks/consensus/tasks/task-7-4-2-pbft-impl>

Track: 6. The Consensus
Task order: 17
Short title: PBFT Implementation
Difficulty: advanced
Subtrack: Byzantine Fault Tolerance

## Problem

Implement a simplified PBFT (Practical Byzantine Fault Tolerance) with 4 nodes (f=1 Byzantine fault).

PBFT Three-Phase Protocol:
1. **Pre-prepare**: Primary assigns sequence number, broadcasts (pre-prepare, v, n, d) to all
2. **Prepare**: Each replica broadcasts (prepare, v, n, d, i) to all. Prepare-certificate = 2f matching prepares
3. **Commit**: Each replica broadcasts (commit, v, n, d, i) to all. Commit-certificate = 2f+1 matching commits

```json
Request:  {"type": "pbft_request", "msg_id": 1, "operation": "set x=42", "client": "c1"}
Response: {"type": "pbft_request_ok", "in_reply_to": 1, "sequence_number": 1, "view": 0, "phase": "pre-prepare"}

Request:  {"type": "pbft_status", "msg_id": 2, "sequence_number": 1}
Response: {"type": "pbft_status_ok", "in_reply_to": 2, "phase": "committed", "prepares_received": 3, "commits_received": 4, "executed": true}
```

## Concepts

- PBFT
- pre-prepare
- prepare
- commit
- three-phase protocol

## Hints

- PBFT uses 3 phases: Pre-prepare, Prepare, Commit
- Pre-prepare: primary broadcasts the request to all replicas
- Prepare: each replica broadcasts Prepare to all other replicas. Wait for 2f matching Prepares
- Commit: each replica broadcasts Commit. Wait for 2f+1 matching Commits
- With f=1 Byzantine fault, need N=4 nodes (3f+1=4)

## Test Cases

### 1. Request starts pre-prepare phase

pbft_request_ok should show sequence_number: 1, view: 0, phase: pre-prepare.

Input:

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1","n2","n3","n4"]}}
{"src":"c1","dest":"n1","body":{"type":"pbft_request","msg_id":2,"operation":"set x=42","client":"c1"}}
```

Expected output:

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

### 2. Status shows execution after all phases

pbft_status_ok should show phase: committed or executed if all phases completed.

Input:

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1","n2","n3","n4"]}}
{"src":"c1","dest":"n1","body":{"type":"pbft_request","msg_id":2,"operation":"set x=1","client":"c1"}}
{"src":"c1","dest":"n1","body":{"type":"pbft_status","msg_id":3,"sequence_number":1}}
```

Expected output:

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

## Resources

- [Practical Byzantine Fault Tolerance - Castro & Liskov](https://pmg.csail.mit.edu/papers/osdi99.pdf): The original PBFT paper from OSDI 1999

## Java Starter

The matching local starter file is:

```text
src/main/java/Main.java
```
