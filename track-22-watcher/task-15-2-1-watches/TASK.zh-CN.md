# 实现一次性监听器以获取变更通知

英文标题：Implement One-Shot Watches for Change Notification
网页：<https://builddistributedsystem.com/tracks/watcher/tasks/task-15-2-1-watches>

课程：22. 观察者：ZooKeeper/etcd 模型
任务序号：6
短标题：Watches
难度：进阶
子主题：Watches and Sessions

## 中文导读

这道题要求你实现 ZooKeeper 的监听器（Watch）机制。监听器让客户端不用反复轮询就能知道数据何时发生了变化。客户端在读取数据时注册一个监听器，当数据变化时 ZooKeeper 会主动推送通知。需要注意的是，ZooKeeper 的监听器是一次性的：触发一次后就失效了，需要重新注册。

## 题目说明

监听器（Watch）让客户端能够在 ZNode 发生变化时收到推送通知。客户端不需要轮询，只需注册一个监听器，当节点被修改时 ZooKeeper 就会主动通知。

**监听器的工作流程**：
1. 客户端调用 `GetData("/config", watch=true)`，获得当前数据的同时注册一个监听器
2. 当另一个客户端调用 `SetData("/config", new_data, version)` 时
3. ZooKeeper 向监听的客户端发送一个 `WatchEvent(NodeDataChanged)` 事件
4. 监听器被移除（一次性的）；客户端如果想继续监听，必须重新注册

**监听事件类型**：
- `NodeDataChanged`：节点数据被修改
- `NodeDeleted`：节点被删除
- `NodeChildrenChanged`：子节点被添加或移除

```json
Request:  {"type": "znode_get_watch", "msg_id": 1, "path": "/config", "watch": true, "watcher_id": "w1"}
Response: {"type": "znode_get_watch_ok", "in_reply_to": 1, "data": "v1", "version": 0, "watch_registered": true}

Event:    {"type": "watch_event", "path": "/config", "event_type": "NodeDataChanged", "watcher_id": "w1"}
```

## 涉及概念

- `watch`
- `one-shot`
- `WatchEvent`
- `change notification`
- `push-based`

## 实现提示

- GetData(path, watch=true) 在节点上注册一个一次性监听器
- 当节点数据变化时，监听者会收到一个 WatchEvent 通知
- 监听器是一次性的：触发一次后就被移除，客户端需要重新注册
- 监听事件类型：NodeDataChanged、NodeDeleted、NodeChildrenChanged
- 监听器是有序的：客户端总是先看到监听事件，再看到新数据

## 测试用例

### 1. 注册监听器并在变更时收到事件

znode_get_watch_ok 应当包含 data、version 和 watch_registered: true。

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"znode_get_watch","msg_id":2,"path":"/cfg","watch":true,"watcher_id":"w1"}}
```

期望输出：

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

### 2. 数据变更触发监听事件

执行 SetData 后，应当向 w1 发送一个 event_type 为 NodeDataChanged 的 watch_event。

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

- [ZooKeeper Watches](https://zookeeper.apache.org/doc/current/zookeeperProgrammers.html#ch_zkWatches)：ZooKeeper 关于监听器和通知语义的官方文档

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
