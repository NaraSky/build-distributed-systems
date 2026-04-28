# Build Distributed Hash Table (Chord)

Website: <https://builddistributedsystem.com/tracks/advanced/tasks/task-10-2-dht>

Track: 10. Advanced
Task order: 2
Short title: DHT
Difficulty: advanced
Subtrack: Advanced Paradigms

## Problem

Build Chord DHT: nodes on ring, finger tables for routing. Achieve O(log n) lookups in P2P network.

## Concept Notes

### Chord DHT

Chord arranges nodes on hash ring. Finger tables point to nodes 2^i ahead for O(log n) hops. Used in P2P systems and some databases.

## Concepts

- DHT
- Chord
- finger table

## Hints

- Each node has ID on hash ring
- Finger table for O(log n) lookup
- Handle node join/leave

## Test Cases

### 1. Hash key to ring

Verify response contains type:chord_hash_ok with hash value between 0 and 2^6-1 (0-63). Hash should be consistent (same key always produces same hash).

Input:

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"chord_hash","msg_id":2,"key":"mykey","m":6}}
```

Expected output:

```text
{"src":"n1","dest":"c0","body":{"type":"init_ok","in_reply_to":1,"msg_id":0}}
{"src":"n1","dest":"c1","body":{"type":"chord_hash_ok","in_reply_to":2,"msg_id":1,"hash":7}}
```

## Resources

- [Chord Paper](https://pdos.csail.mit.edu/papers/chord:sigcomm01/): Chord: A Scalable P2P Lookup

## Java Starter

The matching local starter file is:

```text
src/main/java/Main.java
```
