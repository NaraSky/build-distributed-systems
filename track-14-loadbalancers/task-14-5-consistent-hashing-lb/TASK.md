# Implement Consistent Hashing for Load Balancing

Website: <https://builddistributedsystem.com/tracks/loadbalancers/tasks/task-14-5-consistent-hashing-lb>

Track: 14. Load Balancers
Task order: 5
Short title: Consistent Hash LB
Difficulty: advanced
Subtrack: Layer 4 Load Balancing

## Problem

Implement consistent hashing for stateful load balancing:

1. Assign servers to positions on hash ring
2. Hash each request key to ring position
3. Route to server clockwise from hash position
4. When servers join/leave, only nearby keys move

This maintains cache locality - same user always hits same server, maximizing cache hits.

## Concept Notes

### Consistent Hashing for LB

For stateful services or caching, you want related requests to hit the same server. Consistent hashing routes based on a key (user ID, session), ensuring same key -> same server while minimizing redistribution.

### Virtual Nodes

With few servers, distribution can be uneven. Virtual nodes map each server to many ring positions, smoothing the distribution.

## Concepts

- consistent hashing
- key affinity
- cache locality

## Hints

- Hash request key to server
- Same key always goes to same server
- Minimal redistribution on server changes

## Test Cases

### 1. Consistent routing

Load balancer uses consistent hashing with 3 servers (s1, s2, s3). Request with key "user123" routes to s2. Subsequent requests with same key "user123" should always route to s2. Verify consistent routing based on request key.

Input:

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
```

Expected output:

```text
{"src":"n1","dest":"c0","body":{"type":"init_ok","in_reply_to":1,"msg_id":0}}
```

### 2. Minimal redistribution

Load balancer with 3 servers handling 1000 keys. Add 4th server s4. With consistent hashing, only ~250 keys (1000/4) should remap to s4. Other keys stay on original servers. Verify adding node causes minimal redistribution compared to modulo hashing.

Input:

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
```

Expected output:

```text
{"src":"n1","dest":"c0","body":{"type":"init_ok","in_reply_to":1,"msg_id":0}}
```

## Java Starter

The matching local starter file is:

```text
src/main/java/Main.java
```
