# 实现 API Gateway 服务 Routing

英文标题：Implement API Gateway Service Routing
网页：<https://builddistributedsystem.com/tracks/proxies/tasks/task-21-2-1-api-gateway-routing>

课程：12. 代理
任务序号：6
短标题：API Gateway Routing
难度：intermediate
子主题：API Gateway

## 中文导读

本题要求你完成 `实现 API Gateway 服务 Routing`。

重点关注：`API gateway`、`service routing`、`microservices`、`unified entry point`、`service discovery`。

建议先按提示逐步实现：API gateway provides unified entry point用于multiple microservices。

协议字段、消息类型、输入输出格式请以本文件中的代码块和测试用例为准。

## 题目说明

An API Gateway provides a unified entry point用于multiple microservices. Clients make one 请求 to the gateway, which routes to the appropriate backend service.

**Gateway architecture**:
```
Clients → API Gateway → Microservices
  - /api/users/*    → users-service (3 instances)
  - /api/orders/*   → orders-service (2 instances)
  - /api/products/* → products-service (4 instances)
  - /api/payments/* → payments-service (2 instances)
```

**Routing rules**:
```JSON
{
  "routes": [
    {
      "path_pattern": "/api/users/*",
      "service": "users-service",
      "version": "v1",
      "backends": ["users-1:8080", "users-2:8080", "users-3:8080"],
      "strip_prefix": false
    },
    {
      "path_pattern": "/api/v2/users/*",
      "service": "users-service",
      "version": "v2",
      "backends": ["users-v2-1:8080", "users-v2-2:8080"],
      "strip_prefix": false
    },
    {
      "path_pattern": "/api/orders/*",
      "service": "orders-service",
      "version": "v1",
      "backends": ["orders-1:8080", "orders-2:8080"],
      "strip_prefix": false
    }
  ]
}
```

**Example gateway routing**:
```JSON
// 请求 to gateway:
请求:  {"type": "api_request", "msg_id": 1, "method": "GET", "path": "/api/users/123", "headers": {"Host": "api.example.com"}}
响应: {"type": "api_response", "in_reply_to": 1, "status": 200, "service": "users-service", "backend": "users-1", "body": "{"id": 123, "name": "Alice"}"}

// 请求，包含versioning:
请求:  {"type": "api_request", "msg_id": 2, "method": "GET", "path": "/api/v2/users/123", "headers": {"Host": "api.example.com"}}
响应: {"type": "api_response", "in_reply_to": 2, "status": 200, "service": "users-service", "backend": "users-v2-1", "body": "{"id": 123, "name": "Alice", "email": "alice@example.com"}"}
```

## 涉及概念

- `API gateway`
- `service routing`
- `microservices`
- `unified entry point`
- `service discovery`

## 实现提示

- API gateway provides unified entry point用于multiple microservices
- Route requests to backend services based on URL patterns
- Example: /api/users/* → users-service, /api/orders/* → orders-service
- Support service versioning: /api/v1/users vs /api/v2/users
-处理service discovery: dynamically resolve service instances

## 测试用例

### 1. Route to correct 服务

api_response should route to users-service backend.

输入：

```json
{"src":"client","dest":"gateway","body":{"type":"init","msg_id":1,"routes":[{"path_pattern":"/api/users/*","service":"users-service","backends":["users-1","users-2"]}]}}
{"src":"client","dest":"gateway","body":{"type":"api_request","msg_id":2,"method":"GET","path":"/api/users/123"}}
```

期望输出：

```text
{"src": "gateway", "dest": "client", "body": {"type": "init_ok", "in_reply_to": 1}}
```

### 2. 服务 versioning

Should route to v2 of users-service based on URL path.

输入：

```json
{"src":"client","dest":"gateway","body":{"type":"api_request","msg_id":1,"method":"GET","path":"/api/v2/users/123"}}
```

期望输出：

```text
{"src": "gateway", "dest": "client", "body": {"type": "api_response", "in_reply_to": 1, "status": 200, "service": "users-service", "version": "v2"}}
```

## 参考资料

- [API Gateway Pattern](https://microservices.io/patterns/apigateway.html)：Microservices.io documentation on API Gateway pattern

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
