# Implement Peer-to-Peer Gossip with Random Neighbors

Website: <https://builddistributedsystem.com/tracks/gossiper/tasks/task-3-3-random-gossip>

Track: 3. The Gossiper
Task order: 3
Short title: Random Gossip
Difficulty: intermediate
Subtrack: Naive Broadcast (Flooding)

## Problem

Implement a gossip protocol where each node randomly selects neighbors to share information with. This provides robustness against node failures while keeping message overhead reasonable.

## Concept Notes

### Gossip Protocols

Gossip, or epidemic, protocols spread information like a disease. Each infected node randomly selects peers to infect. This provides probabilistic guarantees of delivery with tunable overhead.

## Concepts

- gossip protocol
- random selection
- probabilistic broadcast

## Hints

- Randomly select a subset of neighbors
- Retry periodically for reliability
- Balance between speed and overhead

## Test Cases

### 1. Random gossip spreads message to all nodes

Input:

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c0","dest":"n1","body":{"type":"topology","msg_id":2,"topology":{"n1":[]}}}
{"src":"c1","dest":"n1","body":{"type":"broadcast","msg_id":3,"message":99}}
{"src":"c1","dest":"n1","body":{"type":"read","msg_id":4}}
```

Expected output:

```text
{"src":"n1","dest":"c0","body":{"type":"init_ok","in_reply_to":1,"msg_id":0}}
{"src":"n1","dest":"c0","body":{"type":"topology_ok","in_reply_to":2,"msg_id":1}}
{"src":"n1","dest":"c1","body":{"type":"broadcast_ok","in_reply_to":3,"msg_id":2}}
{"src":"n1","dest":"c1","body":{"type":"read_ok","in_reply_to":4,"msg_id":3,"messages":[99]}}
```

## Resources

- [Epidemic Algorithms](https://www.cs.cornell.edu/courses/cs6410/2018fa/slides/18-gossip-epidemic.pdf): Academic overview of epidemic/gossip protocols

## Java Starter

The matching local starter file is:

```text
src/main/java/Main.java
```
