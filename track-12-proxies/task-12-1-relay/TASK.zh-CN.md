# 实现 基础 Relay 代理

英文标题：Implement Basic Relay Proxy
网页：<https://builddistributedsystem.com/tracks/proxies/tasks/task-12-1-relay>

课程：12. 代理
任务序号：1
短标题：Relay 代理
难度：beginner
子主题：Caching 代理

## 中文导读

本题要求你完成 `实现 基础 Relay 代理`。

重点关注：`proxy`、`forwarding`、`request handling`。

建议先按提示逐步实现：Accept incoming requests。

协议字段、消息类型、输入输出格式请以本文件中的代码块和测试用例为准。

## 题目说明

Build a basic relay 代理 that forwards requests to a backend 服务端:

1. Listen用于incoming 客户端 requests
2. Parse the 请求 to determine backend destination
3. Forward the 请求 to the backend
4. Wait用于the backend 响应
5. Return the 响应 to the 客户端

Handle connection errors和timeouts gracefully.

## 概念说明

### What is a 代理?

A 代理 sits between clients和servers, intercepting和forwarding requests. Proxies can add functionality like caching, load balancing, security,和logging without modifying 客户端 or 服务端 code.

### Forward vs Reverse 代理

A forward 代理 acts on behalf of clients (e.g., corporate firewall). A reverse 代理 acts on behalf of servers (e.g., NGINX in front of application servers). We will build a reverse 代理.

## 涉及概念

- `proxy`
- `forwarding`
- `request handling`

## 实现提示

- Accept incoming requests
- Forward to backend 服务端
- Return 响应 to 客户端

## 测试用例

### 1. Forward request

代理 forwards GET /api/data to backend和returns 响应 to 客户端

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

- [Proxy Patterns](https://en.wikipedia.org/wiki/Proxy_pattern)：Overview of 代理 design patterns

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
