# Add Periodic Gossip Rounds on a Timer

Website: <https://builddistributedsystem.com/tracks/gossiper/tasks/task-3-2-3-gossip-timer>

Track: 3. The Gossiper
Task order: 8
Short title: Gossip Timer
Difficulty: intermediate
Subtrack: Gossip Protocol

## Problem

Instead of only gossiping when a new broadcast arrives, add **periodic gossip rounds**: every interval, pick K random peers and send them all your known messages. This ensures convergence even if messages are dropped.

Implement a `gossip_round` handler that triggers a single gossip round:
```json
Request:  {"type": "gossip_round", "msg_id": 1}
Response: {"type": "gossip_round_ok", "in_reply_to": 1, "peers_contacted": 2, "messages_sent": 5}
```

And a `gossip_sync` handler that receives a full state from a peer:
```json
Request:  {"type": "gossip_sync", "msg_id": 1, "messages": [1, 2, 3]}
Response: {"type": "gossip_sync_ok", "in_reply_to": 1, "new_count": 2}
```

The sync handler merges the received messages with the local set and reports how many were new.

## Concepts

- periodic gossip
- convergence time
- anti-entropy
- pull gossip

## Hints

- Push gossip sends on broadcast; pull gossip syncs periodically
- A gossip round checks all known messages against a random peer
- Track convergence: how many rounds until all nodes have all messages
- The timer interval affects latency vs message overhead tradeoff
- Implement gossip_round as a message type triggered externally for testing

## Test Cases

### 1. Gossip round with no messages sends nothing

gossip_round_ok should show peers_contacted=2 and messages_sent=0 (no messages to send).

Input:

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1","n2","n3"]}}
{"src":"c1","dest":"n1","body":{"type":"gossip_round","msg_id":2}}
```

Expected output:

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

### 2. Gossip sync merges new messages

Input:

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"broadcast","msg_id":2,"message":10}}
{"src":"n2","dest":"n1","body":{"type":"gossip_sync","msg_id":3,"messages":[10,20,30]}}
{"src":"c1","dest":"n1","body":{"type":"read","msg_id":4}}
```

Expected output:

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
{"src": "n1", "dest": "c1", "body": {"type": "broadcast_ok", "in_reply_to": 2, "msg_id": 1}}
{"src": "n1", "dest": "n2", "body": {"type": "gossip_sync_ok", "new_count": 2, "in_reply_to": 3, "msg_id": 2}}
{"src": "n1", "dest": "c1", "body": {"type": "read_ok", "messages": [10, 20, 30], "in_reply_to": 4, "msg_id": 3}}
```

## Resources

- [Anti-Entropy Gossip Protocols](https://www.distributed-systems.net/my-data/papers/2007.osr.pdf): Overview of push, pull, and push-pull gossip strategies

## Java Starter

The matching local starter file is:

```text
src/main/java/Main.java
```
