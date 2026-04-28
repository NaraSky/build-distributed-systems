# Implement Basic Broadcast to All Nodes

Website: <https://builddistributedsystem.com/tracks/gossiper/tasks/task-3-1-basic-broadcast>

Track: 3. The Gossiper
Task order: 1
Short title: Basic Broadcast
Difficulty: beginner
Subtrack: Naive Broadcast (Flooding)

## Problem

Implement a broadcast system where messages sent to any node eventually reach all nodes.

Handle three message types:
1. topology: Tells you your neighbors in the cluster topology
2. broadcast: Contains a message value to propagate
3. read: Returns all messages this node has seen

When you receive a broadcast, store the message and forward it to your neighbors. A read request should return all unique messages received so far.

## Concept Notes

### Broadcast Protocols

Broadcast is the foundation of many distributed algorithms. When one node learns something, it must share that knowledge with the cluster. The challenge is doing this efficiently without creating message storms.

### Flooding

The simplest approach is flooding: forward every message to all neighbors. This guarantees delivery but creates O(n*m) messages for n nodes and m values. We will optimize this in later tasks.

## Concepts

- broadcast
- flooding
- message propagation

## Hints

- Store received messages in a set
- Forward new messages to all known nodes
- Handle the topology message to learn neighbors

## Test Cases

### 1. Basic broadcast with read

Input:

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c0","dest":"n1","body":{"type":"topology","msg_id":2,"topology":{"n1":[]}}}
{"src":"c1","dest":"n1","body":{"type":"broadcast","msg_id":3,"message":100}}
{"src":"c1","dest":"n1","body":{"type":"read","msg_id":4}}
```

Expected output:

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
{"src": "n1", "dest": "c0", "body": {"type": "topology_ok", "in_reply_to": 2, "msg_id": 1}}
{"src": "n1", "dest": "c1", "body": {"type": "broadcast_ok", "in_reply_to": 3, "msg_id": 2}}
{"src": "n1", "dest": "c1", "body": {"type": "read_ok", "messages": [100], "in_reply_to": 4, "msg_id": 3}}
```

### 2. Broadcast multiple messages

Input:

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c0","dest":"n1","body":{"type":"topology","msg_id":2,"topology":{"n1":[]}}}
{"src":"c1","dest":"n1","body":{"type":"broadcast","msg_id":3,"message":"msg1"}}
{"src":"c2","dest":"n1","body":{"type":"broadcast","msg_id":4,"message":"msg2"}}
{"src":"c3","dest":"n1","body":{"type":"read","msg_id":5}}
```

Expected output:

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
{"src": "n1", "dest": "c0", "body": {"type": "topology_ok", "in_reply_to": 2, "msg_id": 1}}
{"src": "n1", "dest": "c1", "body": {"type": "broadcast_ok", "in_reply_to": 3, "msg_id": 2}}
{"src": "n1", "dest": "c2", "body": {"type": "broadcast_ok", "in_reply_to": 4, "msg_id": 3}}
{"src": "n1", "dest": "c3", "body": {"type": "read_ok", "messages": ["msg1", "msg2"], "in_reply_to": 5, "msg_id": 4}}
```

## Resources

- [Broadcast Challenge](https://fly.io/dist-sys/3a/): Fly.io Gossip Glomers broadcast challenge

## Java Starter

The matching local starter file is:

```text
src/main/java/Main.java
```
