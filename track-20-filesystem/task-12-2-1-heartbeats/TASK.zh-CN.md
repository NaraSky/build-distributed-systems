# 实现块服务器的心跳机制

英文标题：Implement Chunk Server Heartbeats
网页：<https://builddistributedsystem.com/tracks/filesystem/tasks/task-12-2-1-heartbeats>

课程：20. 文件系统：容错与再平衡
任务序号：6
短标题：Heartbeats
难度：进阶
子主题：Fault Tolerance and Rebalancing

## 中文导读

这道题要求你实现块服务器的心跳（Heartbeat）协议。心跳就像是块服务器定期向主节点"报到"：告诉主节点自己还活着、手里有哪些数据块。如果主节点长时间没收到某台服务器的心跳，就会判定它已经宕机，从而触发数据块的重新复制。

## 题目说明

块服务器心跳是主节点追踪哪些服务器存活、它们持有哪些数据块的唯一手段。没有心跳，主节点就无法发现故障，也无法维护准确的数据块位置信息。

心跳协议的工作方式：
1. 每 5 秒，每台块服务器向主节点发送一次心跳
2. 心跳包含：服务器 ID、持有的数据块句柄列表、磁盘使用率和健康状态
3. 主节点根据心跳数据更新内存中的数据块位置映射表
4. 如果主节点连续 3 次（15 秒）未收到某台服务器的心跳，就将其标记为**已宕机**
5. 宕机服务器上的数据块如果副本数不足，就会触发重新复制

```json
Request:  {"type": "heartbeat", "msg_id": 1, "server": "cs1", "chunks": ["ch_001", "ch_005", "ch_012"], "disk_usage_pct": 45}
Response: {"type": "heartbeat_ok", "in_reply_to": 1, "status": "alive", "chunks_to_delete": [], "chunks_to_replicate": []}

Request:  {"type": "server_status", "msg_id": 2}
Response: {"type": "server_status_ok", "in_reply_to": 2, "servers": [
    {"server": "cs1", "status": "alive", "chunks": 3, "last_heartbeat_ms_ago": 2000},
    {"server": "cs2", "status": "dead", "chunks": 0, "last_heartbeat_ms_ago": 30000}
]}
```

## 涉及概念

- `heartbeat`
- `chunk server monitoring`
- `liveness detection`
- `chunk inventory`

## 实现提示

- 每 5 秒，每台块服务器向主节点发送一次心跳
- 心跳中包含该服务器当前持有的数据块列表
- 如果主节点连续 3 次未收到心跳，就将该服务器标记为宕机
- 主节点通过心跳维护最新的数据块位置映射表
- 这是主节点检测故障并触发重新复制的核心机制

## 测试用例

### 1. 心跳将服务器注册为存活状态

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

### 2. 服务器状态显示所有已注册的服务器

server_status_ok 应当列出所有服务器的 status、chunk 数量和 last_heartbeat_ms_ago。

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

- [HDFS DataNode Heartbeats](https://hadoop.apache.org/docs/stable/hadoop-project-dist/hadoop-hdfs/HdfsDesign.html#Data_Replication)：HDFS 中 DataNode 通过心跳向 NameNode 汇报的机制说明

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
