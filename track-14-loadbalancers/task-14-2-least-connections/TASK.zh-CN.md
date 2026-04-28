# 实现 Least Connections Algorithm

英文标题：Implement Least Connections Algorithm
网页：<https://builddistributedsystem.com/tracks/loadbalancers/tasks/task-14-2-least-connections>

课程：14. 负载均衡器
任务序号：2
短标题：Least Connections
难度：intermediate
子主题：Layer 4 Load Balancing

## 中文导读

本题要求你完成 `实现 Least Connections Algorithm`。

重点关注：`least connections`、`dynamic load`、`connection tracking`。

建议先按提示逐步实现：Track active connections per 服务端。

协议字段、消息类型、输入输出格式请以本文件中的代码块和测试用例为准。

## 题目说明

Implement least-connections load balancing:

1. Track active connection count用于each 服务端
2. When a 请求 starts, increment count用于chosen 服务端
3. When a 请求 completes, decrement count
4. Route new requests to 服务端，包含fewest connections

This adapts to varying 请求 durations automatically.

## 概念说明

### Least Connections

Round robin fails when requests have varying durations - slow requests can pile up on one 服务端. Least connections routes to the 服务端，包含fewest active requests, naturally balancing load.

### Weighted Least Connections

Combine weights，包含connection counts: select 服务端，包含lowest (connections / weight) ratio. This accounts用于both current load和服务端 capacity.

## 涉及概念

- `least connections`
- `dynamic load`
- `connection tracking`

## 实现提示

- Track active connections per 服务端
- Increment on 请求, decrement on complete
- Select 服务端，包含fewest connections

## 测试用例

### 1. Balance by connections

Load balancer，包含3 backends: s1 (2 active connections), s2 (5 connections), s3 (1 connection). New 请求 arrives. Verify it routes to s3 (fewest connections). After 请求 completes, connection count decreases.

输入：

```json
{"src":"c0","dest":"lb","body":{"type":"init","msg_id":1,"node_id":"lb","node_ids":["lb","s1","s2","s3"]}}
{"src":"c1","dest":"lb","body":{"type":"set_connections","msg_id":2,"server":"s1","count":2}}
{"src":"c2","dest":"lb","body":{"type":"set_connections","msg_id":3,"server":"s2","count":5}}
{"src":"c3","dest":"lb","body":{"type":"set_connections","msg_id":4,"server":"s3","count":1}}
{"src":"c4","dest":"lb","body":{"type":"route_request","msg_id":5}}
```

期望输出：

```text
{"src": "lb", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
{"src": "lb", "dest": "c1", "body": {"type": "set_connections_ok", "in_reply_to": 2, "msg_id": 1}}
{"src": "lb", "dest": "c2", "body": {"type": "set_connections_ok", "in_reply_to": 3, "msg_id": 2}}
{"src": "lb", "dest": "c3", "body": {"type": "set_connections_ok", "in_reply_to": 4, "msg_id": 3}}
{"src": "lb", "dest": "c4", "body": {"type": "route_request_ok", "server": "s1", "in_reply_to": 5, "msg_id": 4}}
```

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
