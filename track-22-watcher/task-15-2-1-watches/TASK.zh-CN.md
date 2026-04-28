# 实现 One-Shot Watches用于Change Notification

英文标题：Implement One-Shot Watches用于Change Notification
网页：<https://builddistributedsystem.com/tracks/watcher/tasks/task-15-2-1-watches>

课程：22. 观察者：ZooKeeper/etcd 模型
任务序号：6
短标题：Watches
难度：intermediate
子主题：Watches和Sessions

## 中文导读

本题要求你完成 `实现 One-Shot Watches用于Change Notification`。

重点关注：`watch`、`one-shot`、`WatchEvent`、`change notification`、`push-based`。

建议先按提示逐步实现：GetData(path, watch=true) registers a one-shot watch on the 节点。

协议字段、消息类型、输入输出格式请以本文件中的代码块和测试用例为准。

## 题目说明

Watches enable push-based notification when a ZNode changes. Instead of polling, clients register a watch和ZooKeeper notifies them when the 节点 is modified.

**Watch flow**:
1. 客户端 calls `GetData("/config", watch=true)` — receives current data AND registers a watch
2. When another 客户端 calls `SetData("/config", new_data, version)`
3. ZooKeeper sends a `WatchEvent(NodeDataChanged)` to the watching 客户端
4. The watch is removed (one-shot); 客户端 must re-register to watch again

**Watch events**:
- `NodeDataChanged`: 节点 data was modified
- `NodeDeleted`: 节点 was deleted
- `NodeChildrenChanged`: children were added or removed

```JSON
请求:  {"type": "znode_get_watch", "msg_id": 1, "path": "/config", "watch": true, "watcher_id": "w1"}
响应: {"type": "znode_get_watch_ok", "in_reply_to": 1, "data": "v1", "version": 0, "watch_registered": true}

Event:    {"type": "watch_event", "path": "/config", "event_type": "NodeDataChanged", "watcher_id": "w1"}
```

## 涉及概念

- `watch`
- `one-shot`
- `WatchEvent`
- `change notification`
- `push-based`

## 实现提示

- GetData(path, watch=true) registers a one-shot watch on the 节点
- When the 节点 data changes, the watcher receives a WatchEvent notification
- Watches are one-shot: they fire once, then are removed. 客户端 must re-register.
- Watch events: NodeDataChanged, NodeDeleted, NodeChildrenChanged
- Watches are ordered: the 客户端 always sees the watch event before the new data

## 测试用例

### 1. Register watch和receive event on change

znode_get_watch_ok should include data, version,和watch_registered: true.

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"znode_get_watch","msg_id":2,"path":"/cfg","watch":true,"watcher_id":"w1"}}
```

期望输出：

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

### 2. Watch fires on data change

After SetData, a watch_event，包含event_type NodeDataChanged should be sent to w1.

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"znode_create","msg_id":2,"path":"/w","data":"old","ephemeral":false,"sequential":false}}
{"src":"c1","dest":"n1","body":{"type":"znode_get_watch","msg_id":3,"path":"/w","watch":true,"watcher_id":"w1"}}
{"src":"c1","dest":"n1","body":{"type":"znode_set","msg_id":4,"path":"/w","data":"new","version":0}}
```

期望输出：

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

## 参考资料

- [ZooKeeper Watches](https://zookeeper.apache.org/doc/current/zookeeperProgrammers.html#ch_zkWatches)：ZooKeeper documentation on watches和notification semantics

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
