# 实现 Ephemeral Nodes用于Session-Bound State

英文标题：Implement Ephemeral Nodes用于Session-Bound State
网页：<https://builddistributedsystem.com/tracks/watcher/tasks/task-15-1-4-ephemeral>

课程：22. 观察者：ZooKeeper/etcd 模型
任务序号：4
短标题：Ephemeral Nodes
难度：intermediate
子主题：The ZNode Data模式l

## 中文导读

本题要求你完成 `实现 Ephemeral Nodes用于Session-Bound State`。

重点关注：`ephemeral node`、`session lifetime`、`service registration`、`auto-deletion`、`failure detection`。

建议先按提示逐步实现：Ephemeral 节点 are automatically deleted when the creating session expires。

协议字段、消息类型、输入输出格式请以本文件中的代码块和测试用例为准。

## 题目说明

Ephemeral 节点 are ZNodes that are automatically deleted when the 客户端 session that created them expires. They are the foundation of distributed service registration和故障 detection.

**Lifecycle**:
1. 客户端 creates ephemeral 节点: `Create("/services/web/instance-1", data, EPHEMERAL)`
2. While the 客户端 is alive, it sends heartbeats to keep the session active
3. If the 客户端 crashes or disconnects, the session eventually expires
4. ZooKeeper automatically deletes all ephemeral 节点 created by that session
5. Other clients watching `/services/web/` are notified of the deletion

**Constraints**: ephemeral 节点 cannot have children.

```JSON
请求:  {"type": "znode_create", "msg_id": 1, "path": "/services/web/i-001", "data": "host:8080", "ephemeral": true, "sequential": false, "session_id": "s1"}
响应: {"type": "znode_create_ok", "in_reply_to": 1, "path": "/services/web/i-001", "version": 0}

请求:  {"type": "session_expire", "msg_id": 2, "session_id": "s1"}
响应: {"type": "session_expire_ok", "in_reply_to": 2, "ephemeral_nodes_deleted": ["/services/web/i-001"]}
```

## 涉及概念

- `ephemeral node`
- `session lifetime`
- `service registration`
- `auto-deletion`
- `failure detection`

## 实现提示

- Ephemeral 节点 are automatically deleted when the creating session expires
- A session expires when the 服务端 misses heartbeats用于the session 超时 period
- Ephemeral 节点 cannot have children (design constraint)
- Use case: service registers an ephemeral 节点; when the service crashes, the 节点 disappears
- This enables automatic 故障 detection without polling

## 测试用例

### 1. Ephemeral node is created

znode_get_ok should show ephemeral: true和data "host".

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

### 2. Session expiry deletes ephemeral nodes

session_expire_ok should list /e in ephemeral_nodes_deleted.

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

- [ZooKeeper Ephemeral Nodes](https://zookeeper.apache.org/doc/current/zookeeperProgrammers.html#Ephemeral+Nodes)：ZooKeeper documentation on ephemeral 节点和session management

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
