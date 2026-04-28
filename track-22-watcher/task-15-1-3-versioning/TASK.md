# Implement Optimistic Concurrency with Version Checks

Website: <https://builddistributedsystem.com/tracks/watcher/tasks/task-15-1-3-versioning>

Track: 22. The Watcher
Task order: 3
Short title: Version Checks
Difficulty: intermediate
Subtrack: The ZNode Data Model

## Problem

ZooKeeper uses version-based optimistic concurrency control. Every `SetData` and `Delete` must specify the expected version. If the version does not match the current version, the operation fails with `BadVersion`.

**How it works**:
1. Client reads ZNode: gets data and version (e.g., version=5)
2. Client modifies the data locally
3. Client sends `SetData(path, new_data, version=5)`
4. Server checks: if current version == 5, apply update and set version=6
5. If another client updated between steps 1 and 3, the version is now 6, and the operation fails with `BadVersion`
6. The client must re-read (get version=6) and retry

This is the ZooKeeper equivalent of a **compare-and-swap** (CAS) operation.

```json
Request:  {"type": "znode_set", "msg_id": 1, "path": "/cfg", "data": "new", "version": 0}
Response: {"type": "znode_set_ok", "in_reply_to": 1, "new_version": 1}

Request:  {"type": "znode_set", "msg_id": 2, "path": "/cfg", "data": "newer", "version": 0}
Response: {"type": "error", "in_reply_to": 2, "code": "BadVersion", "text": "expected version 0, current version 1"}
```

## Concepts

- optimistic concurrency
- version check
- BadVersion
- compare-and-swap
- conflict detection

## Hints

- SetData(path, data, version) only succeeds if current version == specified version
- On success, version increments to version+1
- On version mismatch, return BadVersion error — the client must re-read and retry
- This is an optimistic concurrency control (OCC) mechanism — no locks needed
- version=-1 is a wildcard that bypasses the version check

## Test Cases

### 1. Correct version allows update

znode_set_ok should show new_version: 1.

Input:

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"znode_create","msg_id":2,"path":"/v","data":"a","ephemeral":false,"sequential":false}}
{"src":"c1","dest":"n1","body":{"type":"znode_set","msg_id":3,"path":"/v","data":"b","version":0}}
```

Expected output:

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

### 2. Wrong version returns BadVersion

Second set with version 0 should return BadVersion error (current is now 1).

Input:

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"znode_create","msg_id":2,"path":"/v","data":"a","ephemeral":false,"sequential":false}}
{"src":"c1","dest":"n1","body":{"type":"znode_set","msg_id":3,"path":"/v","data":"b","version":0}}
{"src":"c1","dest":"n1","body":{"type":"znode_set","msg_id":4,"path":"/v","data":"c","version":0}}
```

Expected output:

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

## Resources

- [ZooKeeper Versioning](https://zookeeper.apache.org/doc/current/zookeeperProgrammers.html#sc_zkStatStructure): ZooKeeper documentation on stat structure and version-based CAS

## Java Starter

The matching local starter file is:

```text
src/main/java/Main.java
```
