# Implement Chunk Replication with Pipeline Writes

Website: <https://builddistributedsystem.com/tracks/filesystem/tasks/task-12-1-4-chunk-replication>

Track: 20. The Filesystem
Task order: 4
Short title: Chunk Replication
Difficulty: advanced
Subtrack: Distributed File Storage

## Problem

When a client writes data, the primary chunk server coordinates replication to all secondaries. GFS uses a **pipeline** design where data flows in a chain to maximize network throughput.

Write replication flow:
1. Client sends data to the **closest** chunk server (not necessarily the primary)
2. That server forwards the data to the next closest server in the chain
3. Data flows as a pipeline: server A -> server B -> server C
4. Once all servers have the data cached, the client sends a **write request** to the primary
5. The primary assigns a serial number to the write (for ordering)
6. The primary applies the write locally, then forwards the serial order to secondaries
7. Secondaries apply the write in the same order
8. All servers acknowledge -> primary replies to client

This separates **data flow** (pipeline for throughput) from **control flow** (primary for ordering).

```json
Request:  {"type": "chunk_write", "msg_id": 1, "chunk_handle": "ch_001", "offset": 0, "data": "hello world", "primary": "cs1", "secondaries": ["cs2", "cs3"]}
Response: {"type": "chunk_write_ok", "in_reply_to": 1, "bytes_written": 11, "replicas_acked": 3, "serial_number": 1}
```

## Concepts

- chunk replication
- pipeline writes
- primary-secondary
- write acknowledgement
- data flow

## Hints

- The primary receives the write and forwards it to the secondaries in a pipeline
- Pipeline: client -> primary -> secondary1 -> secondary2 (data flows in a chain)
- All three must acknowledge before the write is considered successful
- If any replica fails, the write fails and the client retries
- GFS separates data flow (pipeline) from control flow (primary commits order)

## Test Cases

### 1. Write replicates to all servers

chunk_write_ok should show replicas_acked: 3.

Input:

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1","n2","n3"]}}
{"src":"c1","dest":"n1","body":{"type":"chunk_write","msg_id":2,"chunk_handle":"ch_001","offset":0,"data":"hello","primary":"n1","secondaries":["n2","n3"]}}
```

Expected output:

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

### 2. Sequential writes get increasing serial numbers

Second write serial_number should be greater than first.

Input:

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1","n2","n3"]}}
{"src":"c1","dest":"n1","body":{"type":"chunk_write","msg_id":2,"chunk_handle":"ch_001","offset":0,"data":"a","primary":"n1","secondaries":["n2","n3"]}}
{"src":"c1","dest":"n1","body":{"type":"chunk_write","msg_id":3,"chunk_handle":"ch_001","offset":1,"data":"b","primary":"n1","secondaries":["n2","n3"]}}
```

Expected output:

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

## Resources

- [GFS Data Flow Pipeline](https://research.google/pubs/pub51/): GFS paper section on pipeline writes and data/control flow separation

## Java Starter

The matching local starter file is:

```text
src/main/java/Main.java
```
