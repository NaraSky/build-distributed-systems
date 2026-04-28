# Add Message Batching to Reduce Network Overhead

Website: <https://builddistributedsystem.com/tracks/gossiper/tasks/task-3-4-batching>

Track: 3. The Gossiper
Task order: 4
Short title: Message Batching
Difficulty: intermediate
Subtrack: Naive Broadcast (Flooding)

## Problem

Reduce network overhead by batching multiple messages into single transmissions. Instead of sending immediately, buffer messages and flush periodically or when the buffer reaches a threshold.

## Concept Notes

### Batching Trade-offs

Batching improves throughput by reducing per-message overhead but increases latency. The optimal batch size depends on message rate, network latency, and consistency requirements.

## Concepts

- batching
- throughput optimization
- latency tradeoff

## Hints

- Buffer messages before sending
- Use a time-based flush
- Balance latency vs throughput

## Test Cases

### 1. Messages are batched together

Input:

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c0","dest":"n1","body":{"type":"topology","msg_id":2,"topology":{"n1":[]}}}
{"src":"c1","dest":"n1","body":{"type":"broadcast","msg_id":3,"message":1}}
{"src":"c2","dest":"n1","body":{"type":"broadcast","msg_id":4,"message":2}}
{"src":"c3","dest":"n1","body":{"type":"broadcast","msg_id":5,"message":3}}
{"src":"c4","dest":"n1","body":{"type":"read","msg_id":6}}
```

Expected output:

```text
{"src":"n1","dest":"c0","body":{"type":"init_ok","in_reply_to":1,"msg_id":0}}
{"src":"n1","dest":"c0","body":{"type":"topology_ok","in_reply_to":2,"msg_id":1}}
{"src":"n1","dest":"c1","body":{"type":"broadcast_ok","in_reply_to":3,"msg_id":2}}
{"src":"n1","dest":"c2","body":{"type":"broadcast_ok","in_reply_to":4,"msg_id":3}}
{"src":"n1","dest":"c3","body":{"type":"broadcast_ok","in_reply_to":5,"msg_id":4}}
{"src":"n1","dest":"c4","body":{"type":"read_ok","in_reply_to":6,"msg_id":5,"messages":[1,2,3]}}
```

## Java Starter

The matching local starter file is:

```text
src/main/java/Main.java
```
