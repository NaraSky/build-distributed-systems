# Prove G-Counter CRDT Properties

Website: <https://builddistributedsystem.com/tracks/counter/tasks/task-17-2-2-g-counter-proof>

Track: 4. The Counter
Task order: 7
Short title: CRDT Proof
Difficulty: intermediate
Subtrack: G-Counter and PN-Counter

## Problem

A CRDT merge function must satisfy three properties to guarantee convergence: commutativity, associativity, and idempotency. Proving these for the G-Counter validates it as a correct CRDT.

**Commutativity**: `merge(A, B) == merge(B, A)`
- max(A[i], B[i]) == max(B[i], A[i]) for all i. This is true because max is commutative.

**Associativity**: `merge(A, merge(B, C)) == merge(merge(A, B), C)`
- max(A[i], max(B[i], C[i])) == max(max(A[i], B[i]), C[i]). True because max is associative.

**Idempotency**: `merge(A, A) == A`
- max(A[i], A[i]) == A[i]. True because max(x, x) == x.

These properties form a **join semi-lattice**: the set of all possible states with merge as the join operation. The system monotonically advances through this lattice, guaranteeing convergence.

```json
Request:  {"type": "crdt_verify", "msg_id": 1, "state_a": {"n1": 3, "n2": 1}, "state_b": {"n1": 1, "n2": 5}}
Response: {"type": "crdt_verify_ok", "in_reply_to": 1, "merge_ab": {"n1": 3, "n2": 5}, "merge_ba": {"n1": 3, "n2": 5}, "commutative": true, "idempotent": true}
```

## Concepts

- commutativity
- associativity
- idempotency
- lattice
- convergence proof

## Hints

- Commutative: merge(A, B) == merge(B, A) for all states A, B
- Associative: merge(A, merge(B, C)) == merge(merge(A, B), C)
- Idempotent: merge(A, A) == A
- These three properties ensure convergence regardless of message order or duplication
- The element-wise max operation satisfies all three properties

## Test Cases

### 1. Merge is commutative

merge_ab should equal merge_ba and commutative should be true.

Input:

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"crdt_verify","msg_id":2,"state_a":{"n1":3,"n2":1},"state_b":{"n1":1,"n2":5}}}
```

Expected output:

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

### 2. Merge is idempotent

merge(A,A) should equal A and idempotent should be true.

Input:

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"crdt_verify","msg_id":2,"state_a":{"n1":5,"n2":3},"state_b":{"n1":5,"n2":3}}}
```

Expected output:

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

## Resources

- [CRDT Convergence](https://hal.inria.fr/inria-00609399/document): Shapiro et al. - A comprehensive study of CRDTs

## Java Starter

The matching local starter file is:

```text
src/main/java/Main.java
```
