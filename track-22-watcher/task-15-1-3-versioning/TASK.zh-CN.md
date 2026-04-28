# 实现基于版本号的乐观并发控制

英文标题：Implement Optimistic Concurrency with Version Checks
网页：<https://builddistributedsystem.com/tracks/watcher/tasks/task-15-1-3-versioning>

课程：22. 观察者：ZooKeeper/etcd 模型
任务序号：3
短标题：Version Checks
难度：进阶
子主题：The ZNode Data Model

## 中文导读

这道题要求你实现基于版本号的乐观并发控制。简单来说，就是"先读后写，写的时候检查版本号有没有变"。如果在你读和写之间，别人已经改过这个节点了，你的写操作就会失败，你需要重新读取再重试。这就是 ZooKeeper 版的比较并交换（CAS）操作。

## 题目说明

ZooKeeper 使用基于版本号的乐观并发控制。每次执行 `SetData` 和 `Delete` 操作时都必须指定期望的版本号。如果版本号与当前版本不匹配，操作会失败并返回 `BadVersion` 错误。

**工作原理**：
1. 客户端读取 ZNode：获得数据和版本号（例如 version=5）
2. 客户端在本地修改数据
3. 客户端发送 `SetData(path, new_data, version=5)`
4. 服务端检查：如果当前版本 == 5，则执行更新并将版本号设为 6
5. 如果在第 1 步和第 3 步之间有其他客户端更新了数据，版本号已变为 6，操作会失败并返回 `BadVersion`
6. 客户端需要重新读取（获得 version=6）再重试

这就是 ZooKeeper 中的**比较并交换（CAS）**操作。

```json
Request:  {"type": "znode_set", "msg_id": 1, "path": "/cfg", "data": "new", "version": 0}
Response: {"type": "znode_set_ok", "in_reply_to": 1, "new_version": 1}

Request:  {"type": "znode_set", "msg_id": 2, "path": "/cfg", "data": "newer", "version": 0}
Response: {"type": "error", "in_reply_to": 2, "code": "BadVersion", "text": "expected version 0, current version 1"}
```

## 涉及概念

- `optimistic concurrency`
- `version check`
- `BadVersion`
- `compare-and-swap`
- `conflict detection`

## 实现提示

- SetData(path, data, version) 只有在当前版本号等于指定版本号时才会成功
- 成功时，版本号递增为 version+1
- 版本号不匹配时，返回 BadVersion 错误，客户端需要重新读取并重试
- 这是乐观并发控制（OCC）机制，不需要加锁
- version=-1 是通配符，跳过版本检查

## 测试用例

### 1. 正确的版本号允许更新

znode_set_ok 应当显示 new_version: 1。

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"znode_create","msg_id":2,"path":"/v","data":"a","ephemeral":false,"sequential":false}}
{"src":"c1","dest":"n1","body":{"type":"znode_set","msg_id":3,"path":"/v","data":"b","version":0}}
```

期望输出：

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

### 2. 错误的版本号返回 BadVersion

第二次使用 version 0 进行更新应当返回 BadVersion 错误（当前版本已经是 1）。

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"znode_create","msg_id":2,"path":"/v","data":"a","ephemeral":false,"sequential":false}}
{"src":"c1","dest":"n1","body":{"type":"znode_set","msg_id":3,"path":"/v","data":"b","version":0}}
{"src":"c1","dest":"n1","body":{"type":"znode_set","msg_id":4,"path":"/v","data":"c","version":0}}
```

期望输出：

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

## 参考资料

- [ZooKeeper Versioning](https://zookeeper.apache.org/doc/current/zookeeperProgrammers.html#sc_zkStatStructure)：ZooKeeper 关于状态结构和基于版本号的 CAS 机制的官方文档

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
