# Tune Gossip Parameters for Maelstrom Broadcast

Website: <https://builddistributedsystem.com/tracks/gossiper/tasks/task-3-2-5-tuning>

Track: 3. The Gossiper
Task order: 10
Short title: Gossip Tuning
Difficulty: advanced
Subtrack: Gossip Protocol

## Problem

The Maelstrom broadcast workload requires messages-per-op < 30 under network partitions. Your task is to implement configurable gossip parameters and track message efficiency.

Implement a `configure` handler to set gossip parameters:
```json
Request:  {"type": "configure", "msg_id": 1, "fanout": 3, "gossip_interval_ms": 200}
Response: {"type": "configure_ok", "in_reply_to": 1}
```

And a `gossip_stats` handler to report efficiency:
```json
Request:  {"type": "gossip_stats", "msg_id": 2}
Response: {"type": "gossip_stats_ok", "in_reply_to": 2, 
           "broadcasts_received": 10, "gossip_messages_sent": 45,
           "messages_per_op": 4.5, "unique_messages": 10}
```

## Concepts

- parameter tuning
- messages-per-op
- latency tradeoff
- gossip optimization

## Hints

- messages-per-op = total messages sent / total broadcast operations
- Lower fanout = fewer messages but slower convergence
- Higher gossip interval = fewer rounds but more latency
- The sweet spot balances message overhead vs delivery reliability
- Track both metrics and expose them via a stats endpoint

## Test Cases

### 1. Configure updates fanout

Input:

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1","n2","n3"]}}
{"src":"c1","dest":"n1","body":{"type":"configure","msg_id":2,"fanout":3,"gossip_interval_ms":100}}
```

Expected output:

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
{"src": "n1", "dest": "c1", "body": {"type": "configure_ok", "in_reply_to": 2, "msg_id": 1}}
```

### 2. Stats with zero broadcasts

Input:

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"gossip_stats","msg_id":2}}
```

Expected output:

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
{"src": "n1", "dest": "c1", "body": {"type": "gossip_stats_ok", "broadcasts_received": 0, "gossip_messages_sent": 0, "messages_per_op": 0, "unique_messages": 0, "in_reply_to": 2, "msg_id": 1}}
```

## Resources

- [Fly.io Gossip Glomers - Broadcast](https://fly.io/dist-sys/3a/): Fly.io distributed systems challenge for broadcast workloads

## Java Starter

The matching local starter file is:

```text
src/main/java/Main.java
```
