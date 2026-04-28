# 实现最少连接数算法

英文标题：Implement Least Connections Algorithm
网页：<https://builddistributedsystem.com/tracks/loadbalancers/tasks/task-14-2-least-connections>

课程：14. 负载均衡器
任务序号：2
短标题：Least Connections
难度：进阶
子主题：四层负载均衡

## 中文导读

本题要求你实现"最少连接数"负载均衡算法。与轮询不同，这种算法会把新请求分配给当前活跃连接数最少的服务器。这在请求处理时间差异较大的场景下特别有用——比如有的请求 10 毫秒就完成，有的却要好几秒，轮询会导致慢请求堆积在某台服务器上，而最少连接数算法能自动适应这种不均衡。

协议字段、消息类型、输入输出格式请以本文件中的代码块和测试用例为准。

## 题目说明

实现最少连接数负载均衡：

1. 为每台服务器跟踪当前的活跃连接数
2. 当一个请求开始时，将选中服务器的连接计数加一
3. 当一个请求完成时，将对应服务器的连接计数减一
4. 将新请求路由到活跃连接数最少的服务器

这种方式能自动适应不同请求的处理时长差异。

## 概念说明

### 最少连接数（Least Connections）

轮询在请求处理时间差异较大时会失效——耗时长的请求会堆积在某一台服务器上。最少连接数算法把请求路由到当前活跃请求最少的服务器，从而自然地平衡负载。

### 加权最少连接数（Weighted Least Connections）

将权重与连接数结合使用：选择"连接数 / 权重"比值最低的服务器。这样既考虑了当前负载，也考虑了服务器的处理能力。

## 涉及概念

- `least connections`
- `dynamic load`
- `connection tracking`

## 实现提示

- 为每台服务器维护活跃连接计数
- 请求开始时计数加一，请求完成时计数减一
- 选择连接数最少的服务器

## 测试用例

### 1. 按连接数均衡分配

负载均衡器有 3 个后端：s1（2 个活跃连接）、s2（5 个连接）、s3（1 个连接）。新请求到达时，验证它被路由到 s3（连接数最少）。请求完成后，连接计数应相应减少。

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
