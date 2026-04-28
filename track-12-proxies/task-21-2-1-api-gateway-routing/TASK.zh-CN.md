# 实现 API 网关的服务路由

英文标题：Implement API Gateway Service Routing
网页：<https://builddistributedsystem.com/tracks/proxies/tasks/task-21-2-1-api-gateway-routing>

课程：12. 代理
任务序号：6
短标题：API 网关路由
难度：进阶
子主题：API 网关

## 中文导读

这道题要求你实现一个 API 网关（API Gateway）的服务路由功能。API 网关是微服务架构中的统一入口，客户端只需向网关发送一个请求，网关根据 URL 模式将请求路由到对应的后端微服务。这样客户端不需要知道后端有多少个服务，也不需要知道每个服务的地址，大大简化了客户端的复杂度。

## 题目说明

API 网关为多个微服务提供统一的入口。客户端向网关发送一个请求，网关负责将其路由到正确的后端服务。

**网关架构**：
```
客户端 → API 网关 → 微服务
  - /api/users/*    → users-service（3 个实例）
  - /api/orders/*   → orders-service（2 个实例）
  - /api/products/* → products-service（4 个实例）
  - /api/payments/* → payments-service（2 个实例）
```

**路由规则**：
```json
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

**网关路由示例**：
```json
// 发送到网关的请求：
Request:  {"type": "api_request", "msg_id": 1, "method": "GET", "path": "/api/users/123", "headers": {"Host": "api.example.com"}}
Response: {"type": "api_response", "in_reply_to": 1, "status": 200, "service": "users-service", "backend": "users-1", "body": "{"id": 123, "name": "Alice"}"}

// 带版本号的请求：
Request:  {"type": "api_request", "msg_id": 2, "method": "GET", "path": "/api/v2/users/123", "headers": {"Host": "api.example.com"}}
Response: {"type": "api_response", "in_reply_to": 2, "status": 200, "service": "users-service", "backend": "users-v2-1", "body": "{"id": 123, "name": "Alice", "email": "alice@example.com"}"}
```

## 涉及概念

- `API gateway`
- `service routing`
- `microservices`
- `unified entry point`
- `service discovery`

## 实现提示

- API 网关为多个微服务提供统一的入口
- 根据 URL 模式将请求路由到对应的后端服务
- 例如：/api/users/* 路由到 users-service，/api/orders/* 路由到 orders-service
- 支持服务版本管理：/api/v1/users 和 /api/v2/users 路由到不同版本
- 处理服务发现：动态解析服务实例的地址

## 测试用例

### 1. 路由到正确的服务

api_response 应该路由到 users-service 后端。

输入：

```json
{"src":"client","dest":"gateway","body":{"type":"init","msg_id":1,"routes":[{"path_pattern":"/api/users/*","service":"users-service","backends":["users-1","users-2"]}]}}
{"src":"client","dest":"gateway","body":{"type":"api_request","msg_id":2,"method":"GET","path":"/api/users/123"}}
```

期望输出：

```text
{"src": "gateway", "dest": "client", "body": {"type": "init_ok", "in_reply_to": 1}}
```

### 2. 服务版本路由

应根据 URL 路径将请求路由到 users-service 的 v2 版本。

输入：

```json
{"src":"client","dest":"gateway","body":{"type":"api_request","msg_id":1,"method":"GET","path":"/api/v2/users/123"}}
```

期望输出：

```text
{"src": "gateway", "dest": "client", "body": {"type": "api_response", "in_reply_to": 1, "status": 200, "service": "users-service", "version": "v2"}}
```

## 参考资料

- [API Gateway Pattern](https://microservices.io/patterns/apigateway.html)：Microservices.io 上关于 API 网关模式的文档

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
