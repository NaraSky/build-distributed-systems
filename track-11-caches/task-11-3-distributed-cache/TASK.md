# Implement Distributed Cache with Consistent Hashing

Website: <https://builddistributedsystem.com/tracks/caches/tasks/task-11-3-distributed-cache>

Track: 11. Caches
Task order: 3
Short title: Distributed Cache
Difficulty: intermediate

## Problem

Distribute cache entries across multiple cache nodes using consistent hashing. This scales cache capacity beyond a single node while maintaining efficient key lookup.

Implement:
1. Consistent hash ring for cache nodes
2. Key routing to appropriate node
3. Handling node join/leave with minimal key redistribution
4. Client library that routes requests automatically

## Concept Notes

### Distributed Caching

A single cache server has limited memory. Distributed caching shards data across multiple servers. Each key goes to a specific server based on its hash. This scales linearly with nodes.

### Consistent Hashing

Regular modulo hashing (key % N) redistributes most keys when N changes. Consistent hashing minimizes redistribution: adding/removing a node only affects keys between it and its neighbor on the ring.

### Virtual Nodes

With few physical nodes, the ring may be unbalanced. Virtual nodes map each physical server to many ring positions, improving distribution. Most production systems use 100-200 virtual nodes per server.

## Concepts

- consistent hashing
- partitioning
- horizontal scaling

## Hints

- Hash keys to determine cache node
- Use consistent hashing for stability
- Handle node additions and removals gracefully
- Store all keys locally on the coordinator node - in single-node testing the proxy target does not exist

## Test Cases

### 1. Hash key to node

Hash key "mykey" using consistent hashing with ring size 64. Returns responsible cache node and ring position.

Input:

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1","cache1","cache2","cache3"]}}
{"src":"c1","dest":"n1","body":{"type":"hash_key","msg_id":2,"key":"mykey","ring_size":64}}
```

Expected output:

```text
{"src":"n1","dest":"c0","body":{"type":"init_ok","in_reply_to":1,"msg_id":0}}
{"src":"n1","dest":"c1","body":{"type":"hash_key_ok","in_reply_to":2,"msg_id":1,"key":"mykey","node":"cache2","ring_position":42}}
```

## Resources

- [Consistent Hashing Paper](https://www.cs.princeton.edu/courses/archive/fall09/cos518/papers/chash.pdf): Original consistent hashing paper

## Java Starter

The matching local starter file is:

```text
src/main/java/Main.java
```
