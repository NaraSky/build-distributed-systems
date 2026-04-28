# 实现 Chunk Server Heartbeats

英文标题：Implement Chunk Server Heartbeats
网页：<https://builddistributedsystem.com/tracks/filesystem/tasks/task-12-2-1-heartbeats>

课程：20. 文件系统：分布式文件存储
任务序号：6
短标题：Heartbeats
难度：intermediate
子主题：Fault Tolerance和Rebalancing

## 中文导读

本题要求你完成 `实现 Chunk Server Heartbeats`。

重点关注：`heartbeat`、`chunk server monitoring`、`liveness detection`、`chunk inventory`。

建议先按提示逐步实现：Every 5 seconds, each chunk 服务端 sends a 心跳 to the master。

协议字段、消息类型、输入输出格式请以本文件中的代码块和测试用例为准。

## 题目说明

Chunk 服务端 heartbeats are the master's only mechanism用于tracking which servers are alive和which chunks they hold. Without heartbeats, the master cannot detect failures or maintain accurate chunk locations.

心跳 protocol:
1. Every 5 seconds, each chunk 服务端 sends a 心跳 to the master
2. The 心跳 contains: 服务端 ID, list of chunk handles, disk utilization,和health status
3. The master updates its in-memory chunk location map based on 心跳 data
4. If the master misses 3 consecutive heartbeats (15 seconds), it marks the 服务端 as **dead**
5. Dead servers trigger re-复制用于any under-replicated chunks

```JSON
请求:  {"type": "心跳", "msg_id": 1, "服务端": "cs1", "chunks": ["ch_001", "ch_005", "ch_012"], "disk_usage_pct": 45}
响应: {"type": "heartbeat_ok", "in_reply_to": 1, "status": "alive", "chunks_to_delete": [], "chunks_to_replicate": []}

请求:  {"type": "server_status", "msg_id": 2}
响应: {"type": "server_status_ok", "in_reply_to": 2, "servers": [
    {"服务端": "cs1", "status": "alive", "chunks": 3, "last_heartbeat_ms_ago": 2000},
    {"服务端": "cs2", "status": "dead", "chunks": 0, "last_heartbeat_ms_ago": 30000}
]}
```

## 涉及概念

- `heartbeat`
- `chunk server monitoring`
- `liveness detection`
- `chunk inventory`

## 实现提示

- Every 5 seconds, each chunk 服务端 sends a 心跳 to the master
- The 心跳 includes the list of chunks the 服务端 currently holds
- If the master misses 3 consecutive heartbeats, it marks the 服务端 as dead
- The master uses heartbeats to maintain an up-to-date chunk location map
- This is how the master detects failures和triggers re-复制

## 测试用例

### 1. Heartbeat registers server as alive

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1","n2","n3"]}}
{"src":"n2","dest":"n1","body":{"type":"heartbeat","msg_id":2,"server":"n2","chunks":["ch_001","ch_002"],"disk_usage_pct":30}}
```

期望输出：

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
{"src": "n1", "dest": "n2", "body": {"type": "heartbeat_ok", "in_reply_to": 2, "status": "alive", "msg_id": 1}}
```

### 2. Server status shows all registered servers

server_status_ok should list all servers，包含status, chunk count,和last_heartbeat_ms_ago.

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"server_status","msg_id":2}}
```

期望输出：

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

## 参考资料

- [HDFS DataNode Heartbeats](https://hadoop.apache.org/docs/stable/hadoop-project-dist/hadoop-hdfs/HdfsDesign.html#Data_Replication)：How HDFS DataNodes report to the NameNode via heartbeats

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
