# Handle Network Partition Healing and Resynchronization

Website: <https://builddistributedsystem.com/tracks/gossiper/tasks/task-3-5-partition-healing>

Track: 3. The Gossiper
Task order: 5
Short title: Partition Healing
Difficulty: advanced
Subtrack: Naive Broadcast (Flooding)

## Problem

Handle the scenario where network partitions heal and previously isolated nodes reconnect. Implement anti-entropy mechanisms to synchronize message sets between nodes that were separated.

## Concept Notes

### Anti-Entropy

Anti-entropy protocols periodically compare state between nodes and resolve differences. When partitions heal, nodes must reconcile their message sets to ensure eventual consistency.

## Concepts

- network partitions
- resynchronization
- anti-entropy

## Hints

- Detect when partitions heal
- Exchange message sets with reconnected nodes
- Use Merkle trees for efficient sync
- Reply with broadcast_ok before forwarding to neighbors to ensure deterministic output ordering

## Test Cases

### 1. Nodes sync after partition heals

Input:

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1","n2"]}}
{"src":"c0","dest":"n1","body":{"type":"topology","msg_id":2,"topology":{"n1":["n2"],"n2":["n1"]}}}
{"src":"c1","dest":"n1","body":{"type":"broadcast","msg_id":3,"message":10}}
{"src":"c1","dest":"n1","body":{"type":"broadcast","msg_id":4,"message":20}}
{"src":"c2","dest":"n1","body":{"type":"read","msg_id":5}}
```

Expected output:

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
{"src": "n1", "dest": "c0", "body": {"type": "topology_ok", "in_reply_to": 2, "msg_id": 1}}
{"src": "n1", "dest": "c1", "body": {"type": "broadcast_ok", "in_reply_to": 3, "msg_id": 2}}
{"src": "n1", "dest": "n2", "body": {"type": "broadcast", "message": 10, "msg_id": 3}}
{"src": "n1", "dest": "c1", "body": {"type": "broadcast_ok", "in_reply_to": 4, "msg_id": 4}}
{"src": "n1", "dest": "n2", "body": {"type": "broadcast", "message": 20, "msg_id": 5}}
{"src": "n1", "dest": "c2", "body": {"type": "read_ok", "messages": [10, 20], "in_reply_to": 5, "msg_id": 6}}
```

## Resources

- [Anti-Entropy Protocols](https://www.cs.cornell.edu/home/rvr/papers/flowgossip.pdf): Research on anti-entropy and synchronization

## Java Starter

The matching local starter file is:

```text
src/main/java/Main.java
```
