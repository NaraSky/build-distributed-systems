# Implement Vector Clocks

Website: <https://builddistributedsystem.com/tracks/identifier/tasks/task-2-3-3-vector-clock>

Track: 2. The Identifier
Task order: 13
Short title: Vector Clock
Difficulty: advanced
Subtrack: Logical Clocks as IDs

## Problem

Vector clocks solve the limitation of Lamport clocks: they can detect **concurrent events**. Each node maintains a vector of N counters (one per node). The rules are:

1. On **local event** or **send**: increment your own slot in the vector
2. On **receive**: take element-wise max of local and received vectors, then increment your own slot

Two events are concurrent if neither vector dominates the other: A || B when A[i] > B[i] for some i, and A[j] < B[j] for some j.

Implement a `vc_tick` handler:
```json
Request:  {"type": "vc_tick", "msg_id": 1}
Response: {"type": "vc_tick_ok", "in_reply_to": 1, "vector": {"n1": 1, "n2": 0}}
```

And a `vc_receive` handler that merges an incoming vector:
```json
Request:  {"type": "vc_receive", "msg_id": 2, "vector": {"n1": 0, "n2": 3}}
Response: {"type": "vc_receive_ok", "in_reply_to": 2, "vector": {"n1": 2, "n2": 3}}
```

## Concepts

- vector clock
- causality tracking
- element-wise max
- concurrent detection

## Hints

- Each node maintains a vector of N counters, one per node in the cluster
- On local event or send: increment your own slot
- On receive: element-wise max, then increment your own slot
- Vector clocks can distinguish concurrent events from causal ones
- Initialize the vector with zeros for all known node IDs

## Test Cases

### 1. Tick increments own slot

Input:

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1","n2"]}}
{"src":"c1","dest":"n1","body":{"type":"vc_tick","msg_id":2}}
```

Expected output:

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
{"src": "n1", "dest": "c1", "body": {"type": "vc_tick_ok", "vector": {"n1": 1, "n2": 0}, "in_reply_to": 2, "msg_id": 1}}
```

### 2. Merge takes element-wise max and increments own

After tick n1=1,n2=0. Merge with {n1:0,n2:5} -> max -> {n1:1,n2:5}, then increment own -> {n1:2,n2:5}.

Input:

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1","n2"]}}
{"src":"c1","dest":"n1","body":{"type":"vc_tick","msg_id":2}}
{"src":"n2","dest":"n1","body":{"type":"vc_receive","msg_id":3,"vector":{"n1":0,"n2":5}}}
```

Expected output:

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
{"src": "n1", "dest": "c1", "body": {"type": "vc_tick_ok", "vector": {"n1": 1, "n2": 0}, "in_reply_to": 2, "msg_id": 1}}
{"src": "n1", "dest": "n2", "body": {"type": "vc_receive_ok", "vector": {"n1": 2, "n2": 5}, "in_reply_to": 3, "msg_id": 2}}
```

## Resources

- [Vector Clocks Revisited](https://riak.com/posts/technical/vector-clocks-revisited/): Riak documentation on practical use of vector clocks

## Java Starter

The matching local starter file is:

```text
src/main/java/Main.java
```
