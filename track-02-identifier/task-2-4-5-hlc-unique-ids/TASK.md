# HLC-Based Unique ID Generation for Maelstrom

Website: <https://builddistributedsystem.com/tracks/identifier/tasks/task-2-4-5-hlc-unique-ids>

Track: 2. The Identifier
Task order: 20
Short title: HLC Unique IDs
Difficulty: advanced
Subtrack: Hybrid Logical Clocks (HLC)

## Problem

Integrate HLC-based IDs into the Maelstrom `generate` workload. Each generated ID must be globally unique across all nodes and should preserve causal ordering.

ID format: `"{pt}_{lc}_{node_id}"` (e.g., "1704067200001_0_n1")

Implement the standard Maelstrom `generate` handler:
```json
Request:  {"type": "generate", "msg_id": 1}
Response: {"type": "generate_ok", "in_reply_to": 1, "id": "1704067200001_0_n1"}
```

Also implement `parse_hlc_id` to decompose an HLC ID:
```json
Request:  {"type": "parse_hlc_id", "msg_id": 2, "id": "1704067200001_3_n2"}
Response: {"type": "parse_hlc_id_ok", "in_reply_to": 2, "pt": 1704067200001, "lc": 3, "node": "n2"}
```

## Concepts

- unique ID generation
- Maelstrom workload
- linearizability
- HLC integration

## Hints

- Combine HLC timestamp with node_id for globally unique IDs
- Format: pt_lc_nodeId ensures uniqueness across nodes
- HLC guarantees monotonicity even with clock skew
- The Maelstrom generate workload requires globally unique IDs
- Verify uniqueness by collecting IDs from all nodes

## Test Cases

### 1. Generate produces HLC-formatted ID

generate_ok should have id matching pattern "\d+_\d+_n1".

Input:

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"generate","msg_id":2}}
```

Expected output:

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

### 2. Parse HLC ID extracts components

Input:

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"parse_hlc_id","msg_id":2,"id":"1704067200001_3_n2"}}
```

Expected output:

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
{"src": "n1", "dest": "c1", "body": {"type": "parse_hlc_id_ok", "pt": 1704067200001, "lc": 3, "node": "n2", "in_reply_to": 2, "msg_id": 1}}
```

## Resources

- [Spanner: Google Globally Distributed Database](https://research.google/pubs/pub39966/): Google Spanner paper on TrueTime and clocks

## Java Starter

The matching local starter file is:

```text
src/main/java/Main.java
```
