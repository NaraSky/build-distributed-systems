# Implement Grow-Only Set (G-Set) with Gossip

Website: <https://builddistributedsystem.com/tracks/gossiper/tasks/task-3-4-1-gset>

Track: 3. The Gossiper
Task order: 16
Short title: G-Set
Difficulty: intermediate
Subtrack: Epidemic Algorithms and CRDT Gossip

## Problem

A **Grow-only Set (G-Set)** is the simplest CRDT. Elements can be added but never removed. Merge is set union, which is commutative, associative, and idempotent - guaranteeing eventual consistency via gossip.

Implement a G-Set replicated via gossip:
1. `add` - Add an element to the set
2. `read` - Return all elements
3. `merge` - Merge a remote G-Set (union)

```json
Request:  {"type": "add", "msg_id": 1, "element": "x"}
Response: {"type": "add_ok", "in_reply_to": 1}

Request:  {"type": "merge", "msg_id": 2, "elements": ["a","b","c"]}
Response: {"type": "merge_ok", "in_reply_to": 2, "new_count": 2}

Request:  {"type": "read", "msg_id": 3}
Response: {"type": "read_ok", "in_reply_to": 3, "elements": ["a","b","c","x"]}
```

## Concepts

- G-Set
- CRDT
- set union
- eventual consistency

## Hints

- A G-Set only supports add operations, never remove
- Merge is simply set union: merged = local | remote
- Union is commutative, associative, and idempotent - perfect for gossip
- Convergence is guaranteed because sets only grow
- This is the simplest CRDT to implement

## Test Cases

### 1. Add and read

Input:

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"add","msg_id":2,"element":"x"}}
{"src":"c1","dest":"n1","body":{"type":"read","msg_id":3}}
```

Expected output:

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
{"src": "n1", "dest": "c1", "body": {"type": "add_ok", "in_reply_to": 2, "msg_id": 1}}
{"src": "n1", "dest": "c1", "body": {"type": "read_ok", "elements": ["x"], "in_reply_to": 3, "msg_id": 2}}
```

### 2. Merge adds new elements

Input:

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"add","msg_id":2,"element":"a"}}
{"src":"n2","dest":"n1","body":{"type":"merge","msg_id":3,"elements":["a","b","c"]}}
{"src":"c1","dest":"n1","body":{"type":"read","msg_id":4}}
```

Expected output:

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
{"src": "n1", "dest": "c1", "body": {"type": "add_ok", "in_reply_to": 2, "msg_id": 1}}
{"src": "n1", "dest": "n2", "body": {"type": "merge_ok", "new_count": 2, "in_reply_to": 3, "msg_id": 2}}
{"src": "n1", "dest": "c1", "body": {"type": "read_ok", "elements": ["a", "b", "c"], "in_reply_to": 4, "msg_id": 3}}
```

## Resources

- [A Comprehensive Study of CRDTs](https://hal.inria.fr/inria-00555588/document): Shapiro et al. survey of CRDT designs

## Java Starter

The matching local starter file is:

```text
src/main/java/Main.java
```
