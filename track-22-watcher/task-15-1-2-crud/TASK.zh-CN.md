# 实现 ZNode CRUD Operations

英文标题：Implement ZNode CRUD Operations
网页：<https://builddistributedsystem.com/tracks/watcher/tasks/task-15-1-2-crud>

课程：22. 观察者：ZooKeeper/etcd 模型
任务序号：2
短标题：ZNode CRUD
难度：intermediate
子主题：The ZNode Data模式l

## 中文导读

本题要求你完成 `实现 ZNode CRUD Operations`。

重点关注：`Create`、`GetData`、`SetData`、`Delete`、`GetChildren`。

建议先按提示逐步实现：Create takes path, data,和flags (ephemeral, sequential)。

协议字段、消息类型、输入输出格式请以本文件中的代码块和测试用例为准。

## 题目说明

ZooKeeper provides five core operations用于manipulating ZNodes. Together they form a complete API用于coordination 元数据.

**Operations**:
- `Create(path, data, flags)`: create a new ZNode. Fails if it already exists.
- `GetData(path)`: return the data, version,和stat of a ZNode.
- `SetData(path, data, version)`: update the data. The version must match the current version (optimistic locking).
- `Delete(path, version)`: delete a ZNode. Version must match. Fails if the 节点 has children.
- `GetChildren(path)`: return the list of child 节点 names.

```JSON
请求:  {"type": "znode_set", "msg_id": 1, "path": "/config", "data": "new-value", "version": 0}
响应: {"type": "znode_set_ok", "in_reply_to": 1, "new_version": 1}

请求:  {"type": "znode_delete", "msg_id": 2, "path": "/config", "version": 1}
响应: {"type": "znode_delete_ok", "in_reply_to": 2}

请求:  {"type": "znode_children", "msg_id": 3, "path": "/services"}
响应: {"type": "znode_children_ok", "in_reply_to": 3, "children": ["web", "db", "缓存"]}
```

## 涉及概念

- `Create`
- `GetData`
- `SetData`
- `Delete`
- `GetChildren`

## 实现提示

- Create takes path, data,和flags (ephemeral, sequential)
- SetData和Delete require a version parameter用于optimistic concurrency
- GetChildren returns the list of child 节点 names (not full paths)
- Delete fails if the 节点 has children (must delete children first)
- All operations are atomic — no partial updates

## 测试用例

### 1. SetData updates version

znode_set_ok should show new_version: 1.

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"znode_create","msg_id":2,"path":"/cfg","data":"v1","ephemeral":false,"sequential":false}}
{"src":"c1","dest":"n1","body":{"type":"znode_set","msg_id":3,"path":"/cfg","data":"v2","version":0}}
```

期望输出：

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

### 2. Delete removes ZNode

After delete, znode_get should return NoNode error.

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"znode_create","msg_id":2,"path":"/tmp","data":"","ephemeral":false,"sequential":false}}
{"src":"c1","dest":"n1","body":{"type":"znode_delete","msg_id":3,"path":"/tmp","version":0}}
{"src":"c1","dest":"n1","body":{"type":"znode_get","msg_id":4,"path":"/tmp"}}
```

期望输出：

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

## 参考资料

- [ZooKeeper Operations](https://zookeeper.apache.org/doc/current/zookeeperProgrammers.html#ch_zkOperations)：ZooKeeper documentation on CRUD operations和versioning

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
