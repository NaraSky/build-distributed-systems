# 设计仿 GFS 的分布式文件系统架构

英文标题：Design a GFS-Style Distributed File System Architecture
网页：<https://builddistributedsystem.com/tracks/filesystem/tasks/task-12-1-1-architecture>

课程：20. 文件系统：分布式文件存储
任务序号：1
短标题：DFS Architecture
难度：高级
子主题：Distributed File Storage

## 中文导读

这道题要求你设计一个类似谷歌文件系统（GFS）的分布式文件系统架构，包括文件的创建和元数据查询。GFS 是现代分布式存储的基石，理解它的"主节点管元数据、块服务器管数据"的分离思想，是学习大规模存储系统的第一步。

## 题目说明

谷歌文件系统（GFS）的架构是现代分布式存储的基础。它将元数据（Metadata）与实际数据分开管理：元数据由主节点（Master）负责，数据存放在块服务器（Chunk Server）上。这种设计使得系统可以在数千台机器上存储 PB 级别的数据。

**架构组成**：
- **主节点（Master）**：将所有元数据保存在内存中，包括命名空间（文件和目录的树形结构）以及每个文件到其数据块及其所在位置的映射。元数据的变更会记录到预写日志（WAL）中以保证持久性。
- **块服务器（Chunk Server）**：将 64MB 大小的数据块存储在本地磁盘上。每个块会被复制到 3 台服务器上。
- **客户端（Client）**：先联系主节点获取数据块的位置信息，然后直接与块服务器进行读写操作。

关键设计决策：
1. **大块设计（64MB）**：减少了元数据的大小，也减少了与主节点交互的次数
2. **3 副本（Replication Factor 3）**：可以容忍同时 2 台服务器故障
3. **主节点不参与数据传输**：主节点只处理元数据，数据在客户端和块服务器之间直接流动

```json
Request:  {"type": "dfs_create_file", "msg_id": 1, "path": "/data/logs/2024.log", "chunk_size_mb": 64, "replication_factor": 3}
Response: {"type": "dfs_create_file_ok", "in_reply_to": 1, "chunks": [
    {"chunk_handle": "ch_001", "chunk_servers": ["cs1", "cs2", "cs3"], "primary": "cs1"}
]}

Request:  {"type": "dfs_file_info", "msg_id": 2, "path": "/data/logs/2024.log"}
Response: {"type": "dfs_file_info_ok", "in_reply_to": 2, "size_bytes": 67108864, "chunks": 1, "replication_factor": 3}
```

## 涉及概念

- `GFS architecture`
- `master node`
- `chunk server`
- `64MB chunks`
- `replication factor`

## 实现提示

- 架构有两个核心组件：一个主节点（负责元数据）和多个块服务器（负责数据）
- 文件被切分成固定大小的 64MB 数据块，块越大，元数据的开销越小
- 每个数据块会复制到 3 台块服务器上，以实现容错
- 主节点存储的映射关系为：文件名 -> 列表[(数据块句柄, [块服务器地址])]
- 客户端向主节点查询元数据，然后直接与块服务器交互读写数据，主节点不参与数据传输

## 测试用例

### 1. 创建文件并返回数据块分配信息

dfs_create_file_ok 的返回中应包含 chunks 数组，其中每个元素包含 chunk_handle、chunk_servers（长度为 3）和 primary。

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1","n2","n3"]}}
{"src":"c1","dest":"n1","body":{"type":"dfs_create_file","msg_id":2,"path":"/data/test.log","chunk_size_mb":64,"replication_factor":3}}
```

期望输出：

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

### 2. 查询文件信息并返回元数据

dfs_file_info_ok 的返回中应包含 size_bytes、chunks 数量和 replication_factor。

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

- [The Google File System Paper](https://research.google/pubs/pub51/)：谷歌文件系统的原始论文，由 Ghemawat、Gobioff 和 Leung 于 2003 年发表

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
