# Implement Data Migration

Website: <https://builddistributedsystem.com/tracks/sharder/tasks/task-8-4-data-migration>

Track: 8. The Sharder
Task order: 4
Short title: Data Migration
Difficulty: advanced
Subtrack: Range Sharding

## Problem

Implement data migration between replica groups:

1. Source group: stop accepting writes for migrating shard
2. Create snapshot of shard data + client sessions
3. Send to destination group
4. Destination: install snapshot, start serving shard
5. Source: delete shard data after confirmation

Handle failures: retry, idempotency, rollback.

## Concept Notes

### Data Migration

Moving shards requires moving data. This must be atomic per shard and consistent. During migration, the shard may be unavailable or served by source (stale reads OK) until transfer completes.

### Client Session Transfer

Don't forget client deduplication state. If sessions aren't migrated, clients may see duplicate execution on retry. Transfer the client session table with the shard data.

## Concepts

- migration
- data transfer
- consistency

## Hints

- Stop serving shard during migration
- Transfer all key-value pairs
- Include client session state

## Test Cases

### 1. Prepare shard for migration

Shard 3 locked, snapshot created containing data {x:1,y:2}.

Input:

```json
{"src":"c0","dest":"g1","body":{"type":"init","msg_id":1,"node_id":"g1","node_ids":["g1","g2"]}}
{"src":"c0","dest":"g1","body":{"type":"seed_shard","msg_id":2,"shard":3,"data":{"x":1,"y":2}}}
{"src":"c0","dest":"g1","body":{"type":"prepare_migration","msg_id":3,"shard":3,"target_gid":"g2"}}
```

Expected output:

```text
{"src":"g1","dest":"c0","body":{"type":"init_ok","in_reply_to":1,"msg_id":0}}
{"src":"g1","dest":"c0","body":{"type":"seed_shard_ok","in_reply_to":2,"msg_id":1}}
{"src":"g1","dest":"c0","body":{"type":"prepare_migration_ok","in_reply_to":3,"msg_id":2,"shard":3,"target_gid":"g2","snapshot":{"data":{"x":1,"y":2}}}}
```

## Java Starter

The matching local starter file is:

```text
src/main/java/Main.java
```
