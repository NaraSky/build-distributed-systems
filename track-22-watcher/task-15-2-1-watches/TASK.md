# Implement One-Shot Watches for Change Notification

Website: <https://builddistributedsystem.com/tracks/watcher/tasks/task-15-2-1-watches>

Track: 22. The Watcher
Task order: 6
Short title: Watches
Difficulty: intermediate
Subtrack: Watches and Sessions

## Problem

Watches enable push-based notification when a ZNode changes. Instead of polling, clients register a watch and ZooKeeper notifies them when the node is modified.

**Watch flow**:
1. Client calls `GetData("/config", watch=true)` — receives current data AND registers a watch
2. When another client calls `SetData("/config", new_data, version)`
3. ZooKeeper sends a `WatchEvent(NodeDataChanged)` to the watching client
4. The watch is removed (one-shot); client must re-register to watch again

**Watch events**:
- `NodeDataChanged`: node data was modified
- `NodeDeleted`: node was deleted
- `NodeChildrenChanged`: children were added or removed

```json
Request:  {"type": "znode_get_watch", "msg_id": 1, "path": "/config", "watch": true, "watcher_id": "w1"}
Response: {"type": "znode_get_watch_ok", "in_reply_to": 1, "data": "v1", "version": 0, "watch_registered": true}

Event:    {"type": "watch_event", "path": "/config", "event_type": "NodeDataChanged", "watcher_id": "w1"}
```

## Concepts

- watch
- one-shot
- WatchEvent
- change notification
- push-based

## Hints

- GetData(path, watch=true) registers a one-shot watch on the node
- When the node data changes, the watcher receives a WatchEvent notification
- Watches are one-shot: they fire once, then are removed. Client must re-register.
- Watch events: NodeDataChanged, NodeDeleted, NodeChildrenChanged
- Watches are ordered: the client always sees the watch event before the new data

## Test Cases

### 1. Register watch and receive event on change

znode_get_watch_ok should include data, version, and watch_registered: true.

Input:

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"znode_get_watch","msg_id":2,"path":"/cfg","watch":true,"watcher_id":"w1"}}
```

Expected output:

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

### 2. Watch fires on data change

After SetData, a watch_event with event_type NodeDataChanged should be sent to w1.

Input:

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"znode_create","msg_id":2,"path":"/w","data":"old","ephemeral":false,"sequential":false}}
{"src":"c1","dest":"n1","body":{"type":"znode_get_watch","msg_id":3,"path":"/w","watch":true,"watcher_id":"w1"}}
{"src":"c1","dest":"n1","body":{"type":"znode_set","msg_id":4,"path":"/w","data":"new","version":0}}
```

Expected output:

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

## Resources

- [ZooKeeper Watches](https://zookeeper.apache.org/doc/current/zookeeperProgrammers.html#ch_zkWatches): ZooKeeper documentation on watches and notification semantics

## Java Starter

The matching local starter file is:

```text
src/main/java/Main.java
```
