# Architecture Decision Record: Choosing a Clock System

Website: <https://builddistributedsystem.com/tracks/timekeeper/tasks/task-4-4-5-clock-comparison-adr>

Track: 16. The Timekeeper
Task order: 20
Short title: Clock ADR
Difficulty: advanced
Subtrack: Hybrid Logical Clocks

## Problem

Write an Architecture Decision Record (ADR) for choosing a clock system for a multi-region distributed database. Compare five clock systems across multiple dimensions.

Implement a `compare_clocks` handler that generates the comparison table, and a `generate_adr` handler that produces the decision record:

```json
Request:  {"type": "compare_clocks", "msg_id": 1}
Response: {"type": "compare_clocks_ok", "in_reply_to": 1, "comparison": [
    {"system": "uuid_v4", "uniqueness": "global", "causality": "none", "size_bytes": 16, "speed_ns": 50},
    {"system": "snowflake", "uniqueness": "global", "causality": "partial_within_node", "size_bytes": 8, "speed_ns": 10},
    {"system": "lamport", "uniqueness": "none", "causality": "partial", "size_bytes": 8, "speed_ns": 5},
    {"system": "vector_clock", "uniqueness": "none", "causality": "full", "size_bytes": "8*N", "speed_ns": 10},
    {"system": "hlc", "uniqueness": "global_with_node", "causality": "full", "size_bytes": 12, "speed_ns": 15}
]}

Request:  {"type": "generate_adr", "msg_id": 2, "use_case": "multi_region_database", "regions": 3}
Response: {"type": "generate_adr_ok", "in_reply_to": 2, "decision": "hlc", "rationale": "...", "tradeoffs": ["..."], "status": "accepted"}
```

## Concepts

- architecture decision record
- clock comparison
- multi-region
- tradeoffs

## Hints

- Compare HLC, UUID v4, Snowflake, Lamport, and Vector Clocks across multiple dimensions
- Dimensions: uniqueness, causality encoding, storage size, generation speed, cross-region behavior
- For a multi-region database, HLC is the best fit because it gives both causality and time proximity
- UUID v4 gives uniqueness but no ordering; Snowflake gives ordering but no causality
- Write a structured ADR: Context, Decision, Status, Consequences

## Test Cases

### 1. Compare all clock systems

compare_clocks_ok should contain 5 entries covering uuid_v4, snowflake, lamport, vector_clock, and hlc with correct properties.

Input:

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"compare_clocks","msg_id":2}}
```

Expected output:

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

### 2. ADR for multi-region database recommends HLC

generate_adr_ok should recommend HLC for multi-region database with rationale covering causality and time proximity.

Input:

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"generate_adr","msg_id":2,"use_case":"multi_region_database","regions":3}}
```

Expected output:

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

## Resources

- [Architecture Decision Records](https://adr.github.io/): How to write and maintain Architecture Decision Records
- [Spanner: Google Globally-Distributed Database](https://research.google/pubs/pub39966/): The Spanner paper showing TrueTime and its clock system tradeoffs

## Java Starter

The matching local starter file is:

```text
src/main/java/Main.java
```
