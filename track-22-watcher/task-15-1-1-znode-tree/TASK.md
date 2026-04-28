# Implement a ZNode Tree Data Model

Website: <https://builddistributedsystem.com/tracks/watcher/tasks/task-15-1-1-znode-tree>

Track: 22. The Watcher
Task order: 1
Short title: ZNode Tree
Difficulty: intermediate
Subtrack: The ZNode Data Model

## Problem

The ZNode data model is a filesystem-like hierarchy where each node stores a small amount of data (up to 1MB). ZNodes are designed for coordination metadata, not bulk data storage.

**ZNode properties**:
- `path`: filesystem-like path (e.g., `/services/web/instance-1`)
- `data`: arbitrary byte array (typically small: config values, leader IDs)
- `version`: monotonically increasing integer, incremented on every data update
- `children`: list of child node names
- `ephemeral`: if true, node is auto-deleted when the creating session expires
- `sequential`: if true, ZooKeeper appends a 10-digit sequence number to the node name

```json
Request:  {"type": "znode_create", "msg_id": 1, "path": "/services", "data": "", "ephemeral": false, "sequential": false}
Response: {"type": "znode_create_ok", "in_reply_to": 1, "path": "/services", "version": 0}

Request:  {"type": "znode_get", "msg_id": 2, "path": "/services"}
Response: {"type": "znode_get_ok", "in_reply_to": 2, "path": "/services", "data": "", "version": 0, "children": [], "ephemeral": false}
```

## Concepts

- ZNode
- hierarchical tree
- path
- data
- version
- ephemeral
- sequential

## Hints

- A ZNode is a node in a tree, similar to a filesystem path (e.g., /services/web/instance-1)
- Each ZNode stores: path, data (byte array), version (integer), children list
- ZNodes have flags: ephemeral (deleted when session expires) and sequential (auto-numbered)
- The root ZNode "/" always exists and cannot be deleted
- Version starts at 0 and increments on every data update

## Test Cases

### 1. Create and get ZNode

znode_get_ok should return data "config" and version 0.

Input:

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"znode_create","msg_id":2,"path":"/app","data":"config","ephemeral":false,"sequential":false}}
{"src":"c1","dest":"n1","body":{"type":"znode_get","msg_id":3,"path":"/app"}}
```

Expected output:

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

### 2. Create child nodes

znode_get_ok for /app should show ["db"] in children.

Input:

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"znode_create","msg_id":2,"path":"/app","data":"","ephemeral":false,"sequential":false}}
{"src":"c1","dest":"n1","body":{"type":"znode_create","msg_id":3,"path":"/app/db","data":"mysql","ephemeral":false,"sequential":false}}
{"src":"c1","dest":"n1","body":{"type":"znode_get","msg_id":4,"path":"/app"}}
```

Expected output:

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

## Resources

- [ZooKeeper Data Model](https://zookeeper.apache.org/doc/current/zookeeperProgrammers.html#ch_zkDataModel): ZooKeeper documentation on znodes and the hierarchical namespace

## Java Starter

The matching local starter file is:

```text
src/main/java/Main.java
```
