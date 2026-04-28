# Implement ID Generation During Network Partition

Website: <https://builddistributedsystem.com/tracks/identifier/tasks/task-2-3-partition-resilient>

Track: 2. The Identifier
Task order: 3
Short title: Partition Resilient
Difficulty: intermediate
Subtrack: Why Unique IDs Are Hard

## Problem

Distributed systems must handle **network partitions** - times when nodes cannot communicate with each other. Your ID generator must continue working even when completely isolated from other nodes.

Test your implementation by verifying it works when:

1. The node cannot reach any other nodes
2. The network has high latency
3. Messages are being dropped

A good ID generation scheme is **fully local** and does not require coordination with other nodes.

## Concept Notes

## CAP Theorem and Availability

The CAP theorem states that during a network partition, you can have either **Consistency** or **Availability**, but not both.

ID generation should prioritize **availability**: even an isolated node should generate valid IDs.

### Local-First Design

By embedding the `node_id` in our IDs, we achieve partition tolerance. Each node can independently generate IDs that are guaranteed unique across the cluster, *without coordination*.

### The Trade-off

  
    Approach
    Consistency
    Availability
  
  
    Central ID server
    Strong (sequential IDs)
    Fails during partition
  
  
    Node-embedded IDs
    Weak (no ordering)
    Always available
  

### Clock Drift Handling

What if the clock goes *backwards*? This can happen with NTP adjustments. A robust implementation should:

  - Detect backward clock movement

  - Wait until timestamp advances, OR

  - Continue using the previous timestamp with incrementing sequence

## Concepts

- network partitions
- availability
- CAP theorem

## Hints

- Your ID generation should work without network access
- Do not depend on other nodes or external services
- Consider what happens if clocks drift
- Generated IDs must be globally unique - use timestamp + node_id + sequence to guarantee no collisions even under partition

## Test Cases

### 1. Generate basic ID

Input:

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"generate","msg_id":2}}
```

Expected output:

```text
{"src":"n1","dest":"c0","body":{"type":"init_ok","in_reply_to":1,"msg_id":0}}
{"src":"n1","dest":"c1","body":{"type":"generate_ok","in_reply_to":2,"msg_id":1,"id":"n1-0"}}
```

## Resources

- [CAP Theorem](https://en.wikipedia.org/wiki/CAP_theorem): Understanding the trade-offs in distributed systems

## Java Starter

The matching local starter file is:

```text
src/main/java/Main.java
```
