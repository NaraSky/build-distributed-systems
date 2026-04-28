# Handle Client Retry and Deduplication

Website: <https://builddistributedsystem.com/tracks/store/tasks/task-7-4-client-dedup>

Track: 7. The Store
Task order: 4
Short title: Client Dedup
Difficulty: intermediate
Subtrack: Linearizable Key-Value Store

## Problem

Handle client retries without duplicate execution:

1. Client assigns sequence number to each request
2. Server tracks (client_id -> latest_seq, response)
3. If request seq <= latest_seq, return cached response
4. Otherwise, process and cache new response

This makes at-least-once delivery safe for non-idempotent operations.

## Concept Notes

### Exactly-Once Semantics

Network issues cause retries. Without deduplication, a PUT might execute twice. By tracking client sessions and sequence numbers, we can detect and skip duplicates.

### Session State

The deduplication table must survive leader changes. Store it in the replicated state machine. Periodically garbage collect old sessions.

## Concepts

- idempotency
- client sessions
- deduplication

## Hints

- Client assigns unique ID to each request
- Server tracks latest response per client
- Duplicate request returns cached response

## Test Cases

### 1. First request executes

Input:

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"write","msg_id":2,"key":"x","value":1,"client_id":"c1","seq":1}}
```

Expected output:

```text
{"src":"n1","dest":"c0","body":{"type":"init_ok","in_reply_to":1,"msg_id":0}}
{"src":"n1","dest":"c1","body":{"type":"write_ok","in_reply_to":2,"msg_id":1}}
```

## Java Starter

The matching local starter file is:

```text
src/main/java/Main.java
```
