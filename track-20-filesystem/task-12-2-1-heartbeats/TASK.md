# Implement Chunk Server Heartbeats

Website: <https://builddistributedsystem.com/tracks/filesystem/tasks/task-12-2-1-heartbeats>

Track: 20. The Filesystem
Task order: 6
Short title: Heartbeats
Difficulty: intermediate
Subtrack: Fault Tolerance and Rebalancing

## Problem

Chunk server heartbeats are the master's only mechanism for tracking which servers are alive and which chunks they hold. Without heartbeats, the master cannot detect failures or maintain accurate chunk locations.

Heartbeat protocol:
1. Every 5 seconds, each chunk server sends a heartbeat to the master
2. The heartbeat contains: server ID, list of chunk handles, disk utilization, and health status
3. The master updates its in-memory chunk location map based on heartbeat data
4. If the master misses 3 consecutive heartbeats (15 seconds), it marks the server as **dead**
5. Dead servers trigger re-replication for any under-replicated chunks

```json
Request:  {"type": "heartbeat", "msg_id": 1, "server": "cs1", "chunks": ["ch_001", "ch_005", "ch_012"], "disk_usage_pct": 45}
Response: {"type": "heartbeat_ok", "in_reply_to": 1, "status": "alive", "chunks_to_delete": [], "chunks_to_replicate": []}

Request:  {"type": "server_status", "msg_id": 2}
Response: {"type": "server_status_ok", "in_reply_to": 2, "servers": [
    {"server": "cs1", "status": "alive", "chunks": 3, "last_heartbeat_ms_ago": 2000},
    {"server": "cs2", "status": "dead", "chunks": 0, "last_heartbeat_ms_ago": 30000}
]}
```

## Concepts

- heartbeat
- chunk server monitoring
- liveness detection
- chunk inventory

## Hints

- Every 5 seconds, each chunk server sends a heartbeat to the master
- The heartbeat includes the list of chunks the server currently holds
- If the master misses 3 consecutive heartbeats, it marks the server as dead
- The master uses heartbeats to maintain an up-to-date chunk location map
- This is how the master detects failures and triggers re-replication

## Test Cases

### 1. Heartbeat registers server as alive

Input:

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1","n2","n3"]}}
{"src":"n2","dest":"n1","body":{"type":"heartbeat","msg_id":2,"server":"n2","chunks":["ch_001","ch_002"],"disk_usage_pct":30}}
```

Expected output:

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
{"src": "n1", "dest": "n2", "body": {"type": "heartbeat_ok", "in_reply_to": 2, "status": "alive", "msg_id": 1}}
```

### 2. Server status shows all registered servers

server_status_ok should list all servers with status, chunk count, and last_heartbeat_ms_ago.

Input:

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"server_status","msg_id":2}}
```

Expected output:

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

## Resources

- [HDFS DataNode Heartbeats](https://hadoop.apache.org/docs/stable/hadoop-project-dist/hadoop-hdfs/HdfsDesign.html#Data_Replication): How HDFS DataNodes report to the NameNode via heartbeats

## Java Starter

The matching local starter file is:

```text
src/main/java/Main.java
```
