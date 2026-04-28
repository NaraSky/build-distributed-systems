# Implement Client Migration Strategy

Website: <https://builddistributedsystem.com/tracks/migrator/tasks/task-25-2-5-client-migration>

Track: 27. The Migrator
Task order: 10
Short title: Client Migration
Difficulty: advanced
Subtrack: Protocol and API Evolution

## Problem

Migrating clients from API v1 to v2 should be gradual and safe. Canary deployments start with a small percentage of traffic; a/b testing routes specific users deterministically; tracking migration progress shows when it is safe to fully sunset v1.

Implement a node that manages client migration across API versions:

```json
// Canary at 10%: most traffic stays on v1
{ "type": "get_users", "msg_id": 1, "user_id": "user123" }
{ canary_percentage: 10 }
-> { "type": "users_response", "in_reply_to": 1,
    "version": "v1", "canary": false }

// 50/50 traffic split
{ "type": "get_users", "msg_id": 2 }
{ traffic_split: {"v1": 50, "v2": 50} }
-> { "type": "users_response", "in_reply_to": 2,
    "version": "<v1 or v2>" }

// Track how many clients have migrated
{ "type": "get_migration_stats", "msg_id": 3 }
-> { "type": "migration_stats", "in_reply_to": 3,
    "total_clients": 1000,
    "version_percentages": {"v1": 20, "v2": 80},
    "migration_complete": false }

// Gradual rollout with health checks between steps
{ "type": "gradual_rollout", "msg_id": 4,
  "steps": [{"percentage":10,"duration_minutes":60},
              {"percentage":50,"duration_minutes":240}] }
-> { "type": "rollout_complete", "in_reply_to": 4,
    "final_percentage": 50, "health_checks_passed": true }
```

## Concepts

- canary deployment
- traffic splitting
- migration tracking
- gradual rollout
- health checks

## Hints

- Canary: route 10% of traffic to v2 (hash user_id % 100 < 10); rest to v1
- Traffic split: use a random number per request and route by bucket percentage
- migration stats: count requests by version over time; migration_complete when v1 usage drops to 0
- Gradual rollout: each step increases the v2 percentage after checking health metrics
- health_checks_passed: true means no error rate increase was detected during rollout

## Test Cases

### 1. Canary deployment routing

At 10% canary, most users (including user123) should stay on v1.

Input:

```json
{"src":"client","dest":"api","body":{"type":"get_users","msg_id":1,"user_id":"user123"},"canary_percentage":10}
```

Expected output:

```text
{"type": "users_response", "in_reply_to": 1, "version": "v1", "canary": false}
```

### 2. Traffic splitting

Should split traffic 50/50 and return either v1 or v2.

Input:

```json
{"src":"client","dest":"api","body":{"type":"get_users","msg_id":1},"traffic_split":{"v1":50,"v2":50}}
```

Expected output:

```text
{"type": "users_response", "in_reply_to": 1, "version": ".*"}
```

## Resources

- [Canary Release](https://martinfowler.com/bliki/CanaryRelease.html): Gradual traffic shifting to safely roll out API changes
- [Blue-Green Deployment](https://martinfowler.com/bliki/BlueGreenDeployment.html): Martin Fowler on Blue-Green Deployment

## Java Starter

The matching local starter file is:

```text
src/main/java/Main.java
```
