# Implement the Master Namespace Tree

Website: <https://builddistributedsystem.com/tracks/filesystem/tasks/task-12-1-2-namespace>

Track: 20. The Filesystem
Task order: 2
Short title: Master Namespace
Difficulty: advanced
Subtrack: Distributed File Storage

## Problem

The master's namespace is a hierarchical tree of directories and files. It maps every file to its chunks and their locations. This is stored entirely in memory for fast lookups, with all mutations persisted to a WAL.

Namespace structure:
```
/
  /data/
    /data/logs/
      /data/logs/2024.log -> [ch_001@[cs1,cs2,cs3], ch_002@[cs2,cs3,cs4]]
    /data/metrics/
      /data/metrics/cpu.dat -> [ch_003@[cs1,cs3,cs5]]
```

Each file maps to a list of chunk entries: `(chunk_handle, [chunk_server_addresses])`

Operations:
- `mkdir(path)`: create a directory
- `create(path)`: create a file, allocate initial chunks
- `lookup(path)`: return chunk locations for a file
- `ls(path)`: list children of a directory

```json
Request:  {"type": "ns_mkdir", "msg_id": 1, "path": "/data/logs"}
Response: {"type": "ns_mkdir_ok", "in_reply_to": 1, "path": "/data/logs"}

Request:  {"type": "ns_lookup", "msg_id": 2, "path": "/data/logs/2024.log"}
Response: {"type": "ns_lookup_ok", "in_reply_to": 2, "chunks": [{"chunk_handle": "ch_001", "servers": ["cs1", "cs2", "cs3"]}]}
```

## Concepts

- namespace tree
- directory hierarchy
- chunk mapping
- metadata
- WAL-backed

## Hints

- The namespace is a tree of directories and files, similar to a Unix filesystem
- Each file node stores: list of (chunk_handle, [chunk_server_addresses])
- Store the namespace in memory for fast lookups; persist changes to a WAL
- Operations: mkdir, create, lookup, list_directory, delete
- All namespace mutations are logged to WAL before being applied to memory

## Test Cases

### 1. Create directory and list it

ns_ls_ok should list "data" as a child of root.

Input:

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"ns_mkdir","msg_id":2,"path":"/data"}}
{"src":"c1","dest":"n1","body":{"type":"ns_ls","msg_id":3,"path":"/"}}
```

Expected output:

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
{"src": "n1", "dest": "c1", "body": {"type": "ns_mkdir_ok", "in_reply_to": 2, "path": "/data", "msg_id": 1}}
```

### 2. Lookup file returns chunk locations

ns_lookup_ok should return chunks array with chunk_handle and servers list.

Input:

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"ns_lookup","msg_id":2,"path":"/data/test.log"}}
```

Expected output:

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

## Resources

- [HDFS Architecture Guide](https://hadoop.apache.org/docs/stable/hadoop-project-dist/hadoop-hdfs/HdfsDesign.html): Apache HDFS architecture documenting the NameNode namespace design

## Java Starter

The matching local starter file is:

```text
src/main/java/Main.java
```
