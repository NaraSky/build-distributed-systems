# Implement API Composition and Aggregation

Website: <https://builddistributedsystem.com/tracks/proxies/tasks/task-21-2-4-aggregation>

Track: 12. Proxies
Task order: 9
Short title: API Composition
Difficulty: advanced
Subtrack: API Gateway

## Problem

API composition (aggregation) enables clients to fetch data from multiple services with a single request. The gateway fans out to backends and composes the response.

**Composition patterns**:
```
1. Aggregation (merge results):
   Client → Gateway → [Service A, Service B, Service C]
   Gateway merges: {a: {...}, b: {...}, c: {...}}

2. Composition (transform and combine):
   Client → Gateway → [User Service, Order Service]
   Gateway composes: {user: {...}, orders: [...]}

3. Chaining (sequential calls):
   Client → Gateway → Service A → (use A's result) → Service B
```

**Example: Order details aggregation**:
```json
// Client request:
Request:  {"type": "api_request", "msg_id": 1, "method": "GET", "path": "/api/orders/123/details"}

// Gateway fans out to 3 services:
Service A (Orders):   GET /orders/123 → {"id": 123, "user_id": 456, "items": [...]}
Service B (Users):    GET /users/456 → {"id": 456, "name": "Alice", "email": "..."}
Service C (Products): GET /products?id=1,2,3 → [{"id": 1, "name": "Widget"}, ...]

// Gateway composes response:
Response: {"type": "api_response", "in_reply_to": 1, "body": {
  "order": {"id": 123, "items": [...]},
  "user": {"id": 456, "name": "Alice"},
  "products": [{"id": 1, "name": "Widget"}, ...]
}}
```

**Aggregation configuration**:
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
      "failure_strategy": "partial"  // or "fail_fast"
    }
  }
}
```

**Failure strategies**:
```
partial: Return successful services, null for failed
  {"order": {...}, "user": null, "products": [...]}

fail_fast: If any service fails, return error immediately
  {"error": "Service unavailable: users-service"}

ignore: Continue without failed service
  {"order": {...}, "products": [...]}
```

## Concepts

- API composition
- aggregation pattern
- data composition
- parallel requests
- backend fan-out
- response merging

## Hints

- Gateway fans out requests to multiple backend services
- Collect responses from all services
- Merge/compose data into a single response for client
- Execute requests in parallel for performance
- Handle partial failures: return partial data or fail-fast

## Test Cases

### 1. Aggregate from 3 services

Gateway should fan out to 3 services and compose merged response with order, user, products.

Input:

```json
{"src":"client","dest":"gateway","body":{"type":"init","msg_id":1,"aggregations":{"/api/orders/*/details":{"backends":["orders","users","products"]}}}}
{"src":"client","dest":"gateway","body":{"type":"api_request","msg_id":2,"method":"GET","path":"/api/orders/123/details"}}
```

Expected output:

```text
{"src": "gateway", "dest": "client", "body": {"type": "init_ok", "in_reply_to": 1}}
```

### 2. Partial failure handling

With partial strategy, should return successful services and null for failed users service.

Input:

```json
{"src":"client","dest":"gateway","body":{"type":"api_request","msg_id":1,"method":"GET","path":"/api/orders/123/details"},"failure_strategy":"partial","failed_services":["users"]}
```

Expected output:

```text
{"src": "gateway", "dest": "client", "body": {"type": "api_response", "in_reply_to": 1, "body": {"order": {...}, "user": null, "products": [...]}}}
```

## Resources

- [API Gateway Aggregation Pattern](https://docs.microsoft.com/en-us/azure/architecture/patterns/api-gateway): Microsoft documentation on API Gateway aggregation pattern

## Java Starter

The matching local starter file is:

```text
src/main/java/Main.java
```
