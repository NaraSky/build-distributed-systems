# 实现 API Composition和Aggregation

英文标题：Implement API Composition和Aggregation
网页：<https://builddistributedsystem.com/tracks/proxies/tasks/task-21-2-4-aggregation>

课程：12. 代理
任务序号：9
短标题：API Composition
难度：advanced
子主题：API Gateway

## 中文导读

本题要求你完成 `实现 API Composition和Aggregation`。

重点关注：`API composition`、`aggregation pattern`、`data composition`、`parallel requests`、`backend fan-out`。

建议先按提示逐步实现：Gateway fans out requests to multiple backend services。

协议字段、消息类型、输入输出格式请以本文件中的代码块和测试用例为准。

## 题目说明

API composition (aggregation) enables clients to fetch data from multiple services，包含a single 请求. The gateway fans out to backends和composes the 响应.

**Composition patterns**:
```
1. Aggregation (merge results):
   客户端 → Gateway → [Service A, Service B, Service C]
   Gateway merges: {a: {...}, b: {...}, c: {...}}

2. Composition (transform和combine):
   客户端 → Gateway → [User Service, Order Service]
   Gateway composes: {user: {...}, orders: [...]}

3. Chaining (sequential calls):
   客户端 → Gateway → Service A → (use A's result) → Service B
```

**Example: Order details aggregation**:
```JSON
// 客户端 请求:
请求:  {"type": "api_request", "msg_id": 1, "method": "GET", "path": "/api/orders/123/details"}

// Gateway fans out to 3 services:
Service A (Orders):   GET /orders/123 → {"id": 123, "user_id": 456, "items": [...]}
Service B (Users):    GET /users/456 → {"id": 456, "name": "Alice", "email": "..."}
Service C (Products): GET /products?id=1,2,3 → [{"id": 1, "name": "Widget"}, ...]

// Gateway composes 响应:
响应: {"type": "api_response", "in_reply_to": 1, "body": {
  "order": {"id": 123, "items": [...]},
  "user": {"id": 456, "name": "Alice"},
  "products": [{"id": 1, "name": "Widget"}, ...]
}}
```

**Aggregation configuration**:
```JSON
{
  "aggregations": {
    "/api/orders/*/details": {
      "backend_requests": [
        {"service": "orders", "path_template": "/orders/{order_id}"},
        {"service": "users", "path_template": "/users/{user_id}", "source": "orders.user_id"},
        {"service": "products", "path_template": "/products", "source": "orders.items.*.product_id"}
      ],
      "response_template": {
        "order": "$.orders",
        "user": "$.users",
        "products": "$.products"
      },
      "timeout_ms": 2000,
      "failure_strategy": "partial"  // or "fail_fast"
    }
  }
}
```

**故障 strategies**:
```
partial: Return successful services, null用于failed
  {"order": {...}, "user": null, "products": [...]}

fail_fast: If any service fails, return error immediately
  {"error": "Service unavailable: users-service"}

ignore: Continue without failed service
  {"order": {...}, "products": [...]}
```

## 涉及概念

- `API composition`
- `aggregation pattern`
- `data composition`
- `parallel requests`
- `backend fan-out`
- `response merging`

## 实现提示

- Gateway fans out requests to multiple backend services
- Collect responses from all services
- Merge/compose data into a single 响应用于客户端
- Execute requests in parallel用于performance
-处理partial failures: return partial data or fail-fast

## 测试用例

### 1. Aggregate from 3 services

Gateway should fan out to 3 services和compose merged 响应，包含order, user, products.

输入：

```json
{"src":"client","dest":"gateway","body":{"type":"init","msg_id":1,"aggregations":{"/api/orders/*/details":{"backends":["orders","users","products"]}}}}
{"src":"client","dest":"gateway","body":{"type":"api_request","msg_id":2,"method":"GET","path":"/api/orders/123/details"}}
```

期望输出：

```text
{"src": "gateway", "dest": "client", "body": {"type": "init_ok", "in_reply_to": 1}}
```

### 2. Partial failure handling

With partial strategy, should return successful services和null用于failed users service.

输入：

```json
{"src":"client","dest":"gateway","body":{"type":"api_request","msg_id":1,"method":"GET","path":"/api/orders/123/details"},"failure_strategy":"partial","failed_services":["users"]}
```

期望输出：

```text
{"src": "gateway", "dest": "client", "body": {"type": "api_response", "in_reply_to": 1, "body": {"order": {...}, "user": null, "products": [...]}}}
```

## 参考资料

- [API Gateway Aggregation Pattern](https://docs.microsoft.com/en-us/azure/architecture/patterns/api-gateway)：Microsoft documentation on API Gateway aggregation pattern

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
