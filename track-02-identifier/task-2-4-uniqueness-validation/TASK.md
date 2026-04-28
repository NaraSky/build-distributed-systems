# Validate Uniqueness Across Distributed Nodes

Website: <https://builddistributedsystem.com/tracks/identifier/tasks/task-2-4-uniqueness-validation>

Track: 2. The Identifier
Task order: 4
Short title: Uniqueness Validation
Difficulty: intermediate
Subtrack: Why Unique IDs Are Hard

## Problem

Run your ID generator through Maelstrom verification to prove uniqueness. Maelstrom collects all generated IDs across all nodes and checks for duplicates.

Your implementation must pass with:

- Multiple nodes generating concurrently
- High throughput (thousands of IDs per second)
- Network partitions separating nodes

Think about **why** your scheme guarantees uniqueness. What assumptions does it make? What could cause collisions?

## Concept Notes

## Proving Uniqueness

A strong ID scheme should have a **provable uniqueness guarantee**.

### The Proof Structure

If IDs combine:

  - `node_id` - unique per node

  - `timestamp` - monotonic

  - `sequence` - unique per timestamp

Then uniqueness is guaranteed as long as:

  - Node IDs are unique

  - Clocks do not go backwards more than a tolerable amount

  - Sequence does not overflow

### Failure Modes

  
    Failure
    Cause
    Mitigation
  
  
    Clock sync issue
    NTP adjustment
    Wait or use previous timestamp
  
  
    Node ID reuse
    Node restart with same ID
    Persist counter or use epoch
  
  
    Sequence overflow
    >4096 IDs/ms
    Wait for next millisecond

## Concepts

- testing
- verification
- global uniqueness

## Hints

- Maelstrom will verify uniqueness automatically
- Consider mathematical proof of your ID uniqueness
- Document your uniqueness guarantees

## Test Cases

### 1. Generate two IDs with proper format

Input:

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"generate","msg_id":2}}
{"src":"c2","dest":"n1","body":{"type":"generate","msg_id":3}}
```

Expected output:

```text
{"src":"n1","dest":"c0","body":{"type":"init_ok","in_reply_to":1,"msg_id":0}}
{"src":"n1","dest":"c1","body":{"type":"generate_ok","in_reply_to":2,"msg_id":1,"id":"n1-0"}}
{"src":"n1","dest":"c2","body":{"type":"generate_ok","in_reply_to":3,"msg_id":2,"id":"n1-1"}}
```

## Resources

- [Maelstrom Unique IDs Workload](https://github.com/jepsen-io/maelstrom/blob/main/doc/workloads.md#workload-unique-ids): Specification for the unique-ids workload

## Java Starter

The matching local starter file is:

```text
src/main/java/Main.java
```
