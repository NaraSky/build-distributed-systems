# Implement ZNode CRUD Operations

Website: <https://builddistributedsystem.com/tracks/watcher/tasks/task-15-1-2-crud>

Track: 22. The Watcher
Task order: 2
Short title: ZNode CRUD
Difficulty: intermediate
Subtrack: The ZNode Data Model

## Problem

ZooKeeper provides five core operations for manipulating ZNodes. Together they form a complete API for coordination metadata.

**Operations**:
- `Create(path, data, flags)`: create a new ZNode. Fails if it already exists.
- `GetData(path)`: return the data, version, and stat of a ZNode.
- `SetData(path, data, version)`: update the data. The version must match the current version (optimistic locking).
- `Delete(path, version)`: delete a ZNode. Version must match. Fails if the node has children.
- `GetChildren(path)`: return the list of child node names.

```json
Request:  {"type": "znode_set", "msg_id": 1, "path": "/config", "data": "new-value", "version": 0}
Response: {"type": "znode_set_ok", "in_reply_to": 1, "new_version": 1}

Request:  {"type": "znode_delete", "msg_id": 2, "path": "/config", "version": 1}
Response: {"type": "znode_delete_ok", "in_reply_to": 2}

Request:  {"type": "znode_children", "msg_id": 3, "path": "/services"}
Response: {"type": "znode_children_ok", "in_reply_to": 3, "children": ["web", "db", "cache"]}
```

## Concepts

- Create
- GetData
- SetData
- Delete
- GetChildren

## Hints

- Create takes path, data, and flags (ephemeral, sequential)
- SetData and Delete require a version parameter for optimistic concurrency
- GetChildren returns the list of child node names (not full paths)
- Delete fails if the node has children (must delete children first)
- All operations are atomic — no partial updates

## Test Cases

### 1. SetData updates version

znode_set_ok should show new_version: 1.

Input:

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"znode_create","msg_id":2,"path":"/cfg","data":"v1","ephemeral":false,"sequential":false}}
{"src":"c1","dest":"n1","body":{"type":"znode_set","msg_id":3,"path":"/cfg","data":"v2","version":0}}
```

Expected output:

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

### 2. Delete removes ZNode

After delete, znode_get should return NoNode error.

Input:

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"znode_create","msg_id":2,"path":"/tmp","data":"","ephemeral":false,"sequential":false}}
{"src":"c1","dest":"n1","body":{"type":"znode_delete","msg_id":3,"path":"/tmp","version":0}}
{"src":"c1","dest":"n1","body":{"type":"znode_get","msg_id":4,"path":"/tmp"}}
```

Expected output:

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

## Resources

- [ZooKeeper Operations](https://zookeeper.apache.org/doc/current/zookeeperProgrammers.html#ch_zkOperations): ZooKeeper documentation on CRUD operations and versioning

## Java Starter

The matching local starter file is:

```text
src/main/java/Main.java
```
