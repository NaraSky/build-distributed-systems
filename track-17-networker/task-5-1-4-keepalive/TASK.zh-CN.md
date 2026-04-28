# 实现应用层 TCP 保活检测

英文标题：Implement Application-Level TCP Keep-Alive
网页：<https://builddistributedsystem.com/tracks/networker/tasks/task-5-1-4-keepalive>

课程：17. 网络器：TCP 与协议基础
任务序号：4
短标题：TCP 保活机制
难度：进阶
子主题：从零实现 TCP

## 中文导读

这道题让你实现应用层的 TCP 保活（Keep-Alive）检测机制。网络连接有时会"悄悄断开"，比如客户端崩溃或网线被拔掉，服务器端却毫不知情，连接资源白白浪费。保活机制就像定时"敲门"确认对方还在不在：如果客户端超过一定时间没有任何活动，服务器就主动发送探测消息；如果对方没有回应，就判定连接已失效并关闭它。

## 题目说明

实现应用层的 TCP 保活检测。如果一个客户端超过 30 秒没有任何通信，检测到这个情况并关闭连接。使用定期发送的探测消息（Ping）来代替操作系统层面的保活机制。

实现以下消息处理器：

```json
Request:  {"type": "ka_register", "msg_id": 1, "client_id": "c1", "timeout_ms": 30000, "ping_interval_ms": 10000}
Response: {"type": "ka_register_ok", "in_reply_to": 1}

Request:  {"type": "ka_heartbeat", "msg_id": 2, "client_id": "c1"}
Response: {"type": "ka_heartbeat_ok", "in_reply_to": 2, "last_seen_ms_ago": 0}

Request:  {"type": "ka_check", "msg_id": 3, "current_time_ms": 45000}
Response: {"type": "ka_check_ok", "in_reply_to": 3, "expired": ["c1"], "active": ["c2"]}

Request:  {"type": "ka_status", "msg_id": 4}
Response: {"type": "ka_status_ok", "in_reply_to": 4, "connections": [
    {"client_id": "c2", "last_seen_ms_ago": 5000, "status": "active"}
]}
```

## 涉及概念

- `keep-alive`
- `heartbeat`
- `connection health`
- `idle detection`

## 实现提示

- 定期发送探测消息来检测静默失败的客户端
- 为每个连接记录最后一次活动的时间戳
- 如果超过 30 秒没有活动，发送一个探测消息；如果 5 秒内没有收到回应，则关闭连接
- 不要依赖操作系统层面的保活机制，需要在应用层自行实现
- 维护一个连接状态表，记录每个连接的最后活跃时间

## 测试用例

### 1. 注册客户端的保活监控

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"ka_register","msg_id":2,"client_id":"c1","timeout_ms":30000,"ping_interval_ms":10000}}
```

期望输出：

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
{"src": "n1", "dest": "c1", "body": {"type": "ka_register_ok", "in_reply_to": 2, "msg_id": 1}}
```

### 2. 心跳重置最后活跃时间

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"ka_register","msg_id":2,"client_id":"c1","timeout_ms":30000,"ping_interval_ms":10000}}
{"src":"c1","dest":"n1","body":{"type":"ka_heartbeat","msg_id":3,"client_id":"c1"}}
```

期望输出：

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
{"src": "n1", "dest": "c1", "body": {"type": "ka_register_ok", "in_reply_to": 2, "msg_id": 1}}
{"src": "n1", "dest": "c1", "body": {"type": "ka_heartbeat_ok", "in_reply_to": 3, "last_seen_ms_ago": 0, "msg_id": 2}}
```

## 参考资料

- [TCP Keep-Alive in Detail](https://tldp.org/HOWTO/TCP-Keepalive-HOWTO/)：详细讲解操作系统层面和应用层面的 TCP 保活机制

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
