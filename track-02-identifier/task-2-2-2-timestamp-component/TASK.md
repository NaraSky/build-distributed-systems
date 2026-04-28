# Implement Timestamp Component with Custom Epoch

Website: <https://builddistributedsystem.com/tracks/identifier/tasks/task-2-2-2-timestamp-component>

Track: 2. The Identifier
Task order: 7
Short title: Custom Epoch
Difficulty: intermediate
Subtrack: Snowflake IDs (Twitter's Approach)

## Problem

The timestamp component of a Snowflake ID uses 41 bits to represent milliseconds since a **custom epoch**. Using Unix epoch (1970-01-01) wastes over 50 years of timestamp space. A custom epoch starting in 2024 gives the system ~69 years of IDs.

Your task is to:

1. Implement timestamp generation relative to a custom epoch (2024-01-01 00:00:00 UTC)
2. Validate that the timestamp fits within 41 bits
3. Implement a `time_info` message that reports the current timestamp state

```json
Request:  {"type": "time_info", "msg_id": 1}
Response: {"type": "time_info_ok", "in_reply_to": 1, 
           "current_ms": 1234567, 
           "custom_epoch_ms": 1704067200000,
           "max_timestamp_ms": 2199023255551,
           "years_remaining": 69}
```

Also implement `generate` that uses the custom epoch for timestamps, and verify IDs are monotonically increasing:
```json
Request:  {"type": "generate", "msg_id": 1}
Response: {"type": "generate_ok", "in_reply_to": 1, "id": 1234567890}
```

## Concepts

- timestamp
- epoch
- time representation
- overflow planning

## Hints

- A custom epoch starting in 2024 gives you ~69 years before 41 bits overflow
- Unix epoch (1970) would waste 54 years of timestamp space
- Use time.time() * 1000 to get current timestamp in milliseconds
- Subtract the custom epoch to get relative milliseconds
- Check that the timestamp fits in 41 bits before composing the ID

## Test Cases

### 1. Generate produces a numeric ID

The generate_ok response should contain a numeric id field greater than 0.

Input:

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"generate","msg_id":2}}
```

Expected output:

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

### 2. Time info returns epoch and years remaining

Response should contain custom_epoch_ms=1704067200000, max_timestamp_ms=2199023255551, current_ms > 0, and years_remaining > 0.

Input:

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"time_info","msg_id":2}}
```

Expected output:

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

## Resources

- [Time, Clocks, and the Ordering of Events](https://lamport.azurewebsites.net/pubs/time-clocks.pdf): Lamport paper on logical clocks and event ordering in distributed systems

## Java Starter

The matching local starter file is:

```text
src/main/java/Main.java
```
