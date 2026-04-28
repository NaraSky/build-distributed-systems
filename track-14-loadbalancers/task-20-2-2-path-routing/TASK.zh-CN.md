# 实现基于路径的路由

英文标题：Implement Path-Based Routing
网页：<https://builddistributedsystem.com/tracks/loadbalancers/tasks/task-20-2-2-path-routing>

课程：14. 负载均衡器
任务序号：7
短标题：Path-Based Routing
难度：进阶
子主题：七层负载均衡

## 中文导读

本题要求你实现基于 URL 路径的请求路由。在微服务架构中，不同的路径通常对应不同的服务：比如 /api/* 打到 API 服务器，/static/* 打到静态资源服务器。你需要实现路径匹配（包括最长前缀匹配）和 URL 重写功能。这是构建 API 网关和微服务入口的核心能力。

协议字段、消息类型、输入输出格式请以本文件中的代码块和测试用例为准。

## 题目说明

基于路径的路由根据 URL 路径将请求转发到不同的后端池，从而支持微服务架构——例如 /api/* 路由到 API 服务器，/static/* 路由到 CDN 或静态资源服务器。

**路由规则**：
```
/api/*              → api-backend-pool
/api/users/*       → users-service-pool (more specific)
/static/*          → static-backend-pool
/images/*          → image-backend-pool
/admin/*           → admin-backend-pool
```

**最长前缀匹配**：
```
Request: /api/users/123
  - Matches /api/*           (priority: 1)
  - Matches /api/users/*     (priority: 2) ✓ MORE SPECIFIC
  → Route to users-service-pool
```

**URL 重写**：
```
Client request: GET /api/v1/users
  ↓ (proxy rewrites)
Backend request: GET /v1/users
  ↓ (backend responds)
Proxy response: HTTP/1.1 200 OK
```

**路由示例**：
```json
Request:  {"type": "http_request", "msg_id": 1, "method": "GET", "path": "/api/users/123", "headers": {"Host": "example.com"}}
Response: {"type": "http_response", "in_reply_to": 1, "status": 200, "backend": "users-1", "rewritten_path": "/users/123"}
```

**路由表配置**：
```json
{
  "routes": [
    {"path_pattern": "/api/users/*", "backend_pool": "users", "rewrite": { "strip_prefix": "/api" }},
    {"path_pattern": "/api/*", "backend_pool": "api", "rewrite": { "strip_prefix": "/api" }},
    {"path_pattern": "/static/*", "backend_pool": "static", "rewrite": {}},
    {"path_pattern": "/images/*", "backend_pool": "images", "rewrite": {}}
  ]
}
```

## 涉及概念

- `path-based routing`
- `URL rewriting`
- `routing tables`
- `wildcard matching`
- `backend pools`

## 实现提示

- 将 URL 路径与路由规则匹配：/api/* 路由到 API 池，/static/* 路由到静态资源池
- 使用最长前缀匹配：/api/users/auth 应匹配 /api/users/* 而不是 /api/*
- 实现 URL 重写：转发到后端前去掉 /api 前缀
- 支持通配符：/api/v* 匹配 /api/v1、/api/v2
- 没有匹配规则时返回 404

## 测试用例

### 1. 将 /api/users 路由到用户服务池

应匹配 /api/users/*（比 /api/* 更具体），并去掉 /api 前缀。

输入：

```json
{"src":"client","dest":"l7_proxy","body":{"type":"http_request","msg_id":1,"method":"GET","path":"/api/users/123","headers":{"Host":"example.com"}}}
```

期望输出：

```text
{"src": "l7_proxy", "dest": "client", "body": {"type": "http_response", "in_reply_to": 1, "status": 200, "backend": "users-1", "rewritten_path": "/users/123"}}
```

### 2. 将 /api/posts 路由到通用 API 池

应匹配 /api/*（没有更具体的规则），并去掉 /api 前缀。

输入：

```json
{"src":"client","dest":"l7_proxy","body":{"type":"http_request","msg_id":1,"method":"GET","path":"/api/posts/456","headers":{"Host":"example.com"}}}
```

期望输出：

```text
{"src": "l7_proxy", "dest": "client", "body": {"type": "http_response", "in_reply_to": 1, "status": 200, "backend": "api-1", "rewritten_path": "/posts/456"}}
```

## 参考资料

- [Path-Based Routing](https://kubernetes.io/docs/concepts/services-networking/ingress/)：关于基于路径路由的说明文档

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
