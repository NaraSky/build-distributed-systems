# Implement Lease-Based Reads

Website: <https://builddistributedsystem.com/tracks/store/tasks/task-8-2-2-lease-reads>

Track: 7. The Store
Task order: 7
Short title: Lease Reads
Difficulty: advanced
Subtrack: Read Optimization

## Problem

Implement lease-based reads: the leader uses its active lease to serve reads without network round trips. Document the clock assumption required.

```json
Request:  {"type": "lease_read", "msg_id": 1, "key": "x"}
Response: {"type": "lease_read_ok", "in_reply_to": 1, "value": "42", "lease_valid": true, "network_round_trips": 0}

Request:  {"type": "lease_read_config", "msg_id": 2, "lease_duration_ms": 3000, "election_timeout_ms": 5000, "max_clock_skew_ms": 500}
Response: {"type": "lease_read_config_ok", "in_reply_to": 2, "safe": true, "effective_lease_ms": 2500, "reason": "lease - clock_skew < election_timeout"}
```

## Concepts

- lease reads
- clock assumption
- zero network round trips
- stale read risk

## Hints

- The leader uses its lease to serve reads without any network round trips
- During the lease, the leader is guaranteed to still be leader
- Lease duration must be shorter than election timeout to prevent stale reads
- Assumption: bounded clock skew between nodes
- If clocks drift too much, a stale leader may serve reads after a new leader is elected

## Test Cases

### 1. Lease read with zero round trips

lease_read_ok should show network_round_trips: 0 and lease_valid: true.

Input:

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1","n2","n3"]}}
{"src":"c1","dest":"n1","body":{"type":"lease_read","msg_id":2,"key":"x"}}
```

Expected output:

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

### 2. Safe lease configuration

Input:

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"lease_read_config","msg_id":2,"lease_duration_ms":3000,"election_timeout_ms":5000,"max_clock_skew_ms":500}}
```

Expected output:

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
{"src": "n1", "dest": "c1", "body": {"type": "lease_read_config_ok", "in_reply_to": 2, "safe": true, "effective_lease_ms": 2500, "msg_id": 1}}
```

## Resources

- [CockroachDB - Follower Reads and Lease Reads](https://www.cockroachlabs.com/docs/stable/architecture/reads-and-writes-overview.html): How CockroachDB implements lease-based reads for low latency

## Java Starter

The matching local starter file is:

```text
src/main/java/Main.java
```
