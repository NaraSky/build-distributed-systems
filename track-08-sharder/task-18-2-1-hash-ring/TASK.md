# Implement a Consistent Hash Ring

Website: <https://builddistributedsystem.com/tracks/sharder/tasks/task-18-2-1-hash-ring>

Track: 8. The Sharder
Task order: 6
Short title: Hash Ring
Difficulty: intermediate
Subtrack: Consistent Hashing

## Problem

Consistent hashing places nodes and keys on a circular ring, minimizing key redistribution when nodes join or leave. Unlike modulo hashing (`hash(key) % N`), adding a node only moves ~1/N of keys.

**Hash ring construction**:
1. For each node, compute `position = hash(node_id) % 2^32`
2. Place nodes on a circle of size 2^32

**Key lookup**:
1. Compute `position = hash(key) % 2^32`
2. Walk clockwise from that position until you find a node
3. That node owns the key

**Key redistribution on node join**: only keys between the new node and its counter-clockwise neighbor need to move. All other keys stay in place.

```json
Request:  {"type": "ring_lookup", "msg_id": 1, "key": "user:42"}
Response: {"type": "ring_lookup_ok", "in_reply_to": 1, "key": "user:42", "node": "n2", "position": 1048576}
```

## Concepts

- consistent hashing
- hash ring
- key ownership
- clockwise lookup
- minimal disruption

## Hints

- Place nodes at positions hash(node_id) % 2^32 on a circular ring
- A key is owned by the first node clockwise from hash(key) % 2^32
- When a node joins, only keys between the new node and its predecessor migrate
- When a node leaves, only its keys move to its successor
- Compare with modulo hashing: adding a node remaps ~1/N keys vs. nearly all keys

## Test Cases

### 1. Key maps to nearest clockwise node

ring_lookup_ok should return a valid node from the ring.

Input:

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1","n2","n3"]}}
{"src":"c1","dest":"n1","body":{"type":"ring_lookup","msg_id":2,"key":"user:42"}}
```

Expected output:

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

### 2. Same key always maps to same node

Both lookups should return the same node.

Input:

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1","n2"]}}
{"src":"c1","dest":"n1","body":{"type":"ring_lookup","msg_id":2,"key":"k1"}}
{"src":"c1","dest":"n1","body":{"type":"ring_lookup","msg_id":3,"key":"k1"}}
```

Expected output:

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

## Resources

- [Consistent Hashing](https://en.wikipedia.org/wiki/Consistent_hashing): Wikipedia article on consistent hashing

## Java Starter

The matching local starter file is:

```text
src/main/java/Main.java
```
