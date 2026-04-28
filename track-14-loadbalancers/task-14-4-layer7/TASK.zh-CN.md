# 构建七层负载均衡器

英文标题：Build Layer 7 Load Balancer
网页：<https://builddistributedsystem.com/tracks/loadbalancers/tasks/task-14-4-layer7>

课程：14. 负载均衡器
任务序号：4
短标题：Layer 7 LB
难度：进阶
子主题：四层负载均衡

## 中文导读

本题要求你构建一个能理解 HTTP 协议的七层负载均衡器。四层负载均衡器只看 TCP/IP 信息来分发流量，就像一个只看信封地址的邮递员。而七层负载均衡器能"拆开信封"看懂 HTTP 请求的内容（比如请求的路径、域名等），从而做出更智能的路由决策。这是现代 Web 架构中非常核心的能力。

协议字段、消息类型、输入输出格式请以本文件中的代码块和测试用例为准。

## 题目说明

构建一个能感知 HTTP 协议的七层负载均衡器：

1. 解析 HTTP 请求（方法、路径、请求头）
2. 根据 Host 请求头进行路由（虚拟主机）
3. 根据 URL 路径进行路由（比如 /api/* 路由到 API 服务器集群）
4. 通过 Cookie 实现会话粘性
5. 支持 URL 重写

七层负载均衡能够根据请求内容做出智能路由决策。

## 概念说明

### 四层与七层的区别

四层负载均衡器只能看到 TCP/UDP 层面的信息——速度快但功能有限。七层负载均衡器能理解 HTTP 协议——可以根据 URL 路由、读取 Cookie、修改请求头。功能更强大，但开销也更高。

### 会话粘性（Session Stickiness）

有些应用要求同一用户的所有请求都发送到同一台服务器（因为会话数据存在那台服务器的内存中）。负载均衡器可以通过 Cookie 或客户端 IP 来跟踪会话。需要注意的是：会话粘性可能导致负载分布不均。

## 涉及概念

- `Layer 7`
- `HTTP routing`
- `content-based`

## 实现提示

- 解析 HTTP 请求头
- 根据路径或 Host 头进行路由
- 支持会话粘性

## 测试用例

### 1. 基于路径的路由

七层负载均衡器配置了基于路径的路由规则：/api/* 路由到 [s1, s2]，/web/* 路由到 [s3]。发往 /api/users 的请求应该被路由到 s1 或 s2。

输入：

```json
{"src":"c0","dest":"lb","body":{"type":"init","msg_id":1,"node_id":"lb","node_ids":["lb","s1","s2","s3"]}}
{"src":"client","dest":"lb","body":{"type":"http_request","msg_id":2,"path":"/api/users","method":"GET"}}
```

期望输出：

```text
{"src":"lb","dest":"c0","body":{"type":"init_ok","in_reply_to":1,"msg_id":0}}
{"src":"lb","dest":"client","body":{"type":"http_response","in_reply_to":2,"msg_id":1,"path":"/api/users","routed_to":"s1","status":200}}
```

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
