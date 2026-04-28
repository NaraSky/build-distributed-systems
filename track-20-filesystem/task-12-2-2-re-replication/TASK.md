# Implement Automatic Re-Replication

Website: <https://builddistributedsystem.com/tracks/filesystem/tasks/task-12-2-2-re-replication>

Track: 20. The Filesystem
Task order: 7
Short title: Re-Replication
Difficulty: advanced
Subtrack: Fault Tolerance and Rebalancing

## Problem

When a chunk server dies, its chunks become under-replicated. The master must automatically schedule re-replication to restore the target replication factor.

Re-replication algorithm:
1. Detect: master notices missing heartbeats from a server and marks it dead
2. Scan: identify all chunks that were on the dead server — they now have fewer replicas
3. Prioritize: chunks with RF=1 are critical (one more failure = data loss). Re-replicate them first.
4. Schedule: for each under-replicated chunk, pick a healthy server that does NOT already hold the chunk
5. Copy: instruct an existing replica to send the chunk data to the new server
6. Update: add the new server to the chunk's location list in the master's metadata

```json
Request:  {"type": "check_replication", "msg_id": 1}
Response: {"type": "check_replication_ok", "in_reply_to": 1, "under_replicated": [
    {"chunk": "ch_001", "current_rf": 2, "target_rf": 3, "missing_on": ["cs3"]},
    {"chunk": "ch_005", "current_rf": 1, "target_rf": 3, "priority": "critical"}
]}

Request:  {"type": "replicate_chunk", "msg_id": 2, "chunk": "ch_005", "source": "cs1", "target": "cs4"}
Response: {"type": "replicate_chunk_ok", "in_reply_to": 2, "chunk": "ch_005", "new_rf": 2, "bytes_copied": 67108864}
```

## Concepts

- re-replication
- under-replicated chunks
- replication factor
- failure recovery

## Hints

- When a server dies, its chunks drop below replication factor 3
- The master scans for under-replicated chunks and schedules re-replication
- Pick a healthy server that does NOT already hold the chunk to be the new replica
- Copy chunk data from an existing replica to the new server
- Prioritize: chunks with replication factor 1 (one server failure from data loss)

## Test Cases

### 1. Check replication identifies under-replicated chunks

check_replication_ok should list under_replicated chunks with current_rf and target_rf.

Input:

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"check_replication","msg_id":2}}
```

Expected output:

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

### 2. Replicate chunk to new server

replicate_chunk_ok should show new_rf > previous RF.

Input:

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1","n2","n3","n4"]}}
{"src":"c1","dest":"n1","body":{"type":"replicate_chunk","msg_id":2,"chunk":"ch_005","source":"n2","target":"n4"}}
```

Expected output:

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

## Resources

- [HDFS Replication Management](https://hadoop.apache.org/docs/stable/hadoop-project-dist/hadoop-hdfs/HdfsDesign.html): HDFS documentation on replica placement and re-replication strategies

## Java Starter

The matching local starter file is:

```text
src/main/java/Main.java
```
