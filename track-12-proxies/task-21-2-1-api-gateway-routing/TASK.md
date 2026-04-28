# Implement API Gateway Service Routing

Website: <https://builddistributedsystem.com/tracks/proxies/tasks/task-21-2-1-api-gateway-routing>

Track: 12. Proxies
Task order: 6
Short title: API Gateway Routing
Difficulty: intermediate
Subtrack: API Gateway

## Problem

An API Gateway provides a unified entry point for multiple microservices. Clients make one request to the gateway, which routes to the appropriate backend service.

**Gateway architecture**:
```
Clients → API Gateway → Microservices
  - /api/users/*    → users-service (3 instances)
  - /api/orders/*   → orders-service (2 instances)
  - /api/products/* → products-service (4 instances)
  - /api/payments/* → payments-service (2 instances)
```

**Routing rules**:
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

**Example gateway routing**:
```json
// Request to gateway:
Request:  {"type": "api_request", "msg_id": 1, "method": "GET", "path": "/api/users/123", "headers": {"Host": "api.example.com"}}
Response: {"type": "api_response", "in_reply_to": 1, "status": 200, "service": "users-service", "backend": "users-1", "body": "{"id": 123, "name": "Alice"}"}

// Request with versioning:
Request:  {"type": "api_request", "msg_id": 2, "method": "GET", "path": "/api/v2/users/123", "headers": {"Host": "api.example.com"}}
Response: {"type": "api_response", "in_reply_to": 2, "status": 200, "service": "users-service", "backend": "users-v2-1", "body": "{"id": 123, "name": "Alice", "email": "alice@example.com"}"}
```

## Concepts

- API gateway
- service routing
- microservices
- unified entry point
- service discovery

## Hints

- API gateway provides unified entry point for multiple microservices
- Route requests to backend services based on URL patterns
- Example: /api/users/* → users-service, /api/orders/* → orders-service
- Support service versioning: /api/v1/users vs /api/v2/users
- Handle service discovery: dynamically resolve service instances

## Test Cases

### 1. Route to correct service

api_response should route to users-service backend.

Input:

```json
{"src":"client","dest":"gateway","body":{"type":"init","msg_id":1,"routes":[{"path_pattern":"/api/users/*","service":"users-service","backends":["users-1","users-2"]}]}}
{"src":"client","dest":"gateway","body":{"type":"api_request","msg_id":2,"method":"GET","path":"/api/users/123"}}
```

Expected output:

```text
{"src": "gateway", "dest": "client", "body": {"type": "init_ok", "in_reply_to": 1}}
```

### 2. Service versioning

Should route to v2 of users-service based on URL path.

Input:

```json
{"src":"client","dest":"gateway","body":{"type":"api_request","msg_id":1,"method":"GET","path":"/api/v2/users/123"}}
```

Expected output:

```text
{"src": "gateway", "dest": "client", "body": {"type": "api_response", "in_reply_to": 1, "status": 200, "service": "users-service", "version": "v2"}}
```

## Resources

- [API Gateway Pattern](https://microservices.io/patterns/apigateway.html): Microservices.io documentation on API Gateway pattern

## Java Starter

The matching local starter file is:

```text
src/main/java/Main.java
```
