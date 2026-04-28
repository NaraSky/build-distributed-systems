# Implement Chunk Server Load Balancing

Website: <https://builddistributedsystem.com/tracks/filesystem/tasks/task-12-2-3-load-balancing>

Track: 20. The Filesystem
Task order: 8
Short title: Load Balancing
Difficulty: advanced
Subtrack: Fault Tolerance and Rebalancing

## Problem

Over time, chunk distribution becomes uneven: new servers start empty, old servers fill up, and some receive more writes. Load balancing moves chunks to equalize utilization.

Rebalancing algorithm:
1. Periodically compute the average disk utilization across all servers
2. If any server exceeds average + 20%, it is overloaded; if below average - 20%, it is underloaded
3. For each overloaded server, select chunks to migrate to underloaded servers
4. Migration: copy chunk from source to target, update master metadata, delete from source
5. Run as a background process with rate limiting to avoid saturating the network

```json
Request:  {"type": "rebalance_check", "msg_id": 1}
Response: {"type": "rebalance_check_ok", "in_reply_to": 1, "average_utilization_pct": 50, "overloaded": [{"server": "cs1", "utilization_pct": 78}], "underloaded": [{"server": "cs4", "utilization_pct": 15}]}

Request:  {"type": "rebalance_execute", "msg_id": 2, "moves": [{"chunk": "ch_010", "from": "cs1", "to": "cs4"}]}
Response: {"type": "rebalance_execute_ok", "in_reply_to": 2, "moved": 1, "bytes_transferred": 67108864}
```

## Concepts

- load balancing
- chunk migration
- disk utilization
- rebalancing threshold

## Hints

- Monitor each server disk usage; if imbalance exceeds 20%, trigger rebalancing
- Move chunks from overloaded servers to underloaded ones
- Rebalancing is a background operation — do not disrupt active reads/writes
- After moving a chunk, update the master metadata and notify affected servers
- Prefer moving chunks that are infrequently accessed to minimize disruption

## Test Cases

### 1. Check identifies overloaded and underloaded servers

rebalance_check_ok should show average_utilization_pct, overloaded, and underloaded arrays.

Input:

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"rebalance_check","msg_id":2}}
```

Expected output:

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

### 2. Execute rebalance moves chunks

rebalance_execute_ok should show moved: 1 and bytes_transferred > 0.

Input:

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"rebalance_execute","msg_id":2,"moves":[{"chunk":"ch_010","from":"cs1","to":"cs4"}]}}
```

Expected output:

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

## Resources

- [HDFS Balancer](https://hadoop.apache.org/docs/stable/hadoop-project-dist/hadoop-hdfs/HdfsUserGuide.html#Balancer): HDFS balancer tool for redistributing blocks across DataNodes

## Java Starter

The matching local starter file is:

```text
src/main/java/Main.java
```
