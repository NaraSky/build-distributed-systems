# 实现客户端会话管理

英文标题：Implement Client Session Management
网页：<https://builddistributedsystem.com/tracks/watcher/tasks/task-15-2-2-sessions>

课程：22. 观察者：ZooKeeper/etcd 模型
任务序号：7
短标题：Sessions
难度：进阶
子主题：Watches and Sessions

## 中文导读

这道题要求你实现 ZooKeeper 的客户端会话管理。会话是客户端与 ZooKeeper 之间的一条"生命线"：客户端通过定期发送心跳来维持会话，如果心跳中断超时，会话就会过期，该会话创建的临时节点会被自动删除，注册的监听器也会被移除。会话机制是临时节点和监听器正常工作的基础。

## 题目说明

每个 ZooKeeper 客户端都在一个会话（Session）内运行。会话追踪客户端是否存活，是临时节点生命周期和监听器事件投递的基础。

**会话的生命周期**：
1. 客户端连接后获得一个唯一的会话 ID
2. 客户端每隔 `tickTime`（默认 2 秒）发送一次心跳（ping）
3. 如果服务端在 `sessionTimeout`（默认 10 秒）内未收到心跳，会话过期
4. 会话过期时：该会话创建的临时节点被删除，注册的监听器被移除
5. 如果客户端在超时前重新连接，会话会保留，包括所有状态

```json
Request:  {"type": "session_create", "msg_id": 1, "timeout_ms": 10000}
Response: {"type": "session_create_ok", "in_reply_to": 1, "session_id": "s-001", "timeout_ms": 10000}

Request:  {"type": "session_heartbeat", "msg_id": 2, "session_id": "s-001"}
Response: {"type": "session_heartbeat_ok", "in_reply_to": 2, "session_id": "s-001", "remaining_ms": 10000}
```

## 涉及概念

- `session`
- `heartbeat`
- `session timeout`
- `session expiry`
- `reconnection`

## 实现提示

- 每个客户端在连接时被分配一个会话 ID
- 客户端每隔 tick_time（默认 2 秒）发送一次心跳
- 如果服务端在 session_timeout（默认 10 秒）内未收到心跳，会话过期
- 会话过期时：所有临时节点被删除，所有监听器被移除
- 客户端可以在超时窗口内重新连接，不会丢失会话

## 测试用例

### 1. 创建会话并返回会话 ID

session_create_ok 应当包含唯一的 session_id 和 timeout_ms。

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"session_create","msg_id":2,"timeout_ms":10000}}
```

期望输出：

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

### 2. 心跳延长会话

session_heartbeat_ok 应当显示 remaining_ms > 0。

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"session_create","msg_id":2,"timeout_ms":10000}}
{"src":"c1","dest":"n1","body":{"type":"session_heartbeat","msg_id":3,"session_id":"s-001"}}
```

期望输出：

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

## 参考资料

- [ZooKeeper Sessions](https://zookeeper.apache.org/doc/current/zookeeperProgrammers.html#ch_zkSessions)：ZooKeeper 关于会话管理和心跳的官方文档

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
