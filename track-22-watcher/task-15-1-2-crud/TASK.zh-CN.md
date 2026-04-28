# 实现 ZNode 的增删改查操作

英文标题：Implement ZNode CRUD Operations
网页：<https://builddistributedsystem.com/tracks/watcher/tasks/task-15-1-2-crud>

课程：22. 观察者
任务序号：2
短标题：ZNode CRUD
难度：进阶
子主题：ZNode 数据模型

## 中文导读

上一题搭好了 ZNode 树的骨架，这道题要求你为它实现完整的增删改查接口。ZooKeeper 一共提供五个核心操作，它们组合起来就能完成所有的协调元数据管理。值得注意的是，更新和删除都必须带上版本号——这是一种乐观锁机制，防止多个客户端同时改同一个节点时互相覆盖。

## 题目说明

ZooKeeper 提供五个核心操作来管理 ZNode，它们共同构成了一套完整的协调元数据接口：

- **创建（Create）**：在指定路径创建新节点，需要提供路径、数据和标志位。如果该路径已经存在，则操作失败。
- **读取数据（GetData）**：返回指定节点的数据、版本号和状态信息。
- **更新数据（SetData）**：修改节点的数据。调用时必须提供版本号，且该版本号必须与节点当前版本一致，否则操作失败。这就是乐观锁（Optimistic Locking）的工作方式——先读取版本号，再带着版本号去更新，如果期间别人改过了，版本号就对不上，更新就会被拒绝。
- **删除（Delete）**：删除一个节点。同样需要版本号匹配。此外，如果该节点下还有子节点，删除也会失败，必须先把子节点都删掉。
- **获取子节点（GetChildren）**：返回指定节点下所有直接子节点的名称列表（注意是名称而非完整路径）。

协议示例：

```json
Request:  {"type": "znode_set", "msg_id": 1, "path": "/config", "data": "new-value", "version": 0}
Response: {"type": "znode_set_ok", "in_reply_to": 1, "new_version": 1}

Request:  {"type": "znode_delete", "msg_id": 2, "path": "/config", "version": 1}
Response: {"type": "znode_delete_ok", "in_reply_to": 2}

Request:  {"type": "znode_children", "msg_id": 3, "path": "/services"}
Response: {"type": "znode_children_ok", "in_reply_to": 3, "children": ["web", "db", "cache"]}
```

## 涉及概念

- `Create`
- `GetData`
- `SetData`
- `Delete`
- `GetChildren`

## 实现提示

- 创建操作需要路径、数据以及标志位（临时、顺序）
- 更新和删除操作都需要携带版本号参数，用于乐观并发控制
- 获取子节点返回的是子节点的名称，不是完整路径
- 当节点还有子节点时，删除操作会失败——必须先递归删除所有子节点
- 所有操作都是原子性的，不会出现"改了一半"的情况

## 测试用例

### 1. 更新数据后版本号递增

验证说明：执行更新后，返回的新版本号应为 1。

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

### 2. 删除操作移除节点

验证说明：删除节点后再尝试读取，应返回"节点不存在"的错误。

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

- [ZooKeeper Operations](https://zookeeper.apache.org/doc/current/zookeeperProgrammers.html#ch_zkOperations)：ZooKeeper 官方文档中关于增删改查操作及版本控制的详细说明

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
