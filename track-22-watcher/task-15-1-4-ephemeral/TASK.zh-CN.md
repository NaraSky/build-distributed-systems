# 实现临时节点以关联会话生命周期

英文标题：Implement Ephemeral Nodes for Session-Bound State
网页：<https://builddistributedsystem.com/tracks/watcher/tasks/task-15-1-4-ephemeral>

课程：22. 观察者：ZooKeeper/etcd 模型
任务序号：4
短标题：Ephemeral Nodes
难度：进阶
子主题：The ZNode Data Model

## 中文导读

这道题要求你实现临时节点（Ephemeral Node）。临时节点的特点是"人走茶凉"：当创建它的客户端会话过期（比如客户端崩溃或断开连接），该节点就会被自动删除。这个特性是分布式服务注册和故障检测的基础，比如一个服务在 ZooKeeper 上注册了临时节点，当服务宕机后节点自动消失，其他服务立刻就能知道。

## 题目说明

临时节点（Ephemeral Node）是一种特殊的 ZNode，当创建它的客户端会话过期时会被自动删除。它们是分布式服务注册和故障检测的基础。

**生命周期**：
1. 客户端创建临时节点：`Create("/services/web/instance-1", data, EPHEMERAL)`
2. 客户端存活期间，通过心跳保持会话活跃
3. 如果客户端崩溃或断开连接，会话最终会过期
4. ZooKeeper 自动删除该会话创建的所有临时节点
5. 监听 `/services/web/` 的其他客户端会收到删除通知

**约束**：临时节点不能有子节点。

```json
Request:  {"type": "znode_create", "msg_id": 1, "path": "/services/web/i-001", "data": "host:8080", "ephemeral": true, "sequential": false, "session_id": "s1"}
Response: {"type": "znode_create_ok", "in_reply_to": 1, "path": "/services/web/i-001", "version": 0}

Request:  {"type": "session_expire", "msg_id": 2, "session_id": "s1"}
Response: {"type": "session_expire_ok", "in_reply_to": 2, "ephemeral_nodes_deleted": ["/services/web/i-001"]}
```

## 涉及概念

- `ephemeral node`
- `session lifetime`
- `service registration`
- `auto-deletion`
- `failure detection`

## 实现提示

- 临时节点在创建它的会话过期时会被自动删除
- 当服务端在会话超时时间内未收到心跳时，会话过期
- 临时节点不能有子节点（这是设计约束）
- 典型用例：服务注册一个临时节点，当服务崩溃后节点自动消失
- 这使得无需轮询就能实现自动故障检测

## 测试用例

### 1. 成功创建临时节点

znode_get_ok 应当显示 ephemeral: true 和 data 为 "host"。

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"znode_create","msg_id":2,"path":"/svc/i1","data":"host","ephemeral":true,"sequential":false,"session_id":"s1"}}
{"src":"c1","dest":"n1","body":{"type":"znode_get","msg_id":3,"path":"/svc/i1"}}
```

期望输出：

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

### 2. 会话过期时删除临时节点

session_expire_ok 应当在 ephemeral_nodes_deleted 中列出 /e。

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"znode_create","msg_id":2,"path":"/e","data":"","ephemeral":true,"sequential":false,"session_id":"s1"}}
{"src":"c1","dest":"n1","body":{"type":"session_expire","msg_id":3,"session_id":"s1"}}
```

期望输出：

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

## 参考资料

- [ZooKeeper Ephemeral Nodes](https://zookeeper.apache.org/doc/current/zookeeperProgrammers.html#Ephemeral+Nodes)：ZooKeeper 关于临时节点和会话管理的官方文档

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
