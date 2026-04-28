# Implement Rendezvous Hashing (Highest Random Weight)

Website: <https://builddistributedsystem.com/tracks/sharder/tasks/task-18-2-5-rendezvous-hashing>

Track: 8. The Sharder
Task order: 10
Short title: Rendezvous Hashing
Difficulty: advanced
Subtrack: Consistent Hashing

## Problem

Rendezvous hashing (Highest Random Weight) is an alternative to consistent hashing. For each key, compute a score for every node, and the highest score wins.

**Algorithm**:
1. For each key K and each node N: `score = hash(K + N)`
2. Assign K to the node with the highest score
3. When a node is added/removed, re-evaluate only affected keys

**Advantages over consistent hashing**:
- Simpler implementation (no ring data structure)
- Perfect distribution without virtual nodes
- Easy to support weighted nodes: `score = hash(K + N) * weight(N)`

**Disadvantages**:
- O(N) per lookup (must compute score for all nodes) vs. O(log N) for ring
- For small clusters (<100 nodes), the O(N) cost is negligible

```json
Request:  {"type": "hrw_lookup", "msg_id": 1, "key": "user:42", "nodes": ["n1", "n2", "n3"]}
Response: {"type": "hrw_lookup_ok", "in_reply_to": 1, "key": "user:42", "winner": "n2", "scores": {"n1": 12345, "n2": 99999, "n3": 45678}}
```

## Concepts

- rendezvous hashing
- highest random weight
- HRW
- consistent hashing alternative
- weighted nodes

## Hints

- For each key, compute weight(key, node) = hash(key + node_id) for ALL nodes
- The node with the highest weight owns the key
- When a node is added/removed, only keys where that node had the highest weight are affected
- Simpler than consistent hashing: no ring, no virtual nodes
- Naturally supports weighted nodes: multiply the hash by the node weight

## Test Cases

### 1. HRW returns node with highest score

winner should be the node with the highest score in the scores map.

Input:

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1","n2","n3"]}}
{"src":"c1","dest":"n1","body":{"type":"hrw_lookup","msg_id":2,"key":"test","nodes":["n1","n2","n3"]}}
```

Expected output:

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

### 2. Same key always maps to same node

Both lookups should return the same winner.

Input:

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1","n2"]}}
{"src":"c1","dest":"n1","body":{"type":"hrw_lookup","msg_id":2,"key":"k","nodes":["n1","n2"]}}
{"src":"c1","dest":"n1","body":{"type":"hrw_lookup","msg_id":3,"key":"k","nodes":["n1","n2"]}}
```

Expected output:

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

## Resources

- [Rendezvous Hashing](https://en.wikipedia.org/wiki/Rendezvous_hashing): Wikipedia article on rendezvous hashing (highest random weight)

## Java Starter

The matching local starter file is:

```text
src/main/java/Main.java
```
