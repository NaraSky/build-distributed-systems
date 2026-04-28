# Compare HLC, UUID v4, and Snowflake IDs

Website: <https://builddistributedsystem.com/tracks/identifier/tasks/task-2-4-4-id-comparison>

Track: 2. The Identifier
Task order: 19
Short title: ID Comparison
Difficulty: intermediate
Subtrack: Hybrid Logical Clocks (HLC)

## Problem

Different ID schemes have different tradeoffs. Your task is to implement all three and return a comparison table.

Implement a `compare_ids` handler that generates one ID of each type and reports their properties:

```json
Request:  {"type": "compare_ids", "msg_id": 1}
Response: {"type": "compare_ids_ok", "in_reply_to": 1, "comparison": [
    {"scheme": "uuid_v4", "id": "550e8400-e29b...", "bits": 128, "sortable": false, "causal": false},
    {"scheme": "snowflake", "id": "7041429939834880", "bits": 64, "sortable": true, "causal": false},
    {"scheme": "hlc", "id": "1234567-0-n1", "bits": 96, "sortable": true, "causal": true}
]}
```

## Concepts

- UUID
- Snowflake
- HLC
- ID tradeoffs
- benchmarking

## Hints

- UUID v4 is random: 128 bits, no ordering, no coordination needed
- Snowflake is timestamped: 64 bits, sorted, needs machine_id assignment
- HLC is timestamped + causal: variable size, captures causality, needs clock sync
- Compare: storage size, generation speed, uniqueness guarantee, sortability
- Each approach has different tradeoffs for different use cases

## Test Cases

### 1. Compare IDs returns three schemes

compare_ids_ok should contain a comparison array with 3 entries: uuid_v4, snowflake, and hlc. Each has id, bits, sortable, and causal fields.

Input:

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"compare_ids","msg_id":2}}
```

Expected output:

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

## Resources

- [UUID Versions Explained](https://www.ietf.org/rfc/rfc4122.txt): RFC 4122 defining UUID format and versions

## Java Starter

The matching local starter file is:

```text
src/main/java/Main.java
```
