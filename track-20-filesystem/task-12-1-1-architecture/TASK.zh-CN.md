# Design a GFS-Style Distributed File System Architecture

英文标题：Design a GFS-Style Distributed File System Architecture
网页：<https://builddistributedsystem.com/tracks/filesystem/tasks/task-12-1-1-architecture>

课程：20. 文件系统：分布式文件存储
任务序号：1
短标题：DFS Architecture
难度：advanced
子主题：Distributed File Storage

## 中文导读

本题要求你完成 `Design a GFS-Style Distributed File System Architecture`。

重点关注：`GFS architecture`、`master node`、`chunk server`、`64MB chunks`、`replication factor`。

建议先按提示逐步实现：The architecture has two components: a single master (元数据)和many chunk servers (data)。

协议字段、消息类型、输入输出格式请以本文件中的代码块和测试用例为准。

## 题目说明

The Google File System (GFS) architecture is the foundation of modern distributed 存储. It separates 元数据 (managed by a master) from data (stored on chunk servers), enabling petabyte-scale 存储 across thousands of machines.

**Architecture**:
- **Master 节点**: stores all 元数据 in memory — the namespace (file/directory tree)和the mapping of each file to its chunks和their locations. 元数据 changes are logged to a WAL用于durability.
- **Chunk servers**: store 64MB data chunks on local disks. Each chunk is replicated to 3 servers.
- **Clients**: contact the master to discover chunk locations, then read/write directly to chunk servers.

Key design decisions:
1. **Large chunks (64MB)**: reduces 元数据 size和the number of master interactions
2. **复制 factor 3**: tolerates 2 simultaneous 服务端 failures
3. **Master out of data path**: the master only handles 元数据; data flows directly between clients和chunk servers

```JSON
请求:  {"type": "dfs_create_file", "msg_id": 1, "path": "/data/logs/2024.日志", "chunk_size_mb": 64, "replication_factor": 3}
响应: {"type": "dfs_create_file_ok", "in_reply_to": 1, "chunks": [
    {"chunk_handle": "ch_001", "chunk_servers": ["cs1", "cs2", "cs3"], "primary": "cs1"}
]}

请求:  {"type": "dfs_file_info", "msg_id": 2, "path": "/data/logs/2024.日志"}
响应: {"type": "dfs_file_info_ok", "in_reply_to": 2, "size_bytes": 67108864, "chunks": 1, "replication_factor": 3}
```

## 涉及概念

- `GFS architecture`
- `master node`
- `chunk server`
- `64MB chunks`
- `replication factor`

## 实现提示

- The architecture has two components: a single master (元数据)和many chunk servers (data)
- Files are split into fixed-size 64MB chunks — large to minimize 元数据 overhead
- Each chunk is replicated to 3 chunk servers用于故障 tolerance
- The master stores the mapping: filename -> list of (chunk_handle, [chunk_server_addresses])
- Clients talk to the master用于元数据和directly to chunk servers用于data — the master is never in the data path

## 测试用例

### 1. 创建 file returns chunk allocation

dfs_create_file_ok should include a chunks array，包含chunk_handle, chunk_servers (length 3),和primary.

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1","n2","n3"]}}
{"src":"c1","dest":"n1","body":{"type":"dfs_create_file","msg_id":2,"path":"/data/test.log","chunk_size_mb":64,"replication_factor":3}}
```

期望输出：

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

### 2. File info returns metadata

dfs_file_info_ok should include size_bytes, chunks count,和replication_factor.

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"dfs_file_info","msg_id":2,"path":"/data/test.log"}}
```

期望输出：

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

## 参考资料

- [The Google File System Paper](https://research.google/pubs/pub51/)：The original GFS paper by Ghemawat, Gobioff,和Leung (2003)

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
