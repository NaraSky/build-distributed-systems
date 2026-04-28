# 实现 Path-Based Routing

英文标题：Implement Path-Based Routing
网页：<https://builddistributedsystem.com/tracks/loadbalancers/tasks/task-20-2-2-path-routing>

课程：14. 负载均衡器
任务序号：7
短标题：Path-Based Routing
难度：intermediate
子主题：Layer 7 Load Balancing

## 中文导读

本题要求你完成 `实现 Path-Based Routing`。

重点关注：`path-based routing`、`URL rewriting`、`routing tables`、`wildcard matching`、`backend pools`。

建议先按提示逐步实现：Match URL paths against routing rules: /api/* → api pool, /static/* → static pool。

协议字段、消息类型、输入输出格式请以本文件中的代码块和测试用例为准。

## 题目说明

Path-based routing directs requests to different backend pools based on the URL path. This enables microservices architecture where /api/* routes to API servers和/static/* routes to CDN/static servers.

**Routing rules**:
```
/api/*              → api-backend-pool
/api/users/*       → users-service-pool (more specific)
/static/*          → static-backend-pool
/images/*          → image-backend-pool
/admin/*           → admin-backend-pool
```

**Longest-prefix matching**:
```
请求: /api/users/123
  - Matches /api/*           (priority: 1)
  - Matches /api/users/*     (priority: 2) ✓ MORE SPECIFIC
  → Route to users-service-pool
```

**URL rewriting**:
```
客户端 请求: GET /api/v1/users
  ↓ (代理 rewrites)
Backend 请求: GET /v1/users
  ↓ (backend responds)
代理 响应: HTTP/1.1 200 OK
```

**Example routing**:
```JSON
请求:  {"type": "http_request", "msg_id": 1, "method": "GET", "path": "/api/users/123", "headers": {"Host": "example.com"}}
响应: {"type": "http_response", "in_reply_to": 1, "status": 200, "backend": "users-1", "rewritten_path": "/users/123"}
```

**Routing table configuration**:
```JSON
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

- Match URL paths against routing rules: /api/* → api pool, /static/* → static pool
- Use longest-prefix matching: /api/users/auth matches /api/users/* not just /api/*
- Implement URL rewriting: strip /api prefix before forwarding to backend
- Support wildcards: /api/v* matches /api/v1, /api/v2
- Return 404 if no route matches

## 测试用例

### 1. Route /api/users to users pool

Should match /api/users/* (more specific than /api/*)和strip /api prefix.

输入：

```json
{"src":"client","dest":"l7_proxy","body":{"type":"http_request","msg_id":1,"method":"GET","path":"/api/users/123","headers":{"Host":"example.com"}}}
```

期望输出：

```text
{"src": "l7_proxy", "dest": "client", "body": {"type": "http_response", "in_reply_to": 1, "status": 200, "backend": "users-1", "rewritten_path": "/users/123"}}
```

### 2. Route /api/posts to api pool

Should match /api/* (no more specific rule exists)和strip /api prefix.

输入：

```json
{"src":"client","dest":"l7_proxy","body":{"type":"http_request","msg_id":1,"method":"GET","path":"/api/posts/456","headers":{"Host":"example.com"}}}
```

期望输出：

```text
{"src": "l7_proxy", "dest": "client", "body": {"type": "http_response", "in_reply_to": 1, "status": 200, "backend": "api-1", "rewritten_path": "/posts/456"}}
```

## 参考资料

- [Path-Based Routing](https://kubernetes.io/docs/concepts/services-networking/ingress/)：Kubernetes ingress path-based routing documentation

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
