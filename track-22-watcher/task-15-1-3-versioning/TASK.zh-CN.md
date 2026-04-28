# 实现 Optimistic Concurrency，包含Version Checks

英文标题：Implement Optimistic Concurrency，包含Version Checks
网页：<https://builddistributedsystem.com/tracks/watcher/tasks/task-15-1-3-versioning>

课程：22. 观察者：ZooKeeper/etcd 模型
任务序号：3
短标题：Version Checks
难度：intermediate
子主题：The ZNode Data模式l

## 中文导读

本题要求你完成 `实现 Optimistic Concurrency，包含Version Checks`。

重点关注：`optimistic concurrency`、`version check`、`BadVersion`、`compare-and-swap`、`conflict detection`。

建议先按提示逐步实现：SetData(path, data, version) only succeeds if current version == specified version。

协议字段、消息类型、输入输出格式请以本文件中的代码块和测试用例为准。

## 题目说明

ZooKeeper uses version-based optimistic concurrency control. Every `SetData`和`Delete` must specify the expected version. If the version does not match the current version, the operation fails，包含`BadVersion`.

**How it works**:
1. 客户端 reads ZNode: gets data和version (e.g., version=5)
2. 客户端 modifies the data locally
3. 客户端 sends `SetData(path, new_data, version=5)`
4. 服务端 checks: if current version == 5, apply update和set version=6
5. If another 客户端 updated between steps 1和3, the version is now 6,和the operation fails，包含`BadVersion`
6. The 客户端 must re-read (get version=6)和重试

This is the ZooKeeper equivalent of a **compare-and-swap** (CAS) operation.

```JSON
请求:  {"type": "znode_set", "msg_id": 1, "path": "/cfg", "data": "new", "version": 0}
响应: {"type": "znode_set_ok", "in_reply_to": 1, "new_version": 1}

请求:  {"type": "znode_set", "msg_id": 2, "path": "/cfg", "data": "newer", "version": 0}
响应: {"type": "error", "in_reply_to": 2, "code": "BadVersion", "text": "expected version 0, current version 1"}
```

## 涉及概念

- `optimistic concurrency`
- `version check`
- `BadVersion`
- `compare-and-swap`
- `conflict detection`

## 实现提示

- SetData(path, data, version) only succeeds if current version == specified version
- On success, version increments to version+1
- On version mismatch, return BadVersion error — the 客户端 must re-read和重试
- This is an optimistic concurrency control (OCC) mechanism — no locks needed
- version=-1 is a wildcard that bypasses the version check

## 测试用例

### 1. Correct version allows update

znode_set_ok should show new_version: 1.

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

### 2. Wrong version returns BadVersion

Second set，包含version 0 should return BadVersion error (current is now 1).

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

- [ZooKeeper Versioning](https://zookeeper.apache.org/doc/current/zookeeperProgrammers.html#sc_zkStatStructure)：ZooKeeper documentation on stat structure和version-based CAS

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
