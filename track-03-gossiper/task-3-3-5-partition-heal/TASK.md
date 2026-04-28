# Simulate Network Partition and Healing

Website: <https://builddistributedsystem.com/tracks/gossiper/tasks/task-3-3-5-partition-heal>

Track: 3. The Gossiper
Task order: 15
Short title: Partition Heal
Difficulty: advanced
Subtrack: Topology-Aware Gossip

## Problem

Network partitions split the cluster into isolated groups. After the partition heals, gossip must merge the diverged states. Your task is to simulate this.

Implement:
1. `partition` - Block messages to specified nodes
2. `heal` - Unblock all nodes  
3. `partition_status` - Report current partition state

```json
Request:  {"type": "partition", "msg_id": 1, "blocked": ["n3", "n4"]}
Response: {"type": "partition_ok", "in_reply_to": 1}

Request:  {"type": "heal", "msg_id": 2}
Response: {"type": "heal_ok", "in_reply_to": 2}

Request:  {"type": "partition_status", "msg_id": 3}
Response: {"type": "partition_status_ok", "in_reply_to": 3, "blocked": [], "is_partitioned": false, "messages_dropped": 5}
```

## Concepts

- network partition
- partition healing
- convergence
- split brain

## Hints

- A partition blocks all messages between two groups of nodes
- Each side continues to gossip internally
- On healing, cross-partition gossip resumes and states converge
- Track time-to-convergence after partition heals
- Implement partition as a blocked-destinations set

## Test Cases

### 1. Partition blocks specified nodes

Input:

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1","n2"]}}
{"src":"c1","dest":"n1","body":{"type":"partition","msg_id":2,"blocked":["n2"]}}
{"src":"c1","dest":"n1","body":{"type":"partition_status","msg_id":3}}
```

Expected output:

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
{"src": "n1", "dest": "c1", "body": {"type": "partition_ok", "in_reply_to": 2, "msg_id": 1}}
{"src": "n1", "dest": "c1", "body": {"type": "partition_status_ok", "blocked": ["n2"], "is_partitioned": true, "messages_dropped": 0, "in_reply_to": 3, "msg_id": 2}}
```

### 2. Heal removes all blocks

Input:

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1","n2"]}}
{"src":"c1","dest":"n1","body":{"type":"partition","msg_id":2,"blocked":["n2"]}}
{"src":"c1","dest":"n1","body":{"type":"heal","msg_id":3}}
{"src":"c1","dest":"n1","body":{"type":"partition_status","msg_id":4}}
```

Expected output:

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
{"src": "n1", "dest": "c1", "body": {"type": "partition_ok", "in_reply_to": 2, "msg_id": 1}}
{"src": "n1", "dest": "c1", "body": {"type": "heal_ok", "in_reply_to": 3, "msg_id": 2}}
{"src": "n1", "dest": "c1", "body": {"type": "partition_status_ok", "blocked": [], "is_partitioned": false, "messages_dropped": 0, "in_reply_to": 4, "msg_id": 3}}
```

## Resources

- [Jepsen: Network Partitions](https://jepsen.io/analyses): Jepsen analyses of how databases handle network partitions

## Java Starter

The matching local starter file is:

```text
src/main/java/Main.java
```
