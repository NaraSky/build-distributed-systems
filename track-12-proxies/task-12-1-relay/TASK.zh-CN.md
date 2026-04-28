# 实现基础转发代理

英文标题：Implement Basic Relay Proxy
网页：<https://builddistributedsystem.com/tracks/proxies/tasks/task-12-1-relay>

课程：12. 代理
任务序号：1
短标题：转发代理
难度：入门
子主题：缓存代理

## 中文导读

这道题要求你实现一个最基础的转发代理（Relay Proxy）。代理是分布式系统中非常常见的组件，它位于客户端和服务端之间，负责接收客户端请求并转发给后端服务器，再把响应返回给客户端。掌握代理的工作原理是理解负载均衡、缓存、安全等高级功能的基础。

## 题目说明

构建一个基础的转发代理，将请求转发到后端服务器：

1. 监听客户端发来的请求
2. 解析请求，确定要转发到哪个后端服务器
3. 将请求转发给后端服务器
4. 等待后端服务器的响应
5. 将响应返回给客户端

需要妥善处理连接错误和超时的情况。

## 概念说明

### 什么是代理？

代理（Proxy）位于客户端和服务端之间，拦截并转发请求。通过代理，可以在不修改客户端或服务端代码的前提下，添加缓存、负载均衡、安全验证、日志记录等功能。你可以把代理想象成一个"中间人"——客户端把请求交给中间人，中间人再帮忙去找真正的服务端拿结果。

### 正向代理与反向代理

正向代理（Forward Proxy）代表客户端发起请求，例如公司防火墙后面的代理服务器。反向代理（Reverse Proxy）代表服务端接收请求，例如放在应用服务器前面的 NGINX。本题要构建的是一个反向代理。

## 涉及概念

- `proxy`
- `forwarding`
- `request handling`

## 实现提示

- 接收客户端发来的请求
- 将请求转发给后端服务器
- 将后端的响应返回给客户端

## 测试用例

### 1. 转发请求

代理将 GET /api/data 请求转发到后端，并把响应返回给客户端。

输入：

```json
{"src":"c0","dest":"proxy","body":{"type":"init","msg_id":1,"node_id":"proxy","node_ids":["proxy","backend"]}}
{"src":"client","dest":"proxy","body":{"type":"relay_request","msg_id":2,"path":"/api/data","method":"GET"}}
```

期望输出：

```text
{"src":"proxy","dest":"c0","body":{"type":"init_ok","in_reply_to":1,"msg_id":0}}
{"src":"proxy","dest":"client","body":{"type":"relay_response","in_reply_to":2,"msg_id":1,"status":200,"path":"/api/data"}}
```

## 参考资料

- [Proxy Patterns](https://en.wikipedia.org/wiki/Proxy_pattern)：代理设计模式概述

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
