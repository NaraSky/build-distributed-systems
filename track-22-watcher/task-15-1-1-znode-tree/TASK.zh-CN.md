# 实现 a ZNode Tree Data模式l

英文标题：Implement a ZNode Tree Data模式l
网页：<https://builddistributedsystem.com/tracks/watcher/tasks/task-15-1-1-znode-tree>

课程：22. 观察者：ZooKeeper/etcd 模型
任务序号：1
短标题：ZNode Tree
难度：intermediate
子主题：The ZNode Data模式l

## 中文导读

本题要求你完成 `实现 a ZNode Tree Data模式l`。

重点关注：`ZNode`、`hierarchical tree`、`path`、`data`、`version`。

建议先按提示逐步实现：A ZNode is a 节点 in a tree, similar to a filesystem path (e.g., /services/web/instance-1)。

协议字段、消息类型、输入输出格式请以本文件中的代码块和测试用例为准。

## 题目说明

The ZNode data model is a filesystem-like hierarchy where each 节点 stores a small amount of data (up to 1MB). ZNodes are designed用于coordination 元数据, not bulk data 存储.

**ZNode properties**:
- `path`: filesystem-like path (e.g., `/services/web/instance-1`)
- `data`: arbitrary byte array (typically small: config values, Leader IDs)
- `version`: monotonically increasing integer, incremented on every data update
- `children`: list of child 节点 names
- `ephemeral`: if true, 节点 is auto-deleted when the creating session expires
- `sequential`: if true, ZooKeeper appends a 10-digit sequence number to the 节点 name

```JSON
请求:  {"type": "znode_create", "msg_id": 1, "path": "/services", "data": "", "ephemeral": false, "sequential": false}
响应: {"type": "znode_create_ok", "in_reply_to": 1, "path": "/services", "version": 0}

请求:  {"type": "znode_get", "msg_id": 2, "path": "/services"}
响应: {"type": "znode_get_ok", "in_reply_to": 2, "path": "/services", "data": "", "version": 0, "children": [], "ephemeral": false}
```

## 涉及概念

- `ZNode`
- `hierarchical tree`
- `path`
- `data`
- `version`
- `ephemeral`
- `sequential`

## 实现提示

- A ZNode is a 节点 in a tree, similar to a filesystem path (e.g., /services/web/instance-1)
- Each ZNode stores: path, data (byte array), version (integer), children list
- ZNodes have flags: ephemeral (deleted when session expires)和sequential (auto-numbered)
- The root ZNode "/" always exists和cannot be deleted
- Version starts at 0和increments on every data update

## 测试用例

### 1. 创建和get ZNode

znode_get_ok should return data "config"和version 0.

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"znode_create","msg_id":2,"path":"/app","data":"config","ephemeral":false,"sequential":false}}
{"src":"c1","dest":"n1","body":{"type":"znode_get","msg_id":3,"path":"/app"}}
```

期望输出：

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

### 2. 创建 child nodes

znode_get_ok用于/app should show ["db"] in children.

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"znode_create","msg_id":2,"path":"/app","data":"","ephemeral":false,"sequential":false}}
{"src":"c1","dest":"n1","body":{"type":"znode_create","msg_id":3,"path":"/app/db","data":"mysql","ephemeral":false,"sequential":false}}
{"src":"c1","dest":"n1","body":{"type":"znode_get","msg_id":4,"path":"/app"}}
```

期望输出：

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

## 参考资料

- [ZooKeeper Data模式l](https://zookeeper.apache.org/doc/current/zookeeperProgrammers.html#ch_zkDataModel)：ZooKeeper documentation on znodes和the hierarchical namespace

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
