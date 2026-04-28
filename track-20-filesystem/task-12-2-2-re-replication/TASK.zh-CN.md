# 实现 Automatic Re-复制

英文标题：Implement Automatic Re-Replication
网页：<https://builddistributedsystem.com/tracks/filesystem/tasks/task-12-2-2-re-replication>

课程：20. 文件系统：分布式文件存储
任务序号：7
短标题：Re-复制
难度：advanced
子主题：Fault Tolerance和Rebalancing

## 中文导读

本题要求你完成 `实现 Automatic Re-复制`。

重点关注：`re-replication`、`under-replicated chunks`、`replication factor`、`failure recovery`。

建议先按提示逐步实现：When a 服务端 dies, its chunks drop below 复制 factor 3。

协议字段、消息类型、输入输出格式请以本文件中的代码块和测试用例为准。

## 题目说明

When a chunk 服务端 dies, its chunks become under-replicated. The master must automatically schedule re-复制 to restore the target 复制 factor.

Re-复制 algorithm:
1. Detect: master notices missing heartbeats from a 服务端和marks it dead
2. Scan: identify all chunks that were on the dead 服务端 — they now have fewer replicas
3. Prioritize: chunks，包含RF=1 are critical (one more 故障 = data loss). Re-replicate them first.
4. Schedule:用于each under-replicated chunk, pick a healthy 服务端 that does NOT already hold the chunk
5. Copy: instruct an existing replica to send the chunk data to the new 服务端
6. Update: add the new 服务端 to the chunk's location list in the master's 元数据

```JSON
请求:  {"type": "check_replication", "msg_id": 1}
响应: {"type": "check_replication_ok", "in_reply_to": 1, "under_replicated": [
    {"chunk": "ch_001", "current_rf": 2, "target_rf": 3, "missing_on": ["cs3"]},
    {"chunk": "ch_005", "current_rf": 1, "target_rf": 3, "priority": "critical"}
]}

请求:  {"type": "replicate_chunk", "msg_id": 2, "chunk": "ch_005", "source": "cs1", "target": "cs4"}
响应: {"type": "replicate_chunk_ok", "in_reply_to": 2, "chunk": "ch_005", "new_rf": 2, "bytes_copied": 67108864}
```

## 涉及概念

- `re-replication`
- `under-replicated chunks`
- `replication factor`
- `failure recovery`

## 实现提示

- When a 服务端 dies, its chunks drop below 复制 factor 3
- The master scans用于under-replicated chunks和schedules re-复制
- Pick a healthy 服务端 that does NOT already hold the chunk to be the new replica
- Copy chunk data from an existing replica to the new 服务端
- Prioritize: chunks，包含复制 factor 1 (one 服务端 故障 from data loss)

## 测试用例

### 1. Check 复制 identifies under-replicated chunks

check_replication_ok should list under_replicated chunks，包含current_rf和target_rf.

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"check_replication","msg_id":2}}
```

期望输出：

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

### 2. Replicate chunk to new server

replicate_chunk_ok should show new_rf > previous RF.

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1","n2","n3","n4"]}}
{"src":"c1","dest":"n1","body":{"type":"replicate_chunk","msg_id":2,"chunk":"ch_005","source":"n2","target":"n4"}}
```

期望输出：

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

## 参考资料

- [HDFS Replication Management](https://hadoop.apache.org/docs/stable/hadoop-project-dist/hadoop-hdfs/HdfsDesign.html)：HDFS documentation on replica placement和re-复制 strategies

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
