# Implement Hybrid Tree and Gossip Broadcast

Website: <https://builddistributedsystem.com/tracks/gossiper/tasks/task-3-3-3-hybrid-gossip>

Track: 3. The Gossiper
Task order: 13
Short title: Hybrid Gossip
Difficulty: advanced
Subtrack: Topology-Aware Gossip

## Problem

Pure tree broadcast is fast but fragile. Pure gossip is reliable but slow and wasteful. A **hybrid** approach uses tree for the first hop (fast, efficient) and gossip for reliability (catch stragglers).

Implement a hybrid broadcast:
1. On broadcast, forward via tree neighbors immediately
2. Periodically gossip all known messages to random peers (catch-up)
3. Track delivery path for each message (tree vs gossip)

```json
Request:  {"type": "delivery_info", "msg_id": 1, "value": 42}
Response: {"type": "delivery_info_ok", "in_reply_to": 1, "value": 42, "delivered_via": "tree", "hops": 1}
```

```json
Request:  {"type": "hybrid_stats", "msg_id": 2}
Response: {"type": "hybrid_stats_ok", "in_reply_to": 2, "tree_deliveries": 8, "gossip_deliveries": 2, "total": 10}
```

## Concepts

- hybrid broadcast
- tree overlay
- gossip fallback
- convergence speed

## Hints

- First hop uses the tree for fast delivery (low latency)
- Background gossip rounds catch any missed nodes (high reliability)
- Track whether each message was delivered via tree or gossip
- Compare convergence speed of pure tree, pure gossip, and hybrid
- The hybrid approach gives the best of both worlds

## Test Cases

### 1. Broadcast via tree tracks delivery

Input:

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"topology","msg_id":2,"topology":{"n1":[]}}}
{"src":"c1","dest":"n1","body":{"type":"broadcast","msg_id":3,"message":42}}
{"src":"c1","dest":"n1","body":{"type":"delivery_info","msg_id":4,"value":42}}
```

Expected output:

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
{"src": "n1", "dest": "c1", "body": {"type": "topology_ok", "in_reply_to": 2, "msg_id": 1}}
{"src": "n1", "dest": "c1", "body": {"type": "broadcast_ok", "in_reply_to": 3, "msg_id": 2}}
{"src": "n1", "dest": "c1", "body": {"type": "delivery_info_ok", "value": 42, "delivered_via": "tree", "hops": 0, "in_reply_to": 4, "msg_id": 3}}
```

### 2. Hybrid stats with zero messages

Input:

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"hybrid_stats","msg_id":2}}
```

Expected output:

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
{"src": "n1", "dest": "c1", "body": {"type": "hybrid_stats_ok", "tree_deliveries": 0, "gossip_deliveries": 0, "total": 0, "in_reply_to": 2, "msg_id": 1}}
```

## Resources

- [Plumtree: Epidemic Broadcast Trees](https://asc.di.fct.unl.pt/~jleitao/pdf/srds07-leitao.pdf): Paper on combining tree and gossip for efficient broadcast

## Java Starter

The matching local starter file is:

```text
src/main/java/Main.java
```
