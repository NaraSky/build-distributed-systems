# Implement Consistent Hashing for Sharding

Website: <https://builddistributedsystem.com/tracks/sharder/tasks/task-8-2-consistent-hash>

Track: 8. The Sharder
Task order: 2
Short title: Consistent Hash
Difficulty: intermediate
Subtrack: Range Sharding

## Problem

Use consistent hashing for shard assignment:

1. Place shards on a hash ring
2. Hash each key to a ring position
3. Find the next shard clockwise from key position
4. Use virtual nodes for better distribution
5. Minimize key movement when shards join/leave

## Concept Notes

### Consistent Hashing for Sharding

Traditional modulo hashing (key % N) redistributes most keys when N changes. Consistent hashing only moves keys between affected neighbors, minimizing data migration during rebalancing.

### Virtual Nodes

With few shards, the ring may be imbalanced. Virtual nodes give each shard multiple ring positions, smoothing distribution. Typically 100-200 virtual nodes per shard.

## Concepts

- consistent hashing
- key distribution
- virtual nodes

## Hints

- Hash keys to ring positions
- Use virtual nodes for balance
- Minimal movement on changes

## Test Cases

### 1. Hash key to ring

Hash returns a numeric value. Exact hash depends on implementation but must be deterministic.

Input:

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"hash_key","msg_id":2,"key":"mykey"}}
```

Expected output:

```text
{"src":"n1","dest":"c0","body":{"type":"init_ok","in_reply_to":1,"msg_id":0}}
{"src":"n1","dest":"c1","body":{"type":"hash_key_ok","in_reply_to":2,"msg_id":1,"key":"mykey"}}
```

## Java Starter

The matching local starter file is:

```text
src/main/java/Main.java
```
