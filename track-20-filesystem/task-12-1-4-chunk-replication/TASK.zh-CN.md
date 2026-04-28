# 实现 Chunk 复制，包含Pipeline Writes

英文标题：Implement Chunk Replication，包含Pipeline Writes
网页：<https://builddistributedsystem.com/tracks/filesystem/tasks/task-12-1-4-chunk-replication>

课程：20. 文件系统：分布式文件存储
任务序号：4
短标题：Chunk 复制
难度：advanced
子主题：Distributed File Storage

## 中文导读

本题要求你完成 `实现 Chunk 复制，包含Pipeline Writes`。

重点关注：`chunk replication`、`pipeline writes`、`primary-secondary`、`write acknowledgement`、`data flow`。

建议先按提示逐步实现：The primary receives the write和forwards it to the secondaries in a pipeline。

协议字段、消息类型、输入输出格式请以本文件中的代码块和测试用例为准。

## 题目说明

When a 客户端 writes data, the primary chunk 服务端 coordinates 复制 to all secondaries. GFS uses a **pipeline** design where data flows in a chain to maximize 网络 throughput.

Write 复制 flow:
1. 客户端 sends data to the **closest** chunk 服务端 (not necessarily the primary)
2. That 服务端 forwards the data to the next closest 服务端 in the chain
3. Data flows as a pipeline: 服务端 A -> 服务端 B -> 服务端 C
4. Once all servers have the data cached, the 客户端 sends a **write 请求** to the primary
5. The primary assigns a serial number to the write (for ordering)
6. The primary applies the write locally, then forwards the serial order to secondaries
7. Secondaries apply the write in the same order
8. All servers acknowledge -> primary replies to 客户端

This separates **data flow** (pipeline用于throughput) from **control flow** (primary用于ordering).

```JSON
请求:  {"type": "chunk_write", "msg_id": 1, "chunk_handle": "ch_001", "offset": 0, "data": "hello world", "primary": "cs1", "secondaries": ["cs2", "cs3"]}
响应: {"type": "chunk_write_ok", "in_reply_to": 1, "bytes_written": 11, "replicas_acked": 3, "serial_number": 1}
```

## 涉及概念

- `chunk replication`
- `pipeline writes`
- `primary-secondary`
- `write acknowledgement`
- `data flow`

## 实现提示

- The primary receives the write和forwards it to the secondaries in a pipeline
- Pipeline: 客户端 -> primary -> secondary1 -> secondary2 (data flows in a chain)
- All three must acknowledge before the write is considered successful
- If any replica fails, the write fails和the 客户端 retries
- GFS separates data flow (pipeline) from control flow (primary commits order)

## 测试用例

### 1. Write replicates to all servers

chunk_write_ok should show replicas_acked: 3.

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1","n2","n3"]}}
{"src":"c1","dest":"n1","body":{"type":"chunk_write","msg_id":2,"chunk_handle":"ch_001","offset":0,"data":"hello","primary":"n1","secondaries":["n2","n3"]}}
```

期望输出：

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

### 2. Sequential writes get increasing serial numbers

Second write serial_number should be greater than first.

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1","n2","n3"]}}
{"src":"c1","dest":"n1","body":{"type":"chunk_write","msg_id":2,"chunk_handle":"ch_001","offset":0,"data":"a","primary":"n1","secondaries":["n2","n3"]}}
{"src":"c1","dest":"n1","body":{"type":"chunk_write","msg_id":3,"chunk_handle":"ch_001","offset":1,"data":"b","primary":"n1","secondaries":["n2","n3"]}}
```

期望输出：

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

## 参考资料

- [GFS Data Flow Pipeline](https://research.google/pubs/pub51/)：GFS paper section on pipeline writes和data/control flow separation

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
