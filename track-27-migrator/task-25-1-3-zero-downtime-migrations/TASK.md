# Implement Zero-Downtime Database Migrations

Website: <https://builddistributedsystem.com/tracks/migrator/tasks/task-25-1-3-zero-downtime-migrations>

Track: 27. The Migrator
Task order: 3
Short title: Zero-Downtime Migrations
Difficulty: advanced
Subtrack: Schema Migrations

## Problem

A naive `ALTER TABLE ADD COLUMN NOT NULL DEFAULT 'x'` rewrites the entire table and holds an exclusive lock, blocking all reads and writes. Zero-downtime migrations use PostgreSQL features to make schema changes without taking the table offline.

Implement a node that performs lock-safe schema changes:

```json
// Create index without locking the table
{ "type": "create_index", "msg_id": 1,
  "table": "users", "column": "email", "concurrently": true }
-> { "type": "index_created", "in_reply_to": 1,
    "index": "idx_email", "duration_seconds": 120,
    "table_locked": false }

// Add NOT NULL column with default — no table rewrite needed
{ "type": "add_column", "msg_id": 2,
  "table": "users", "column": "status",
  "default": "active", "nullable": false }
-> { "type": "column_added", "in_reply_to": 2,
    "duration_seconds": 0.1, "table_rewritten": false }

// Migrate data in batches to avoid long locks
{ "type": "migrate_data", "msg_id": 3,
  "table": "users", "batch_size": 1000, "total_rows": 10000 }
-> { "type": "data_migrated", "in_reply_to": 3,
    "total_rows": 10000, "batches": 10, "table_locked": false }
```

Lock-aware migration: if a lock cannot be acquired within `max_lock_duration_ms`, abort and roll back rather than blocking the application.

## Concepts

- concurrent index
- lock-free migrations
- batch data migration
- lock-aware migration

## Hints

- CREATE INDEX CONCURRENTLY builds the index without holding an exclusive table lock
- Adding a column with a server-side default does not rewrite the table in PostgreSQL 11+
- Batch data migration: process rows in chunks (e.g. WHERE id BETWEEN x AND x+1000); sleep between batches
- Lock-aware migration: set a short lock timeout; abort if a lock cannot be acquired quickly
- table_locked: false confirms the operation did not block read/write access

## Test Cases

### 1. Create index concurrently

Concurrent index creation should not lock the table.

Input:

```json
{"src":"admin","dest":"migrations","body":{"type":"create_index","msg_id":1,"table":"users","column":"email","concurrently":true}}
```

Expected output:

```text
{"type": "index_created", "in_reply_to": 1, "index": "idx_email", "duration_seconds": 120, "table_locked": false}
```

### 2. Add column without table rewrite

Adding column with server-side default should not rewrite the table.

Input:

```json
{"src":"admin","dest":"migrations","body":{"type":"add_column","msg_id":1,"table":"users","column":"status","default":"active","nullable":false}}
```

Expected output:

```text
{"type": "column_added", "in_reply_to": 1, "duration_seconds": 0.1, "table_rewritten": false}
```

## Resources

- [Zero-Downtime Migrations](https://www.citusdata.com/blog/2018/02/22/seven-tips-for-better-postgresql-migrations/): Seven tips for safer PostgreSQL migrations in production
- [pt-online-schema-change](https://www.percona.com/doc/percona-toolkit/LATEST/pt-online-schema-change.html): Percona pt-online-schema-change documentation

## Java Starter

The matching local starter file is:

```text
src/main/java/Main.java
```
