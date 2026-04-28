# Add Follower Reads with Bounded Staleness

Website: <https://builddistributedsystem.com/tracks/store/tasks/task-8-2-3-follower-reads>

Track: 7. The Store
Task order: 8
Short title: Follower Reads
Difficulty: advanced
Subtrack: Read Optimization

## Problem

Implement follower reads with bounded staleness. Clients can opt to read from any follower if they accept data up to T seconds stale. This scales read throughput linearly with cluster size.

```json
Request:  {"type": "follower_read", "msg_id": 1, "key": "x", "max_staleness_ms": 5000}
Response: {"type": "follower_read_ok", "in_reply_to": 1, "value": "42", "actual_staleness_ms": 200, "served_by": "n2", "linearizable": false}

Request:  {"type": "follower_read", "msg_id": 2, "key": "x", "max_staleness_ms": 0}
Response: {"type": "follower_read_ok", "in_reply_to": 2, "value": "42", "served_by": "n1", "linearizable": true, "reason": "redirected_to_leader"}
```

## Concepts

- follower reads
- bounded staleness
- read scalability
- consistency tradeoff

## Hints

- Clients opt in to reading from followers if they accept data up to T seconds stale
- Followers track their applied index; reads are served if the data is fresh enough
- This distributes read load across all replicas, not just the leader
- The staleness bound is configurable per-request
- Compare latency: follower reads avoid the leader bottleneck

## Test Cases

### 1. Follower read within staleness bound

follower_read_ok with actual_staleness_ms <= 5000. linearizable: false.

Input:

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1","n2","n3"]}}
{"src":"c1","dest":"n1","body":{"type":"follower_read","msg_id":2,"key":"x","max_staleness_ms":5000}}
```

Expected output:

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

### 2. Zero staleness redirects to leader

With max_staleness_ms: 0, read should be served by leader. linearizable: true.

Input:

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1","n2","n3"]}}
{"src":"c1","dest":"n1","body":{"type":"follower_read","msg_id":2,"key":"x","max_staleness_ms":0}}
```

Expected output:

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

## Resources

- [CockroachDB Follower Reads](https://www.cockroachlabs.com/docs/stable/follower-reads.html): How CockroachDB implements follower reads for geo-distributed systems

## Java Starter

The matching local starter file is:

```text
src/main/java/Main.java
```
