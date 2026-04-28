# 实现主节点的命名空间树

英文标题：Implement the Master Namespace Tree
网页：<https://builddistributedsystem.com/tracks/filesystem/tasks/task-12-1-2-namespace>

课程：20. 文件系统：分布式文件存储
任务序号：2
短标题：Master Namespace
难度：高级
子主题：Distributed File Storage

## 中文导读

这道题要求你实现主节点上的命名空间树，即目录和文件的层级结构。命名空间树是整个分布式文件系统的"索引"，有了它才能根据文件路径找到对应的数据块存放在哪些服务器上。

## 题目说明

主节点的命名空间（Namespace）是一棵由目录和文件组成的层级树。它记录了每个文件到其数据块以及块所在位置的映射关系。这棵树完全保存在内存中以支持快速查找，所有变更都会持久化到预写日志（WAL）。

命名空间的结构示例：
```
/
  /data/
    /data/logs/
      /data/logs/2024.log -> [ch_001@[cs1,cs2,cs3], ch_002@[cs2,cs3,cs4]]
    /data/metrics/
      /data/metrics/cpu.dat -> [ch_003@[cs1,cs3,cs5]]
```

每个文件映射到一组数据块条目：`(数据块句柄, [块服务器地址列表])`

支持的操作：
- `mkdir(path)`：创建一个目录
- `create(path)`：创建一个文件，并分配初始数据块
- `lookup(path)`：返回某个文件的数据块位置信息
- `ls(path)`：列出某个目录的子项

```json
Request:  {"type": "ns_mkdir", "msg_id": 1, "path": "/data/logs"}
Response: {"type": "ns_mkdir_ok", "in_reply_to": 1, "path": "/data/logs"}

Request:  {"type": "ns_lookup", "msg_id": 2, "path": "/data/logs/2024.log"}
Response: {"type": "ns_lookup_ok", "in_reply_to": 2, "chunks": [{"chunk_handle": "ch_001", "servers": ["cs1", "cs2", "cs3"]}]}
```

## 涉及概念

- `namespace tree`
- `directory hierarchy`
- `chunk mapping`
- `metadata`
- `WAL-backed`

## 实现提示

- 命名空间是一棵由目录和文件组成的树，类似于 Unix 文件系统
- 每个文件节点存储：数据块列表 [(数据块句柄, [块服务器地址])]
- 将命名空间保存在内存中以支持快速查找；通过预写日志持久化变更
- 支持的操作包括：创建目录、创建文件、查找、列目录、删除
- 所有命名空间的变更必须先写入预写日志，再应用到内存中

## 测试用例

### 1. 创建目录并列出内容

ns_ls_ok 应当列出 "data" 作为根目录的子项。

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"ns_mkdir","msg_id":2,"path":"/data"}}
{"src":"c1","dest":"n1","body":{"type":"ns_ls","msg_id":3,"path":"/"}}
```

期望输出：

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
{"src": "n1", "dest": "c1", "body": {"type": "ns_mkdir_ok", "in_reply_to": 2, "path": "/data", "msg_id": 1}}
```

### 2. 查找文件并返回数据块位置

ns_lookup_ok 应当返回 chunks 数组，其中每个元素包含 chunk_handle 和 servers 列表。

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"ns_lookup","msg_id":2,"path":"/data/test.log"}}
```

期望输出：

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

## 参考资料

- [HDFS Architecture Guide](https://hadoop.apache.org/docs/stable/hadoop-project-dist/hadoop-hdfs/HdfsDesign.html)：Apache HDFS 架构文档，详细说明了 NameNode 的命名空间设计

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
