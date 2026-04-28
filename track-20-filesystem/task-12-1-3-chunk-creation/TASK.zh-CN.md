# 实现 Chunk Creation和Allocation

英文标题：Implement Chunk Creation和Allocation
网页：<https://builddistributedsystem.com/tracks/filesystem/tasks/task-12-1-3-chunk-creation>

课程：20. 文件系统：分布式文件存储
任务序号：3
短标题：Chunk Creation
难度：advanced
子主题：Distributed File Storage

## 中文导读

本题要求你完成 `实现 Chunk Creation和Allocation`。

重点关注：`chunk allocation`、`placement policy`、`rack awareness`、`primary assignment`。

建议先按提示逐步实现：客户端 asks master用于a new chunk; master allocates it on 3 servers和returns their addresses。

协议字段、消息类型、输入输出格式请以本文件中的代码块和测试用例为准。

## 题目说明

When a 客户端 creates a file or appends a new chunk, the master must allocate chunk 存储 on appropriate chunk servers.

Chunk creation flow:
1. 客户端 sends `allocate_chunk` to master
2. Master selects 3 chunk servers based on placement policy:
   - Prefer servers，包含below-average disk utilization
   - Spread across racks用于故障 tolerance (if rack-aware)
   - Prefer locally-close servers用于the primary
3. Master creates chunk 元数据, assigns a unique chunk handle
4. Master designates one 服务端 as the **primary** (via a lease)
5. Returns chunk handle和服务端 addresses to the 客户端
6. 客户端 writes data directly to the primary

```JSON
请求:  {"type": "allocate_chunk", "msg_id": 1, "file": "/data/日志.dat", "chunk_index": 0}
响应: {"type": "allocate_chunk_ok", "in_reply_to": 1, "chunk_handle": "ch_00042", "primary": "cs1", "secondaries": ["cs2", "cs3"], "lease_expires_ms": 60000}
```

## 涉及概念

- `chunk allocation`
- `placement policy`
- `rack awareness`
- `primary assignment`

## 实现提示

- 客户端 asks master用于a new chunk; master allocates it on 3 servers和returns their addresses
- Placement policy: spread replicas across different racks用于故障 tolerance
- The master picks a primary chunk 服务端和grants it a lease
- 客户端 writes to the primary chunk 服务端 directly — master is NOT in the data path
- Return addresses in order: primary first, then secondaries

## 测试用例

### 1. Allocate chunk returns primary和secondaries

allocate_chunk_ok should have a unique chunk_handle, a primary,和2 secondaries.

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1","n2","n3","n4"]}}
{"src":"c1","dest":"n1","body":{"type":"allocate_chunk","msg_id":2,"file":"/data/log.dat","chunk_index":0}}
```

期望输出：

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

### 2. Multiple allocations produce 唯一 chunk handles

Each allocation should produce a different chunk_handle.

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1","n2","n3","n4"]}}
{"src":"c1","dest":"n1","body":{"type":"allocate_chunk","msg_id":2,"file":"/a.dat","chunk_index":0}}
{"src":"c1","dest":"n1","body":{"type":"allocate_chunk","msg_id":3,"file":"/b.dat","chunk_index":0}}
```

期望输出：

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

## 参考资料

- [GFS Chunk Allocation](https://research.google/pubs/pub51/)：GFS paper section on chunk creation, placement,和replica management

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
