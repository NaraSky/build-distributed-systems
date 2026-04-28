# Implement Gossip Fanout with Random Peer Selection

Website: <https://builddistributedsystem.com/tracks/gossiper/tasks/task-3-2-1-gossip-fanout>

Track: 3. The Gossiper
Task order: 6
Short title: Gossip Fanout
Difficulty: intermediate
Subtrack: Gossip Protocol

## Problem

Gossip protocols spread information probabilistically: instead of broadcasting to all nodes, each node forwards to K random peers. This is more resilient than tree-based broadcast because there is no single point of failure.

Your task is to implement gossip fanout:

1. Maintain a set of known messages (seen set)
2. On receiving a `broadcast` message, add the value to the seen set
3. Forward (gossip) the value to K random peers (default K=2)
4. On receiving a `read` message, return all known values
5. Track gossip statistics

```json
Broadcast: {"type": "broadcast", "msg_id": 1, "message": 42}
Response:  {"type": "broadcast_ok", "in_reply_to": 1}

Read:     {"type": "read", "msg_id": 2}
Response: {"type": "read_ok", "in_reply_to": 2, "messages": [42]}
```

## Concepts

- gossip protocol
- fanout
- random peer selection
- probabilistic broadcast

## Hints

- Pick K random peers from the cluster on each gossip round
- Do not gossip to yourself or to the message source
- Start with fanout K=2 for reasonable coverage
- Use random.sample to select peers without replacement
- Track which messages you have already seen to avoid re-gossip

## Test Cases

### 1. Broadcast stores value and replies ok

Should output init_ok, then gossip messages to peers, then broadcast_ok. Order of gossip vs ok may vary.

Input:

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1","n2","n3"]}}
{"src":"c1","dest":"n1","body":{"type":"broadcast","msg_id":2,"message":42}}
```

Expected output:

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

### 2. Read returns stored messages

Input:

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"broadcast","msg_id":2,"message":10}}
{"src":"c1","dest":"n1","body":{"type":"broadcast","msg_id":3,"message":20}}
{"src":"c1","dest":"n1","body":{"type":"read","msg_id":4}}
```

Expected output:

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
{"src": "n1", "dest": "c1", "body": {"type": "broadcast_ok", "in_reply_to": 2, "msg_id": 1}}
{"src": "n1", "dest": "c1", "body": {"type": "broadcast_ok", "in_reply_to": 3, "msg_id": 2}}
{"src": "n1", "dest": "c1", "body": {"type": "read_ok", "messages": [10, 20], "in_reply_to": 4, "msg_id": 3}}
```

## Resources

- [Epidemic Algorithms for Replicated Database Maintenance](https://dl.acm.org/doi/10.1145/41840.41841): Original 1987 paper on gossip-based replication by Demers et al.

## Java Starter

The matching local starter file is:

```text
src/main/java/Main.java
```
