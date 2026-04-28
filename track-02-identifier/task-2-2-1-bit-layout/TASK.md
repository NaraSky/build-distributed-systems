# Implement Snowflake ID Bit Layout

Website: <https://builddistributedsystem.com/tracks/identifier/tasks/task-2-2-1-bit-layout>

Track: 2. The Identifier
Task order: 6
Short title: Bit Layout
Difficulty: intermediate
Subtrack: Snowflake IDs (Twitter's Approach)

## Problem

Twitter's Snowflake generates unique, roughly-sorted 64-bit IDs without coordination. The layout is:

```
| 1 bit unused | 41 bits timestamp | 10 bits machine ID | 12 bits sequence |
|     0        |   ms since epoch  |    0-1023          |    0-4095        |
```

Your task is to implement functions that:

1. **Compose** a Snowflake ID from its three components (timestamp_ms, machine_id, sequence)
2. **Decompose** a Snowflake ID back into its components
3. Handle the Maelstrom `generate` workload using Snowflake IDs

Implement a `generate` message handler:
```json
Request:  {"type": "generate", "msg_id": 1}
Response: {"type": "generate_ok", "in_reply_to": 1, "id": 7041429939834880}
```

And a `decompose` handler for debugging:
```json
Request:  {"type": "decompose", "msg_id": 2, "id": 7041429939834880}
Response: {"type": "decompose_ok", "in_reply_to": 2, "timestamp_ms": 1678886400000, "machine_id": 1, "sequence": 0}
```

## Concepts

- bit manipulation
- Snowflake ID
- bit layout
- scalability

## Hints

- Use left shift (<<) to position each component in the 64-bit integer
- Timestamp goes in the top 41 bits, machine ID in the next 10, sequence in the bottom 12
- Use bitwise OR (|) to combine the components
- To extract components, use right shift (>>) and bitwise AND (&) with masks
- Max IDs per ms per node = 2^12 = 4096

## Test Cases

### 1. Init and generate produces an ID

The second line should be a generate_ok with a numeric id field. Exact value varies by timestamp.

Input:

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"generate","msg_id":2}}
```

Expected output:

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

### 2. Two sequential generates produce different IDs

Two generate_ok responses with different id values. The second ID should be greater than or equal to the first.

Input:

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"generate","msg_id":2}}
{"src":"c1","dest":"n1","body":{"type":"generate","msg_id":3}}
```

Expected output:

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

## Resources

- [Twitter Snowflake (Original Announcement)](https://blog.twitter.com/engineering/en_us/a/2010/announcing-snowflake): Twitter engineering blog post introducing Snowflake ID generation

## Java Starter

The matching local starter file is:

```text
src/main/java/Main.java
```
