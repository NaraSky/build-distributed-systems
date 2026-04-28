# Implement Tree-Based Broadcast Overlay

Website: <https://builddistributedsystem.com/tracks/gossiper/tasks/task-3-3-1-tree-broadcast>

Track: 3. The Gossiper
Task order: 11
Short title: Tree Broadcast
Difficulty: intermediate
Subtrack: Topology-Aware Gossip

## Problem

Random gossip wastes messages because nodes may receive duplicates. A **spanning tree** ensures each node receives exactly one copy: the root broadcasts to its children, who forward to their children, etc.

Your task is to implement tree-based broadcast:

1. Use the `topology` message to learn your tree neighbors
2. On `broadcast`, forward to all tree neighbors except the source
3. Track the forwarding path for debugging

Handle these message types:
- `topology`: Store the neighbor list for this node
- `broadcast`: Store value and forward to tree neighbors
- `read`: Return all known values
- `tree_info`: Return current tree structure for this node

```json
Request:  {"type": "tree_info", "msg_id": 1}
Response: {"type": "tree_info_ok", "in_reply_to": 1, "neighbors": ["n2", "n3"], "message_count": 5}
```

## Concepts

- spanning tree
- tree broadcast
- overlay network
- message forwarding

## Hints

- Build a spanning tree from the topology provided by Maelstrom
- Each node only forwards to its children in the tree
- Tree broadcast has O(N-1) messages vs O(N*K) for random gossip
- The root receives the broadcast and pushes down the tree
- Use the topology message to learn your neighbors

## Test Cases

### 1. Topology stores neighbors

Input:

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1","n2","n3"]}}
{"src":"c1","dest":"n1","body":{"type":"topology","msg_id":2,"topology":{"n1":["n2","n3"],"n2":["n1"],"n3":["n1"]}}}
{"src":"c1","dest":"n1","body":{"type":"tree_info","msg_id":3}}
```

Expected output:

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
{"src": "n1", "dest": "c1", "body": {"type": "topology_ok", "in_reply_to": 2, "msg_id": 1}}
{"src": "n1", "dest": "c1", "body": {"type": "tree_info_ok", "neighbors": ["n2", "n3"], "message_count": 0, "in_reply_to": 3, "msg_id": 2}}
```

### 2. Broadcast stores and reads back

Input:

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"topology","msg_id":2,"topology":{"n1":[]}}}
{"src":"c1","dest":"n1","body":{"type":"broadcast","msg_id":3,"message":42}}
{"src":"c1","dest":"n1","body":{"type":"read","msg_id":4}}
```

Expected output:

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
{"src": "n1", "dest": "c1", "body": {"type": "topology_ok", "in_reply_to": 2, "msg_id": 1}}
{"src": "n1", "dest": "c1", "body": {"type": "broadcast_ok", "in_reply_to": 3, "msg_id": 2}}
{"src": "n1", "dest": "c1", "body": {"type": "read_ok", "messages": [42], "in_reply_to": 4, "msg_id": 3}}
```

## Resources

- [Spanning Tree Protocol](https://en.wikipedia.org/wiki/Spanning_Tree_Protocol): Overview of spanning tree concepts in networking

## Java Starter

The matching local starter file is:

```text
src/main/java/Main.java
```
