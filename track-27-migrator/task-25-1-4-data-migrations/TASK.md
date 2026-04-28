# Implement Data Migrations

Website: <https://builddistributedsystem.com/tracks/migrator/tasks/task-25-1-4-data-migrations>

Track: 27. The Migrator
Task order: 4
Short title: Data Migrations
Difficulty: advanced
Subtrack: Schema Migrations

## Problem

Data migrations transform existing data to match a new schema or business rule. Unlike schema migrations, they touch every row. Running them during peak traffic causes lock contention — so they must run in small batches, be idempotent (safe to re-run), and be validated before the old schema is removed.

Implement a node that manages data migrations:

```json
// Backfill full_name column for 10,000 existing users in batches
{ "type": "backfill", "msg_id": 1,
  "table": "users", "column": "full_name",
  "batch_size": 1000, "total_rows": 10000 }
-> { "type": "backfill_complete", "in_reply_to": 1,
    "total_processed": 10000, "total_updated": 9500,
    "duration_seconds": 60 }

// Validate the migrated data meets constraints
{ "type": "validate", "msg_id": 2,
  "table": "users",
  "validations": ["no_nulls", "email_format"] }
-> { "type": "validation_results", "in_reply_to": 2,
    "results": [
      {"name": "no_nulls", "passed": true, "failed_rows": 0},
      {"name": "email_format", "passed": true, "failed_rows": 0}
    ]}

// Running migration 3 times produces the same final state
{ "type": "migrate", "msg_id": 3,
  "idempotent": true, "table": "users", "runs": 3 }
-> { "type": "migration_complete", "in_reply_to": 3,
    "rows_updated": 100, "final_state": "unchanged" }
```

## Concepts

- data backfill
- batch processing
- idempotent migration
- data validation
- rollback on failure

## Hints

- Backfill in batches: process rows WHERE id > last_processed_id LIMIT batch_size
- Track total_processed and total_updated separately (some rows may already be correct)
- Idempotent: running the migration twice should produce the same result, not double-update
- Validate after migration: check constraints like no_nulls and format rules
- Rollback on validation failure: restore from backup if post-migration checks fail

## Test Cases

### 1. Backfill data in batches

Should backfill 10000 rows in batches and report processed vs updated counts.

Input:

```json
{"src":"admin","dest":"migrations","body":{"type":"backfill","msg_id":1,"table":"users","column":"full_name","batch_size":1000,"total_rows":10000}}
```

Expected output:

```text
{"type": "backfill_complete", "in_reply_to": 1, "total_processed": 10000, "total_updated": 9500, "duration_seconds": 60}
```

### 2. Validate migrated data

Both validation rules should pass with zero failed rows.

Input:

```json
{"src":"admin","dest":"migrations","body":{"type":"validate","msg_id":1,"table":"users","validations":["no_nulls","email_format"]}}
```

Expected output:

```text
{"type": "validation_results", "in_reply_to": 1, "results": [{"name": "no_nulls", "passed": true, "failed_rows": 0}, {"name": "email_format", "passed": true, "failed_rows": 0}]}
```

## Resources

- [Database Migrations](https://martinfowler.com/articles/evodb.html): Evolutionary database design: schema and data migrations

## Java Starter

The matching local starter file is:

```text
src/main/java/Main.java
```
