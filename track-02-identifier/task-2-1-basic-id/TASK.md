# Generate Unique IDs Using Node ID and Timestamp

Website: <https://builddistributedsystem.com/tracks/identifier/tasks/task-2-1-basic-id>

Track: 2. The Identifier
Task order: 1
Short title: Basic ID Generation
Difficulty: beginner
Subtrack: Why Unique IDs Are Hard

## Problem

Distributed systems need unique identifiers for entities, events, and messages. Without a central authority, each node must generate IDs independently while avoiding collisions.

Implement a generate workload handler that responds to generate requests with unique IDs:

```json
{
  "type": "generate",
  "msg_id": 1
}
```

Your response should be:

```json
{
  "type": "generate_ok",
  "msg_id": 1,
  "in_reply_to": 1,
  "id": "unique-id-here"
}
```

For this first implementation, combine your node_id with a timestamp to create IDs. This provides uniqueness across nodes (different node_ids) and over time (different timestamps).

## Concept Notes

## Why Unique IDs Matter

Every **database record**, every **log entry**, every **message** needs an identifier. In a distributed system, you cannot simply increment a counter because multiple nodes might generate the same number simultaneously.

### The Collision Problem

Consider a simple counter-based approach:

```text
Node A: counter = 1 → generates ID 1
Node B: counter = 1 → generates ID 1  // COLLISION!
```

Both nodes generate the same ID because they have *no coordination*.

### Timestamp-Based IDs

Timestamps provide a natural ordering and uniqueness over time, but two nodes might generate the same timestamp. By including the `node_id`, we guarantee uniqueness across nodes:

```text
ID = "{node_id}-{timestamp}"

Node A: "n1-1704067200000"
Node B: "n2-1704067200000"  // Different node_id = unique
```

### Remaining Challenge

However, a single node might still generate duplicate IDs within the same millisecond. We'll address this in the next task.

## Concepts

- unique IDs
- timestamps
- node identity

## Hints

- Combine node_id with a timestamp for basic uniqueness
- Consider using millisecond precision
- Format: node_id-timestamp-sequence

## Test Cases

### 1. Generate single ID with init

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

- [Unique ID Generation Challenge](https://fly.io/dist-sys/2/): Fly.io Gossip Glomers unique ID generation walkthrough

## Java Starter

The matching local starter file is:

```text
src/main/java/Main.java
```
