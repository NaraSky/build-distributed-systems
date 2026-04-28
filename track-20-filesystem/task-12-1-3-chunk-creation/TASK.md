# Implement Chunk Creation and Allocation

Website: <https://builddistributedsystem.com/tracks/filesystem/tasks/task-12-1-3-chunk-creation>

Track: 20. The Filesystem
Task order: 3
Short title: Chunk Creation
Difficulty: advanced
Subtrack: Distributed File Storage

## Problem

When a client creates a file or appends a new chunk, the master must allocate chunk storage on appropriate chunk servers.

Chunk creation flow:
1. Client sends `allocate_chunk` to master
2. Master selects 3 chunk servers based on placement policy:
   - Prefer servers with below-average disk utilization
   - Spread across racks for fault tolerance (if rack-aware)
   - Prefer locally-close servers for the primary
3. Master creates chunk metadata, assigns a unique chunk handle
4. Master designates one server as the **primary** (via a lease)
5. Returns chunk handle and server addresses to the client
6. Client writes data directly to the primary

```json
Request:  {"type": "allocate_chunk", "msg_id": 1, "file": "/data/log.dat", "chunk_index": 0}
Response: {"type": "allocate_chunk_ok", "in_reply_to": 1, "chunk_handle": "ch_00042", "primary": "cs1", "secondaries": ["cs2", "cs3"], "lease_expires_ms": 60000}
```

## Concepts

- chunk allocation
- placement policy
- rack awareness
- primary assignment

## Hints

- Client asks master for a new chunk; master allocates it on 3 servers and returns their addresses
- Placement policy: spread replicas across different racks for fault tolerance
- The master picks a primary chunk server and grants it a lease
- Client writes to the primary chunk server directly — master is NOT in the data path
- Return addresses in order: primary first, then secondaries

## Test Cases

### 1. Allocate chunk returns primary and secondaries

allocate_chunk_ok should have a unique chunk_handle, a primary, and 2 secondaries.

Input:

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1","n2","n3","n4"]}}
{"src":"c1","dest":"n1","body":{"type":"allocate_chunk","msg_id":2,"file":"/data/log.dat","chunk_index":0}}
```

Expected output:

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

### 2. Multiple allocations produce unique chunk handles

Each allocation should produce a different chunk_handle.

Input:

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1","n2","n3","n4"]}}
{"src":"c1","dest":"n1","body":{"type":"allocate_chunk","msg_id":2,"file":"/a.dat","chunk_index":0}}
{"src":"c1","dest":"n1","body":{"type":"allocate_chunk","msg_id":3,"file":"/b.dat","chunk_index":0}}
```

Expected output:

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

## Resources

- [GFS Chunk Allocation](https://research.google/pubs/pub51/): GFS paper section on chunk creation, placement, and replica management

## Java Starter

The matching local starter file is:

```text
src/main/java/Main.java
```
