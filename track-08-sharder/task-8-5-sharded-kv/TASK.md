# Build Complete Sharded Key-Value Store

Website: <https://builddistributedsystem.com/tracks/sharder/tasks/task-8-5-sharded-kv>

Track: 8. The Sharder
Task order: 5
Short title: Sharded KV
Difficulty: advanced
Subtrack: Range Sharding

## Problem

Build a complete sharded KV store:

1. Client determines shard for key
2. Client routes to replica group owning shard
3. If wrong group, get new config and retry
4. Handle concurrent config changes
5. Ensure linearizability within each shard

This combines all previous components into a working system.

## Concept Notes

### Putting It Together

A sharded KV store has: (1) shard controller managing configuration, (2) multiple replica groups each handling some shards, (3) clients that route requests based on configuration.

### Client Retry

When a group receives a request for a shard it doesn't own, it returns an error. The client refreshes configuration and retries. This may happen multiple times during reconfiguration.

## Concepts

- sharded storage
- routing
- end-to-end

## Hints

- Route requests to correct shard
- Handle "wrong group" errors
- Retry on configuration changes

## Test Cases

### 1. Route to correct shard

Proxy routes request to correct group based on shard assignment.

Input:

```json
{"src":"client","dest":"proxy","body":{"type":"init","msg_id":1,"node_id":"proxy","node_ids":["proxy"]}}
{"src":"controller","dest":"proxy","body":{"type":"config","msg_id":2,"version":1,"shards":{"0":"g1","1":"g1","2":"g1","3":"g1","4":"g2","5":"g2"}}}
{"src":"c1","dest":"proxy","body":{"type":"get","msg_id":3,"key":"mykey"}}
```

Expected output:

```text
{"src":"proxy","dest":"client","body":{"type":"init_ok","in_reply_to":1,"msg_id":0}}
{"src":"proxy","dest":"controller","body":{"type":"config_ok","in_reply_to":2,"msg_id":1}}
{"src":"proxy","dest":"c1","body":{"type":"get_ok","in_reply_to":3,"msg_id":2,"key":"mykey"}}
```

## Java Starter

The matching local starter file is:

```text
src/main/java/Main.java
```
