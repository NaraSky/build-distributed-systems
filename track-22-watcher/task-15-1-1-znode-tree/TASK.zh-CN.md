# 实现 ZNode 树形数据模型

英文标题：Implement a ZNode Tree Data Model
网页：<https://builddistributedsystem.com/tracks/watcher/tasks/task-15-1-1-znode-tree>

课程：22. 观察者
任务序号：1
短标题：ZNode Tree
难度：进阶
子主题：ZNode 数据模型

## 中文导读

这道题要求你搭建一棵类似文件系统的树，树上的每个节点叫做 ZNode。你可以把它想象成一个精简版的文件夹结构：每个"文件夹"自身能存一小段数据，同时还能拥有若干子"文件夹"。在分布式系统中，这棵树不是用来存大文件的，而是用来存放配置信息、锁状态、领导者地址等协调用的小数据。理解这棵树的结构，是后续所有 ZooKeeper 操作的基础。

## 题目说明

ZNode（ZooKeeper 节点）数据模型是一种类似文件系统的层级结构，每个节点可以存储少量数据，上限约为 1MB。设计它的目的是存储分布式协调所需的元数据，而不是用来存放大量业务数据。

每个 ZNode 具有以下属性：

- **路径（Path）**：和文件系统路径一样，用斜杠分隔层级，例如 `/services/web/instance-1`。
- **数据（Data）**：一段任意的字节数组，通常很小，比如一条配置值或一个领导者的标识。
- **版本号（Version）**：一个从零开始的整数，每次数据被更新时自动加一，用于实现乐观锁。
- **子节点列表（Children）**：当前节点下所有直接子节点的名称。
- **临时标志（Ephemeral）**：如果设为真，当创建它的客户端会话断开后，该节点会被自动删除。
- **顺序标志（Sequential）**：如果设为真，创建时系统会在节点名称末尾追加一个 10 位的递增序列号，保证名称唯一。

协议示例：

```json
Request:  {"type": "znode_create", "msg_id": 1, "path": "/services", "data": "", "ephemeral": false, "sequential": false}
Response: {"type": "znode_create_ok", "in_reply_to": 1, "path": "/services", "version": 0}

Request:  {"type": "znode_get", "msg_id": 2, "path": "/services"}
Response: {"type": "znode_get_ok", "in_reply_to": 2, "path": "/services", "data": "", "version": 0, "children": [], "ephemeral": false}
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

- 每个 ZNode 就是树中的一个节点，通过路径来定位，和文件系统的目录结构类似
- 每个 ZNode 需要维护四项信息：路径、数据、版本号、子节点列表
- ZNode 有两个标志位：临时节点在会话过期后自动删除，顺序节点在创建时自动追加编号
- 根节点 `/` 始终存在，不允许被删除
- 版本号从 0 开始，每次修改数据时递增 1

## 测试用例

### 1. 创建并获取 ZNode

验证说明：获取刚创建的节点时，返回的数据应为 "config"，版本号应为 0。

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

### 2. 创建子节点

验证说明：获取父节点 /app 时，子节点列表中应包含 ["db"]。

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

- [ZooKeeper Data Model](https://zookeeper.apache.org/doc/current/zookeeperProgrammers.html#ch_zkDataModel)：ZooKeeper 官方文档中关于节点和层级命名空间的详细说明

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
