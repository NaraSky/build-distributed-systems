# Implement Migration Rollback Strategies

Website: <https://builddistributedsystem.com/tracks/migrator/tasks/task-25-1-5-rollback-strategies>

Track: 27. The Migrator
Task order: 5
Short title: Rollback Strategies
Difficulty: advanced
Subtrack: Schema Migrations

## Problem

When a migration goes wrong in production, you need a rollback plan. Different situations call for different strategies: instant feature flag disables for behavioural changes, blue-green traffic switch for deployment issues, migration down() functions for schema changes, and database restore for catastrophic data corruption.

Implement a node that supports four rollback strategies:

```json
// 1. Migration rollback: run down() for version 3
{ "type": "rollback", "msg_id": 1, "version": 3 }
-> { "type": "rollback_complete", "in_reply_to": 1,
    "rolled_back_from": 3, "rolled_back_to": 2,
    "duration_seconds": 5 }

// 2. Feature flag rollback: disable instantly
{ "type": "disable_feature", "msg_id": 2,
  "feature": "new_checkout" }
-> { "type": "feature_disabled", "in_reply_to": 2,
    "feature": "new_checkout", "rolled_back_instant": true }

// 3. Blue-green: switch traffic back to the previous environment
{ "type": "switch_traffic", "msg_id": 3,
  "from": "green", "to": "blue" }
-> { "type": "traffic_switched", "in_reply_to": 3,
    "current_environment": "blue", "downtime_seconds": 0 }

// 4. Restore from backup (last resort)
{ "type": "restore", "msg_id": 4,
  "backup": "users_backup_20240115" }
-> { "type": "restore_complete", "in_reply_to": 4,
    "restored_rows": 100000, "duration_seconds": 60 }
```

## Concepts

- migration rollback
- feature flags
- blue-green deployment
- database restore
- instant rollback

## Hints

- Migration rollback: run the down() function for the target version
- Feature flag rollback: disable the flag instantly without a deployment
- Blue-green: two identical environments; switch traffic from green back to blue in seconds
- Database restore is the last resort: restore from a pre-migration backup
- Rollback strategies range from instant (feature flag) to slow (database restore)

## Test Cases

### 1. Rollback migration

Should run down() for version 3 and leave database at version 2.

Input:

```json
{"src":"admin","dest":"migrations","body":{"type":"rollback","msg_id":1,"version":3}}
```

Expected output:

```text
{"type": "rollback_complete", "in_reply_to": 1, "rolled_back_from": 3, "rolled_back_to": 2, "duration_seconds": 5}
```

### 2. Feature flag rollback

Feature flag should be disabled instantly without redeployment.

Input:

```json
{"src":"admin","dest":"features","body":{"type":"disable_feature","msg_id":1,"feature":"new_checkout"}}
```

Expected output:

```text
{"type": "feature_disabled", "in_reply_to": 1, "feature": "new_checkout", "rolled_back_instant": true}
```

## Resources

- [Blue-Green Deployment](https://martinfowler.com/bliki/BlueGreenDeployment.html): Martin Fowler's blue-green deployment pattern for zero-downtime rollback

## Java Starter

The matching local starter file is:

```text
src/main/java/Main.java
```
