# 实现 the Master Namespace Tree

英文标题：Implement the Master Namespace Tree
网页：<https://builddistributedsystem.com/tracks/filesystem/tasks/task-12-1-2-namespace>

课程：20. 文件系统：分布式文件存储
任务序号：2
短标题：Master Namespace
难度：advanced
子主题：Distributed File Storage

## 中文导读

本题要求你完成 `实现 the Master Namespace Tree`。

重点关注：`namespace tree`、`directory hierarchy`、`chunk mapping`、`metadata`、`WAL-backed`。

建议先按提示逐步实现：The namespace is a tree of directories和files, similar to a Unix filesystem。

协议字段、消息类型、输入输出格式请以本文件中的代码块和测试用例为准。

## 题目说明

The master's namespace is a hierarchical tree of directories和files. It maps every file to its chunks和their locations. This is stored entirely in memory用于fast lookups,，包含all mutations persisted to a WAL.

Namespace structure:
```
/
  /data/
    /data/logs/
      /data/logs/2024.日志 -> [ch_001@[cs1,cs2,cs3], ch_002@[cs2,cs3,cs4]]
    /data/metrics/
      /data/metrics/cpu.dat -> [ch_003@[cs1,cs3,cs5]]
```

Each file maps to a list of chunk entries: `(chunk_handle, [chunk_server_addresses])`

Operations:
- `mkdir(path)`: create a directory
- `create(path)`: create a file, allocate initial chunks
- `lookup(path)`: return chunk locations用于a file
- `ls(path)`: list children of a directory

```JSON
请求:  {"type": "ns_mkdir", "msg_id": 1, "path": "/data/logs"}
响应: {"type": "ns_mkdir_ok", "in_reply_to": 1, "path": "/data/logs"}

请求:  {"type": "ns_lookup", "msg_id": 2, "path": "/data/logs/2024.日志"}
响应: {"type": "ns_lookup_ok", "in_reply_to": 2, "chunks": [{"chunk_handle": "ch_001", "servers": ["cs1", "cs2", "cs3"]}]}
```

## 涉及概念

- `namespace tree`
- `directory hierarchy`
- `chunk mapping`
- `metadata`
- `WAL-backed`

## 实现提示

- The namespace is a tree of directories和files, similar to a Unix filesystem
- Each file 节点 stores: list of (chunk_handle, [chunk_server_addresses])
- Store the namespace in memory用于fast lookups; persist changes to a WAL
- Operations: mkdir, create, lookup, list_directory, delete
- All namespace mutations are logged to WAL before being applied to memory

## 测试用例

### 1. 创建 directory和list it

ns_ls_ok should list "data" as a child of root.

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

### 2. Lookup file returns chunk locations

ns_lookup_ok should return chunks array，包含chunk_handle和servers list.

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

- [HDFS Architecture Guide](https://hadoop.apache.org/docs/stable/hadoop-project-dist/hadoop-hdfs/HdfsDesign.html)：Apache HDFS architecture documenting the NameNode namespace design

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
