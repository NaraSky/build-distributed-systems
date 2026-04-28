# Design a GFS-Style Distributed File System Architecture

Website: <https://builddistributedsystem.com/tracks/filesystem/tasks/task-12-1-1-architecture>

Track: 20. The Filesystem
Task order: 1
Short title: DFS Architecture
Difficulty: advanced
Subtrack: Distributed File Storage

## Problem

The Google File System (GFS) architecture is the foundation of modern distributed storage. It separates metadata (managed by a master) from data (stored on chunk servers), enabling petabyte-scale storage across thousands of machines.

**Architecture**:
- **Master node**: stores all metadata in memory — the namespace (file/directory tree) and the mapping of each file to its chunks and their locations. Metadata changes are logged to a WAL for durability.
- **Chunk servers**: store 64MB data chunks on local disks. Each chunk is replicated to 3 servers.
- **Clients**: contact the master to discover chunk locations, then read/write directly to chunk servers.

Key design decisions:
1. **Large chunks (64MB)**: reduces metadata size and the number of master interactions
2. **Replication factor 3**: tolerates 2 simultaneous server failures
3. **Master out of data path**: the master only handles metadata; data flows directly between clients and chunk servers

```json
Request:  {"type": "dfs_create_file", "msg_id": 1, "path": "/data/logs/2024.log", "chunk_size_mb": 64, "replication_factor": 3}
Response: {"type": "dfs_create_file_ok", "in_reply_to": 1, "chunks": [
    {"chunk_handle": "ch_001", "chunk_servers": ["cs1", "cs2", "cs3"], "primary": "cs1"}
]}

Request:  {"type": "dfs_file_info", "msg_id": 2, "path": "/data/logs/2024.log"}
Response: {"type": "dfs_file_info_ok", "in_reply_to": 2, "size_bytes": 67108864, "chunks": 1, "replication_factor": 3}
```

## Concepts

- GFS architecture
- master node
- chunk server
- 64MB chunks
- replication factor

## Hints

- The architecture has two components: a single master (metadata) and many chunk servers (data)
- Files are split into fixed-size 64MB chunks — large to minimize metadata overhead
- Each chunk is replicated to 3 chunk servers for fault tolerance
- The master stores the mapping: filename -> list of (chunk_handle, [chunk_server_addresses])
- Clients talk to the master for metadata and directly to chunk servers for data — the master is never in the data path

## Test Cases

### 1. Create file returns chunk allocation

dfs_create_file_ok should include a chunks array with chunk_handle, chunk_servers (length 3), and primary.

Input:

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1","n2","n3"]}}
{"src":"c1","dest":"n1","body":{"type":"dfs_create_file","msg_id":2,"path":"/data/test.log","chunk_size_mb":64,"replication_factor":3}}
```

Expected output:

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

### 2. File info returns metadata

dfs_file_info_ok should include size_bytes, chunks count, and replication_factor.

Input:

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"dfs_file_info","msg_id":2,"path":"/data/test.log"}}
```

Expected output:

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

## Resources

- [The Google File System Paper](https://research.google/pubs/pub51/): The original GFS paper by Ghemawat, Gobioff, and Leung (2003)

## Java Starter

The matching local starter file is:

```text
src/main/java/Main.java
```
