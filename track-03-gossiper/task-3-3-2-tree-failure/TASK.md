# Handle Tree Node Failure with Direct Fallback

Website: <https://builddistributedsystem.com/tracks/gossiper/tasks/task-3-3-2-tree-failure>

Track: 3. The Gossiper
Task order: 12
Short title: Tree Failure
Difficulty: advanced
Subtrack: Topology-Aware Gossip

## Problem

Tree broadcast is efficient but fragile: if a node crashes, all its descendants lose connectivity. Your task is to add **failure detection** with direct fallback.

When forwarding to a neighbor, expect a `broadcast_ack` within a timeout. If no ack arrives, fall back to direct delivery to all known nodes that might be in the failed subtree.

Implement:
1. `broadcast` with ack tracking
2. `broadcast_ack` handler for acknowledgments
3. `check_acks` handler to simulate timeout checking and trigger fallback
4. `failure_stats` to report failures

```json
Request:  {"type": "check_acks", "msg_id": 1}
Response: {"type": "check_acks_ok", "in_reply_to": 1, "pending": 2, "timed_out": 1, "direct_sent": 3}
```

```json
Request:  {"type": "failure_stats", "msg_id": 2}
Response: {"type": "failure_stats_ok", "in_reply_to": 2, "total_failures": 1, "direct_deliveries": 3}
```

## Concepts

- fault tolerance
- tree failure
- ack timeout
- direct delivery

## Hints

- When a child node crashes, the entire subtree below it goes dark
- Track acknowledgments from children with timeouts
- If no ack within 500ms, send directly to known downstream nodes
- Maintain a list of all nodes for direct fallback
- Log failed deliveries to stderr for debugging

## Test Cases

### 1. Broadcast with no neighbors

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

### 2. Failure stats initially zero

Input:

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"failure_stats","msg_id":2}}
```

Expected output:

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
{"src": "n1", "dest": "c1", "body": {"type": "failure_stats_ok", "total_failures": 0, "direct_deliveries": 0, "in_reply_to": 2, "msg_id": 1}}
```

## Resources

- [Fault-Tolerant Broadcast](https://www.cs.cornell.edu/projects/Quicksilver/public_pdfs/2003-reliable-scalable.pdf): Cornell research on reliable broadcast in unreliable networks

## Java Starter

The matching local starter file is:

```text
src/main/java/Main.java
```
