# 实现带可配置积压队列的连接池

英文标题：Add a Connection Pool with Configurable Backlog
网页：<https://builddistributedsystem.com/tracks/networker/tasks/task-5-1-2-connection-pool>

课程：17. 网络器：TCP 与协议基础
任务序号：2
短标题：连接池
难度：进阶
子主题：从零实现 TCP

## 中文导读

这道题让你在 TCP 服务器的基础上增加连接池（Connection Pool）功能。想象一个餐厅只有 N 个座位，坐满后新来的客人要在门口排队；如果队伍也排满了，就只能拒绝入场。连接池的工作原理与此类似，它能帮助服务器在高并发场景下有序地管理有限的连接资源。

## 题目说明

扩展你的 TCP 服务器，使其最多同时接受 N 个并发连接。当活跃连接数超过 N 时，将新连接放入积压队列（Backlog）中等待。如果积压队列也满了，则拒绝该连接。

实现以下消息处理器：

```json
Request:  {"type": "pool_config", "msg_id": 1, "max_connections": 3, "backlog_size": 5}
Response: {"type": "pool_config_ok", "in_reply_to": 1}

Request:  {"type": "pool_connect", "msg_id": 2, "client_id": "c1"}
Response: {"type": "pool_connect_ok", "in_reply_to": 2, "status": "connected", "active": 1, "queued": 0}

Request:  {"type": "pool_connect", "msg_id": 5, "client_id": "c4"}
Response: {"type": "pool_connect_ok", "in_reply_to": 5, "status": "queued", "active": 3, "queued": 1}

Request:  {"type": "pool_disconnect", "msg_id": 6, "client_id": "c1"}
Response: {"type": "pool_disconnect_ok", "in_reply_to": 6, "promoted": "c4", "active": 3, "queued": 0}
```

## 涉及概念

- `connection pool`
- `backlog`
- `concurrency`
- `resource management`

## 实现提示

- 使用计数器跟踪当前活跃连接数
- 当达到最大连接数时，将新连接放入队列或直接拒绝
- 积压队列的大小应可配置
- 当连接关闭时，递减计数器，并将队列中等待的连接提升为活跃连接
- 注意处理队列本身也满了的情况

## 测试用例

### 1. 配置连接池并建立连接

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"pool_config","msg_id":2,"max_connections":2,"backlog_size":3}}
{"src":"c1","dest":"n1","body":{"type":"pool_connect","msg_id":3,"client_id":"c1"}}
```

期望输出：

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
{"src": "n1", "dest": "c1", "body": {"type": "pool_config_ok", "in_reply_to": 2, "msg_id": 1}}
{"src": "n1", "dest": "c1", "body": {"type": "pool_connect_ok", "in_reply_to": 3, "status": "connected", "active": 1, "queued": 0, "msg_id": 2}}
```

### 2. 超出最大连接数后进入队列

验证说明：第三个 pool_connect_ok 应显示 status: queued、active: 2、queued: 1。

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"pool_config","msg_id":2,"max_connections":2,"backlog_size":3}}
{"src":"c1","dest":"n1","body":{"type":"pool_connect","msg_id":3,"client_id":"c1"}}
{"src":"c1","dest":"n1","body":{"type":"pool_connect","msg_id":4,"client_id":"c2"}}
{"src":"c1","dest":"n1","body":{"type":"pool_connect","msg_id":5,"client_id":"c3"}}
```

期望输出：

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

## 参考资料

- [TCP Backlog and Connection Queuing](https://veithen.io/2014/01/01/how-tcp-backlog-works-in-linux.html)：深入讲解 Linux 中 TCP 积压队列的工作原理

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
