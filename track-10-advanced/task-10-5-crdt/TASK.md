# Implement CRDTs

Website: <https://builddistributedsystem.com/tracks/advanced/tasks/task-10-5-crdt>

Track: 10. Advanced
Task order: 5
Short title: CRDTs
Difficulty: advanced
Subtrack: Advanced Paradigms

## Problem

Build CRDTs for conflict-free replication: G-Counter (grow-only counter), G-Set, OR-Set.

## Concept Notes

### CRDTs

Conflict-free Replicated Data Types allow concurrent updates that merge without conflicts. Merge is associative, commutative, idempotent.

## Concepts

- CRDT
- eventual consistency
- conflict-free

## Hints

- Merge must be commutative, associative, idempotent
- G-Counter: only increment
- OR-Set: add wins over remove

## Test Cases

### 1. G-Counter increment and merge

Multi-node test: n1 increments (count n1->1), n2 increments (count n2->1). When nodes sync, they merge their counters. Query n1 for total value, should return 2 (sum of all node counts).

Input:

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1","n2"]}}
{"src":"c1","dest":"n1","body":{"type":"gcounter_increment","msg_id":2}}
{"src":"c2","dest":"n2","body":{"type":"gcounter_increment","msg_id":3}}
{"src":"c3","dest":"n1","body":{"type":"gcounter_value","msg_id":4}}
```

## Resources

- [CRDTs Paper](https://hal.inria.fr/inria-00555588): Comprehensive study of CRDTs

## Java Starter

The matching local starter file is:

```text
src/main/java/Main.java
```
