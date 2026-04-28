# 实现轮询负载均衡器

英文标题：Implement Round Robin Load Balancer
网页：<https://builddistributedsystem.com/tracks/loadbalancers/tasks/task-14-1-round-robin>

课程：14. 负载均衡器
任务序号：1
短标题：Round Robin
难度：入门
子主题：四层负载均衡

## 中文导读

本题要求你实现最基础的负载均衡算法——轮询（Round Robin）。轮询的核心思想很简单：按顺序把请求依次分配给每台后端服务器，分完一轮后再从头开始。这是理解所有负载均衡算法的起点，掌握它之后再学习更复杂的策略会容易很多。

协议字段、消息类型、输入输出格式请以本文件中的代码块和测试用例为准。

## 题目说明

实现轮询负载均衡：

1. 维护一个后端服务器的有序列表
2. 记录当前服务器的索引位置
3. 每收到一个请求，就把它发送到当前索引对应的服务器
4. 索引加一，到达列表末尾时回绕到 0

当所有请求的处理开销差不多时，轮询可以均匀地分配负载。

## 概念说明

### 轮询（Round Robin）

轮询是最简单的负载均衡算法。请求按顺序在服务器之间循环分配：1、2、3、1、2、3……当所有服务器配置相同，且请求的处理成本接近时，轮询的效果最好。

### 加权轮询（Weighted Round Robin）

当服务器的处理能力不同时，可以使用加权轮询，按比例给性能更强的服务器分配更多请求。例如，权重为 3 的服务器每轮会被分配 3 次请求，而权重为 1 的服务器只分配 1 次。

## 涉及概念

- `round robin`
- `load balancing`
- `stateless`

## 实现提示

- 记录当前在服务器列表中的位置
- 每次请求后递增索引，到达末尾时回绕到起始位置
- 处理服务器列表为空的情况

## 测试用例

### 1. 均匀分配

负载均衡器有 3 个后端（s1、s2、s3）。发送 6 个请求，验证轮询是否均匀分配：请求1 发往 s1，请求2 发往 s2，请求3 发往 s3，请求4 发往 s1，请求5 发往 s2，请求6 发往 s3。每个后端恰好收到 2 个请求。

输入：

```json
{"src":"c0","dest":"lb","body":{"type":"init","msg_id":1,"node_id":"lb","node_ids":["lb","s1","s2","s3"]}}
{"src":"c1","dest":"lb","body":{"type":"add_servers","msg_id":2,"servers":["s1","s2","s3"]}}
{"src":"c2","dest":"lb","body":{"type":"get_server","msg_id":3}}
{"src":"c3","dest":"lb","body":{"type":"get_server","msg_id":4}}
{"src":"c4","dest":"lb","body":{"type":"get_server","msg_id":5}}
```

期望输出：

```text
{"src": "lb", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
{"src": "lb", "dest": "c1", "body": {"type": "add_servers_ok", "servers": ["s1", "s2", "s3"], "in_reply_to": 2, "msg_id": 1}}
{"src": "lb", "dest": "c2", "body": {"type": "get_server_ok", "server": "s1", "in_reply_to": 3, "msg_id": 2}}
{"src": "lb", "dest": "c3", "body": {"type": "get_server_ok", "server": "s2", "in_reply_to": 4, "msg_id": 3}}
{"src": "lb", "dest": "c4", "body": {"type": "get_server_ok", "server": "s3", "in_reply_to": 5, "msg_id": 4}}
```

### 2. 索引回绕

负载均衡器有 2 个后端（s1、s2）。发送 5 个请求，验证计数器是否正确回绕：请求1 发往 s1，请求2 发往 s2，请求3 发往 s1（回绕），请求4 发往 s2，请求5 发往 s1。索引到达服务器列表末尾后应重置为 0。

输入：

```json
{"src":"c0","dest":"lb","body":{"type":"init","msg_id":1,"node_id":"lb","node_ids":["lb","s1","s2"]}}
{"src":"c1","dest":"lb","body":{"type":"add_servers","msg_id":2,"servers":["s1","s2"]}}
{"src":"c2","dest":"lb","body":{"type":"get_server","msg_id":3}}
{"src":"c3","dest":"lb","body":{"type":"get_server","msg_id":4}}
{"src":"c4","dest":"lb","body":{"type":"get_server","msg_id":5}}
```

期望输出：

```text
{"src": "lb", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
{"src": "lb", "dest": "c1", "body": {"type": "add_servers_ok", "servers": ["s1", "s2"], "in_reply_to": 2, "msg_id": 1}}
{"src": "lb", "dest": "c2", "body": {"type": "get_server_ok", "server": "s1", "in_reply_to": 3, "msg_id": 2}}
{"src": "lb", "dest": "c3", "body": {"type": "get_server_ok", "server": "s2", "in_reply_to": 4, "msg_id": 3}}
{"src": "lb", "dest": "c4", "body": {"type": "get_server_ok", "server": "s1", "in_reply_to": 5, "msg_id": 4}}
```

## 参考资料

- [Load Balancing Algorithms](https://www.nginx.com/blog/choosing-nginx-plus-load-balancing-techniques/)：关于负载均衡技术的入门指南

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
