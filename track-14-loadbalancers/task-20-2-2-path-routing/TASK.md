# Implement Path-Based Routing

Website: <https://builddistributedsystem.com/tracks/loadbalancers/tasks/task-20-2-2-path-routing>

Track: 14. Load Balancers
Task order: 7
Short title: Path-Based Routing
Difficulty: intermediate
Subtrack: Layer 7 Load Balancing

## Problem

Path-based routing directs requests to different backend pools based on the URL path. This enables microservices architecture where /api/* routes to API servers and /static/* routes to CDN/static servers.

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
Request: /api/users/123
  - Matches /api/*           (priority: 1)
  - Matches /api/users/*     (priority: 2) ✓ MORE SPECIFIC
  → Route to users-service-pool
```

**URL rewriting**:
```
Client request: GET /api/v1/users
  ↓ (proxy rewrites)
Backend request: GET /v1/users
  ↓ (backend responds)
Proxy response: HTTP/1.1 200 OK
```

**Example routing**:
```json
Request:  {"type": "http_request", "msg_id": 1, "method": "GET", "path": "/api/users/123", "headers": {"Host": "example.com"}}
Response: {"type": "http_response", "in_reply_to": 1, "status": 200, "backend": "users-1", "rewritten_path": "/users/123"}
```

**Routing table configuration**:
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

## Concepts

- path-based routing
- URL rewriting
- routing tables
- wildcard matching
- backend pools

## Hints

- Match URL paths against routing rules: /api/* → api pool, /static/* → static pool
- Use longest-prefix matching: /api/users/auth matches /api/users/* not just /api/*
- Implement URL rewriting: strip /api prefix before forwarding to backend
- Support wildcards: /api/v* matches /api/v1, /api/v2
- Return 404 if no route matches

## Test Cases

### 1. Route /api/users to users pool

Should match /api/users/* (more specific than /api/*) and strip /api prefix.

Input:

```json
{"src":"client","dest":"l7_proxy","body":{"type":"http_request","msg_id":1,"method":"GET","path":"/api/users/123","headers":{"Host":"example.com"}}}
```

Expected output:

```text
{"src": "l7_proxy", "dest": "client", "body": {"type": "http_response", "in_reply_to": 1, "status": 200, "backend": "users-1", "rewritten_path": "/users/123"}}
```

### 2. Route /api/posts to api pool

Should match /api/* (no more specific rule exists) and strip /api prefix.

Input:

```json
{"src":"client","dest":"l7_proxy","body":{"type":"http_request","msg_id":1,"method":"GET","path":"/api/posts/456","headers":{"Host":"example.com"}}}
```

Expected output:

```text
{"src": "l7_proxy", "dest": "client", "body": {"type": "http_response", "in_reply_to": 1, "status": 200, "backend": "api-1", "rewritten_path": "/posts/456"}}
```

## Resources

- [Path-Based Routing](https://kubernetes.io/docs/concepts/services-networking/ingress/): Kubernetes ingress path-based routing documentation

## Java Starter

The matching local starter file is:

```text
src/main/java/Main.java
```
