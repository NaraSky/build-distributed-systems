# Build Flat Tree Topology Gossip

Website: <https://builddistributedsystem.com/tracks/gossiper/tasks/task-3-2-tree-topology>

Track: 3. The Gossiper
Task order: 2
Short title: Tree Topology
Difficulty: intermediate
Subtrack: Naive Broadcast (Flooding)

## Problem

Optimize your broadcast by using a tree topology. Instead of flooding to all neighbors, organize nodes into a spanning tree where each message travels along tree edges exactly once.

This reduces message complexity from O(n*m) to O(n) for each broadcast, where n is the number of nodes.

## Concept Notes

### Spanning Trees

A spanning tree connects all nodes with exactly n-1 edges and no cycles. Broadcasting along a tree ensures each message is delivered exactly once to each node, minimizing network traffic.

## Concepts

- tree topology
- spanning tree
- efficient propagation

## Hints

- Use the provided topology to form a tree
- Avoid sending back to parent
- Tree ensures O(n) messages
- Reply with broadcast_ok before forwarding to neighbors - this ensures deterministic msg_id ordering in the output

## Test Cases

### 1. Tree broadcast with 3 nodes

Input:

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1","n2","n3"]}}
{"src":"c0","dest":"n1","body":{"type":"topology","msg_id":2,"topology":{"n1":["n2"],"n2":["n1","n3"],"n3":["n2"]}}}
{"src":"c1","dest":"n1","body":{"type":"broadcast","msg_id":3,"message":100}}
{"src":"c1","dest":"n1","body":{"type":"read","msg_id":4}}
```

Expected output:

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
{"src": "n1", "dest": "c0", "body": {"type": "topology_ok", "in_reply_to": 2, "msg_id": 1}}
{"src": "n1", "dest": "c1", "body": {"type": "broadcast_ok", "in_reply_to": 3, "msg_id": 2}}
{"src": "n1", "dest": "n2", "body": {"type": "broadcast", "message": 100, "msg_id": 3}}
{"src": "n1", "dest": "c1", "body": {"type": "read_ok", "messages": [100], "in_reply_to": 4, "msg_id": 4}}
```

## Java Starter

The matching local starter file is:

```text
src/main/java/Main.java
```
