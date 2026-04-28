# Implement Backward-Compatible Schema Migrations

Website: <https://builddistributedsystem.com/tracks/migrator/tasks/task-25-1-2-backward-compatible-migrations>

Track: 27. The Migrator
Task order: 2
Short title: Backward-Compatible Migrations
Difficulty: advanced
Subtrack: Schema Migrations

## Problem

A simple "rename column" migration breaks running app instances that still reference the old name. The **expand-contract pattern** avoids this: first add the new column (both columns exist simultaneously), then backfill the data, then remove the old column once all app instances are updated.

Implement a node that manages backward-compatible schema changes in three phases:

```json
// Phase 1 — EXPAND: add new column (nullable, old column still present)
{ "type": "migrate", "msg_id": 1,
  "phase": "expand", "table": "users", "add_column": "full_name" }
-> { "type": "migration_applied", "in_reply_to": 1,
    "version": 1, "name": "add_full_name_column",
    "schema": "users (name, full_name NULL)",
    "backward_compatible": true }

// Phase 2 — DATA MIGRATION: copy name -> full_name for existing rows
{ "type": "migrate", "msg_id": 2,
  "phase": "migrate_data", "from": "name", "to": "full_name" }
-> { "type": "data_migrated", "in_reply_to": 2,
    "version": 2, "rows_migrated": 1000 }

// Phase 3 — CONTRACT: remove old column (only after all app instances updated)
{ "type": "migrate", "msg_id": 3,
  "phase": "contract", "table": "users", "remove_column": "name" }
-> { "type": "migration_applied", "in_reply_to": 3,
    "version": 3, "name": "remove_name_column",
    "schema": "users (full_name)" }
```

## Concepts

- expand-contract pattern
- backward compatibility
- rolling deployment
- column rename
- zero downtime

## Hints

- Expand: add the new column as nullable alongside the old one (both exist)
- Migrate data: copy/transform values from old column to new column
- Contract: remove the old column only after all app instances use the new column
- Never rename or drop a column in a single migration with zero downtime
- Rolling deployment: deploy new app version to instances one by one, health-checking each

## Test Cases

### 1. Expand phase (add new column)

Should add full_name nullable while keeping name; backward_compatible=true.

Input:

```json
{"src":"admin","dest":"migrations","body":{"type":"migrate","msg_id":1,"phase":"expand","table":"users","add_column":"full_name"}}
```

Expected output:

```text
{"type": "migration_applied", "in_reply_to": 1, "version": 1, "name": "add_full_name_column", "schema": "users (name, full_name NULL)", "backward_compatible": true}
```

### 2. Data migration (backfill)

Should copy name values to full_name and report rows migrated.

Input:

```json
{"src":"admin","dest":"migrations","body":{"type":"migrate","msg_id":1,"phase":"migrate_data","from":"name","to":"full_name"}}
```

Expected output:

```text
{"type": "data_migrated", "in_reply_to": 1, "version": 2, "rows_migrated": 1000}
```

## Resources

- [Expand-Contract Pattern](https://martinfowler.com/bliki/ParallelChange.html): Martin Fowler's parallel change pattern for zero-downtime migrations

## Java Starter

The matching local starter file is:

```text
src/main/java/Main.java
```
