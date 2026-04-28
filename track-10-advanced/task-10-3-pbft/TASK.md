# Implement Byzantine Fault Tolerance

Website: <https://builddistributedsystem.com/tracks/advanced/tasks/task-10-3-pbft>

Track: 10. Advanced
Task order: 3
Short title: PBFT
Difficulty: advanced
Subtrack: Advanced Paradigms

## Problem

Implement PBFT: tolerates f Byzantine faults with 3f+1 nodes. Three phases: pre-prepare, prepare, commit.

## Concept Notes

### Byzantine Fault Tolerance

Byzantine faults include malicious behavior. PBFT requires 3f+1 nodes to tolerate f faulty nodes. Uses 3 phases with quorum certificates.

## Concepts

- Byzantine
- PBFT
- f faults

## Hints

- Need 3f+1 nodes to tolerate f faults
- Pre-prepare, Prepare, Commit phases
- Wait for 2f+1 matching messages

## Test Cases

### 1. Pre-prepare phase

Multi-node test: 4 nodes (n=4, f=1, need 2f+1=3 for quorum). Primary (n0) receives client request seq=1. Primary broadcasts PRE-PREPARE to all replicas (n1, n2, n3) with sequence number, digest, and view. Verify all replicas receive pre-prepare message.

Input:

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
```

Expected output:

```text
{"src":"n1","dest":"c0","body":{"type":"init_ok","in_reply_to":1,"msg_id":0}}
```

## Resources

- [PBFT Paper](http://pmg.csail.mit.edu/papers/osdi99.pdf): Practical Byzantine Fault Tolerance

## Java Starter

The matching local starter file is:

```text
src/main/java/Main.java
```
