# Build a Time Oracle Service with Failover

Website: <https://builddistributedsystem.com/tracks/timekeeper/tasks/task-4-4-4-time-oracle>

Track: 16. The Timekeeper
Task order: 19
Short title: Time Oracle
Difficulty: advanced
Subtrack: Hybrid Logical Clocks

## Problem

Build a centralized time oracle service that nodes query for globally consistent HLC timestamps. This avoids the problem of unbounded clock skew between nodes.

Architecture:
- **Primary oracle**: maintains an HLC, issues timestamps on request
- **Backup oracle**: monitors the primary, takes over on failure
- **Nodes**: query the oracle instead of using local clocks

Failure mode: if primary crashes after issuing timestamp T but before the backup knows, the backup must start with T + safety_margin to avoid issuing duplicate timestamps.

Implement handlers:

```json
Request:  {"type": "oracle_get_time", "msg_id": 1}
Response: {"type": "oracle_get_time_ok", "in_reply_to": 1, "pt": 1000, "c": 0, "oracle": "primary"}

Request:  {"type": "oracle_fail_primary", "msg_id": 2}
Response: {"type": "oracle_fail_primary_ok", "in_reply_to": 2, "new_oracle": "backup", "safety_margin_ms": 100}

Request:  {"type": "oracle_get_time", "msg_id": 3}
Response: {"type": "oracle_get_time_ok", "in_reply_to": 3, "pt": 1100, "c": 0, "oracle": "backup"}

Request:  {"type": "oracle_status", "msg_id": 4}
Response: {"type": "oracle_status_ok", "in_reply_to": 4, "primary_alive": false, "active_oracle": "backup", "timestamps_issued": 2}
```

## Concepts

- time oracle
- centralized clock
- failover
- backup oracle
- single point of failure

## Hints

- The oracle maintains an HLC and issues globally consistent timestamps
- Nodes query the oracle instead of using their own clocks for ordering
- If the primary oracle crashes, the backup takes over with a higher counter
- The backup oracle must start with a timestamp guaranteed to be higher than any issued by the primary
- Use a lease mechanism: the oracle is valid only while its lease is active

## Test Cases

### 1. Primary oracle issues timestamps

Two oracle_get_time_ok responses from primary oracle. Second timestamp must be strictly greater than first.

Input:

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"oracle_get_time","msg_id":2}}
{"src":"c1","dest":"n1","body":{"type":"oracle_get_time","msg_id":3}}
```

Expected output:

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

### 2. Failover to backup oracle

After oracle_fail_primary, oracle_get_time_ok should show oracle: backup and pt >= last_primary_pt + safety_margin.

Input:

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"oracle_get_time","msg_id":2}}
{"src":"c1","dest":"n1","body":{"type":"oracle_fail_primary","msg_id":3}}
{"src":"c1","dest":"n1","body":{"type":"oracle_get_time","msg_id":4}}
```

Expected output:

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

## Resources

- [TiDB - Timestamp Oracle Design](https://docs.pingcap.com/tidb/stable/tidb-architecture): How TiDB uses a centralized timestamp oracle (TSO) for transaction ordering

## Java Starter

The matching local starter file is:

```text
src/main/java/Main.java
```
