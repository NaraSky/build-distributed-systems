# Handle Configuration Changes

Website: <https://builddistributedsystem.com/tracks/sharder/tasks/task-8-3-config-change>

Track: 8. The Sharder
Task order: 3
Short title: Config Change
Difficulty: advanced
Subtrack: Range Sharding

## Problem

Handle shard configuration changes:

1. Replica groups poll controller for configuration updates
2. Detect when shard assignment changes
3. Start migration: fetch shards assigned to this group
4. Complete migration before processing client requests
5. Acknowledge migration to source groups

Groups must coordinate to ensure exactly-once transfer.

## Concept Notes

### Configuration Versioning

Configurations are versioned. Groups must apply configurations in order. Skip a version and you might miss a shard assignment, leading to data loss.

### Migration Coordination

When shards move, both source and destination must coordinate. Source stops serving the shard, sends data, destination takes over. Use config version to track progress.

## Concepts

- configuration
- coordination
- atomic transition

## Hints

- Poll controller for new configs
- Process configs in order
- Coordinate between replicas

## Test Cases

### 1. Detect config change

Group detects version change (1→2) and applies new config.

Input:

```json
{"src":"c0","dest":"g1","body":{"type":"init","msg_id":1,"node_id":"g1","node_ids":["g1","g2"]}}
{"src":"c0","dest":"g1","body":{"type":"set_config","msg_id":2,"version":1,"shards":[0,1,2]}}
{"src":"controller","dest":"g1","body":{"type":"config_update","msg_id":3,"version":2,"shards":[0,1]}}
```

Expected output:

```text
{"src":"g1","dest":"c0","body":{"type":"init_ok","in_reply_to":1,"msg_id":0}}
{"src":"g1","dest":"c0","body":{"type":"set_config_ok","in_reply_to":2,"msg_id":1}}
{"src":"g1","dest":"controller","body":{"type":"config_update_ok","in_reply_to":3,"msg_id":2,"applied":true}}
```

## Java Starter

The matching local starter file is:

```text
src/main/java/Main.java
```
