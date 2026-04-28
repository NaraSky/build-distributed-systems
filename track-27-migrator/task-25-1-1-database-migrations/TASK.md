# Implement Database Schema Migrations

Website: <https://builddistributedsystem.com/tracks/migrator/tasks/task-25-1-1-database-migrations>

Track: 27. The Migrator
Task order: 1
Short title: Schema Migrations
Difficulty: intermediate
Subtrack: Schema Migrations

## Problem

Database migrations version-control schema changes. Each migration has an `up()` function that applies the change and a `down()` function that reverses it. A migrations table tracks which versions have been applied so you can apply pending ones or roll back the latest.

Implement a node that manages database schema migrations:

```json
// Apply all pending migrations in version order
{ "type": "migrate", "msg_id": 1 }
-> { "type": "migrations_applied", "in_reply_to": 1,
    "count": 2,
    "migrations": [
      {"version": 1, "name": "create_users", "status": "applied"},
      {"version": 2, "name": "add_posts_table", "status": "applied"}
    ]}

// Rollback the most recently applied migration
{ "type": "rollback", "msg_id": 2 }
-> { "type": "migration_rolled_back", "in_reply_to": 2,
    "version": 2, "name": "add_posts_table" }

// Show applied and pending migrations
{ "type": "status", "msg_id": 3 }
-> { "type": "migration_status", "in_reply_to": 3,
    "migrations": [
      {"version": 1, "name": "create_users", "applied": true},
      {"version": 2, "name": "add_posts_table", "applied": false}
    ]}
```

If a migration fails partway through, the transaction must be rolled back and the migration must NOT be recorded as applied.

## Concepts

- schema migrations
- migration versioning
- up/down migrations
- transaction safety
- migration status

## Hints

- Migrations are applied in version order; track which ones have run in a migrations table
- Each migration has an up() function (apply change) and down() function (undo change)
- Wrap each migration in a transaction; rollback the whole migration on any error
- migrate applies all pending migrations in order; rollback undoes the most recent one
- status lists all migrations with applied: true/false

## Test Cases

### 1. Apply pending migrations

Should apply both pending migrations in version order.

Input:

```json
{"src":"admin","dest":"migrations","body":{"type":"migrate","msg_id":1}}
```

Expected output:

```text
{"type": "migrations_applied", "in_reply_to": 1, "count": 2, "migrations": [{"version": 1, "name": "create_users", "status": "applied"}, {"version": 2, "name": "add_posts_table", "status": "applied"}]}
```

### 2. Rollback migration

Should rollback the most recently applied migration.

Input:

```json
{"src":"admin","dest":"migrations","body":{"type":"rollback","msg_id":1}}
```

Expected output:

```text
{"type": "migration_rolled_back", "in_reply_to": 1, "version": 2, "name": "add_posts_table"}
```

## Resources

- [Database Migrations](https://martinfowler.com/articles/evodb.html): Evolutionary database design: managing schema changes over time

## Java Starter

The matching local starter file is:

```text
src/main/java/Main.java
```
