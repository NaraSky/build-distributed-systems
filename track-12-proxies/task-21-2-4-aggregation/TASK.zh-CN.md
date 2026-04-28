# 实现 API 组合与聚合

英文标题：Implement API Composition and Aggregation
网页：<https://builddistributedsystem.com/tracks/proxies/tasks/task-21-2-4-aggregation>

课程：12. 代理
任务序号：9
短标题：API 组合
难度：高级
子主题：API 网关

## 中文导读

这道题要求你实现 API 组合（API Composition）和聚合功能。在微服务架构中，一次用户操作往往需要从多个服务获取数据。如果让客户端分别调用每个服务，不仅增加了网络往返次数，还增加了客户端的复杂度。通过在网关层实现聚合，客户端只需发送一个请求，网关就会并行调用多个后端服务并将结果合并后返回。

## 题目说明

API 组合（也叫聚合）让客户端能够通过一次请求从多个服务获取数据。网关负责将请求扇出到多个后端，然后组合响应。

**组合模式**：
```
1. 聚合（合并结果）：
   客户端 → 网关 → [服务 A, 服务 B, 服务 C]
   网关合并结果：{a: {...}, b: {...}, c: {...}}

2. 组合（转换并合并）：
   客户端 → 网关 → [用户服务, 订单服务]
   网关组合结果：{user: {...}, orders: [...]}

3. 链式调用（顺序调用）：
   客户端 → 网关 → 服务 A → （使用 A 的结果） → 服务 B
```

**示例：订单详情聚合**：
```json
// 客户端请求：
Request:  {"type": "api_request", "msg_id": 1, "method": "GET", "path": "/api/orders/123/details"}

// 网关扇出到 3 个服务：
Service A (Orders):   GET /orders/123 → {"id": 123, "user_id": 456, "items": [...]}
Service B (Users):    GET /users/456 → {"id": 456, "name": "Alice", "email": "..."}
Service C (Products): GET /products?id=1,2,3 → [{"id": 1, "name": "Widget"}, ...]

// 网关组合响应：
Response: {"type": "api_response", "in_reply_to": 1, "body": {
  "order": {"id": 123, "items": [...]},
  "user": {"id": 456, "name": "Alice"},
  "products": [{"id": 1, "name": "Widget"}, ...]
}}
```

**聚合配置**：
```json
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
      "failure_strategy": "partial"
    }
  }
}
```

**失败策略**：
```
partial（部分返回）：返回成功的服务结果，失败的用 null 表示
  {"order": {...}, "user": null, "products": [...]}

fail_fast（快速失败）：如果任何一个服务失败，立即返回错误
  {"error": "Service unavailable: users-service"}

ignore（忽略）：跳过失败的服务，继续返回其余结果
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

- 网关将请求扇出到多个后端服务
- 收集所有服务的响应
- 将数据合并或组合成一个统一的响应返回给客户端
- 并行执行请求以提高性能
- 处理部分失败的情况：可以返回部分数据，也可以快速失败

## 测试用例

### 1. 从 3 个服务聚合数据

网关应扇出到 3 个服务，并将订单、用户、商品信息组合成一个合并的响应。

输入：

```json
{"src":"client","dest":"gateway","body":{"type":"init","msg_id":1,"aggregations":{"/api/orders/*/details":{"backends":["orders","users","products"]}}}}
{"src":"client","dest":"gateway","body":{"type":"api_request","msg_id":2,"method":"GET","path":"/api/orders/123/details"}}
```

期望输出：

```text
{"src": "gateway", "dest": "client", "body": {"type": "init_ok", "in_reply_to": 1}}
```

### 2. 部分失败处理

使用部分返回策略时，应返回成功的服务结果，对失败的用户服务返回 null。

输入：

```json
{"src":"client","dest":"gateway","body":{"type":"api_request","msg_id":1,"method":"GET","path":"/api/orders/123/details"},"failure_strategy":"partial","failed_services":["users"]}
```

期望输出：

```text
{"src": "gateway", "dest": "client", "body": {"type": "api_response", "in_reply_to": 1, "body": {"order": {...}, "user": null, "products": [...]}}}
```

## 参考资料

- [API Gateway Aggregation Pattern](https://docs.microsoft.com/en-us/azure/architecture/patterns/api-gateway)：微软关于 API 网关聚合模式的文档

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
