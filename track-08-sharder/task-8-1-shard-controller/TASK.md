# Implement Shard Controller

Website: <https://builddistributedsystem.com/tracks/sharder/tasks/task-8-1-shard-controller>

Track: 8. The Sharder
Task order: 1
Short title: Shard Controller
Difficulty: advanced
Subtrack: Range Sharding

## Problem

Build a shard controller that manages shard assignment:

1. Maintain configuration: which replica group owns which shards
2. Support operations: Join (add group), Leave (remove group), Move (reassign shard)
3. Replicate controller state with Raft for fault tolerance
4. Distribute shards evenly across groups
5. Provide configuration query API

The controller is the source of truth for shard ownership.

## Concept Notes

### Sharding

When data exceeds one machine's capacity, split it across multiple machines (shards). Each shard handles a subset of keys. Sharding provides horizontal scalability.

### Shard Controller

The controller decides which shard goes where. It is typically a small Raft group for high availability. Configuration changes are versioned to coordinate migrations.

## Concepts

- sharding
- configuration
- coordination

## Hints

- Controller manages shard-to-group mapping
- Use Raft for controller replication
- Support join, leave, move operations

## Test Cases

### 1. Join new group

Config version incremented, group g1 added with servers [s1, s2], all 10 shards assigned to g1.

Input:

```json
{"src":"c0","dest":"controller","body":{"type":"init","msg_id":1,"node_id":"controller","node_ids":["controller"]}}
{"src":"c1","dest":"controller","body":{"type":"join","msg_id":2,"gid":"g1","servers":["s1","s2"]}}
{"src":"c1","dest":"controller","body":{"type":"query","msg_id":3,"num":-1}}
```

Expected output:

```text
{"src":"controller","dest":"c0","body":{"type":"init_ok","in_reply_to":1,"msg_id":0}}
{"src":"controller","dest":"c1","body":{"type":"join_ok","in_reply_to":2,"msg_id":1}}
{"src":"controller","dest":"c1","body":{"type":"query_ok","in_reply_to":3,"msg_id":2,"version":1,"groups":{"g1":["s1","s2"]},"shards":{"0":"g1","1":"g1","2":"g1","3":"g1","4":"g1","5":"g1","6":"g1","7":"g1","8":"g1","9":"g1"}}}
```

## Resources

- [MIT 6.824 Lab 4](https://pdos.csail.mit.edu/6.824/labs/lab-shard.html): Sharded KV store lab

## Java Starter

The matching local starter file is:

```text
src/main/java/Main.java
```
