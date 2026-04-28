# Add Virtual Nodes for Even Distribution

Website: <https://builddistributedsystem.com/tracks/sharder/tasks/task-18-2-2-virtual-nodes>

Track: 8. The Sharder
Task order: 7
Short title: Virtual Nodes
Difficulty: intermediate
Subtrack: Consistent Hashing

## Problem

With few physical nodes, a consistent hash ring has uneven key distribution. Virtual nodes fix this by giving each physical node V positions on the ring.

**Problem**: with 3 physical nodes, one node might own 50% of the ring, another 35%, and the last 15%. This is because hash positions are pseudo-random.

**Solution**: create V virtual nodes for each physical node at positions `hash(node_id + "-" + i)` for i in 0..V.

**Distribution quality** (V = virtual nodes per physical node):
- V=1: high variance (~40% standard deviation)
- V=10: moderate (~15% standard deviation)
- V=150: low (~5.5% standard deviation)
- V=500: very low (~3% standard deviation)

```json
Request:  {"type": "ring_create", "msg_id": 1, "nodes": ["n1", "n2", "n3"], "vnodes_per_node": 150}
Response: {"type": "ring_create_ok", "in_reply_to": 1, "total_vnodes": 450, "distribution": {"n1": 0.34, "n2": 0.33, "n3": 0.33}}
```

## Concepts

- virtual nodes
- vnodes
- even distribution
- load balancing
- hash collision

## Hints

- With only 3 physical nodes, distribution is uneven (one node may own 60% of keys)
- Virtual nodes: each physical node has V positions: hash(node_id + "-" + i) for i in 0..V
- V=150 gives a standard deviation of ~5.5% around the ideal 1/N per node
- Key lookup: find the nearest vnode clockwise, then map vnode -> physical node
- More vnodes = better distribution, but more memory for the ring data structure

## Test Cases

### 1. Virtual nodes improve distribution

Each node should own roughly 33% of the ring.

Input:

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1","n2","n3"]}}
{"src":"c1","dest":"n1","body":{"type":"ring_create","msg_id":2,"nodes":["n1","n2","n3"],"vnodes_per_node":150}}
```

Expected output:

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

### 2. Total vnodes equals nodes * vnodes_per_node

total_vnodes should be 200.

Input:

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1","n2"]}}
{"src":"c1","dest":"n1","body":{"type":"ring_create","msg_id":2,"nodes":["n1","n2"],"vnodes_per_node":100}}
```

Expected output:

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

## Resources

- [DynamoDB Virtual Nodes](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/HowItWorks.Partitions.html): AWS DynamoDB documentation on partition key distribution

## Java Starter

The matching local starter file is:

```text
src/main/java/Main.java
```
