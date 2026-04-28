# Implement Master Failover with Shadow Master

Website: <https://builddistributedsystem.com/tracks/filesystem/tasks/task-12-2-4-master-failover>

Track: 20. The Filesystem
Task order: 9
Short title: Master Failover
Difficulty: advanced
Subtrack: Fault Tolerance and Rebalancing

## Problem

The master is a single point of failure. A shadow master mitigates this by continuously replaying the primary's WAL, staying nearly synchronized.

Failover process:
1. **Normal operation**: primary master handles all requests; shadow replays WAL entries from a shared storage
2. **Failure detection**: if the primary misses heartbeats for 10 seconds, the shadow initiates takeover
3. **WAL catchup**: shadow replays any remaining WAL entries not yet processed
4. **Promote**: shadow becomes the new primary, starts accepting requests
5. **Redirect**: chunk servers and clients are notified to use the new master

```json
Request:  {"type": "shadow_status", "msg_id": 1}
Response: {"type": "shadow_status_ok", "in_reply_to": 1, "primary": "master1", "shadow": "master2", "wal_lag_entries": 5, "wal_lag_ms": 200}

Request:  {"type": "trigger_failover", "msg_id": 2, "failed_master": "master1"}
Response: {"type": "trigger_failover_ok", "in_reply_to": 2, "new_primary": "master2", "wal_entries_replayed": 5, "failover_time_ms": 450}
```

## Concepts

- master failover
- shadow master
- WAL replay
- hot standby
- failover time

## Hints

- A shadow master replays the primary WAL periodically to stay nearly up-to-date
- On primary failure, the shadow takes over with minimal data loss (only recent WAL entries)
- The shadow cannot serve queries while the primary is alive — it is a hot standby
- Failover time = time to detect failure + time to replay remaining WAL entries
- After failover, chunk servers redirect heartbeats to the new master

## Test Cases

### 1. Shadow status shows WAL lag

shadow_status_ok should show primary, shadow, and wal_lag_entries.

Input:

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1","n2"]}}
{"src":"c1","dest":"n1","body":{"type":"shadow_status","msg_id":2}}
```

Expected output:

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

### 2. Failover promotes shadow

trigger_failover_ok should have new_primary different from failed_master.

Input:

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1","n2"]}}
{"src":"c1","dest":"n1","body":{"type":"trigger_failover","msg_id":2,"failed_master":"n1"}}
```

Expected output:

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

## Resources

- [GFS Master Replication](https://research.google/pubs/pub51/): GFS paper section on master replication and shadow masters

## Java Starter

The matching local starter file is:

```text
src/main/java/Main.java
```
