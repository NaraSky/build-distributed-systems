# Implement Layer 7 HTTP Proxy

Website: <https://builddistributedsystem.com/tracks/loadbalancers/tasks/task-20-2-1-http-proxy>

Track: 14. Load Balancers
Task order: 6
Short title: HTTP Proxy
Difficulty: intermediate
Subtrack: Layer 7 Load Balancing

## Problem

Layer 7 load balancing operates at the HTTP application layer, inspecting headers and URL paths to make routing decisions. Unlike Layer 4 (TCP), L7 proxies understand HTTP semantics.

**HTTP proxy architecture**:
```
Client → L7 Proxy → Backend
  - Parse HTTP request
  - Inspect headers (Host, User-Agent, Cookies)
  - Inspect URL path (/api/users, /static/images)
  - Select backend based on rules
  - Forward request and return response
```

**Request flow**:
```
1. Client sends: GET /api/users HTTP/1.1
   Host: example.com

2. Proxy parses:
   - Method: GET
   - Path: /api/users
   - Host: example.com

3. Proxy routes to backend pool "api"

4. Backend responds: HTTP/1.1 200 OK
   {"users": [...]}

5. Proxy returns response to client
```

**Example request**:
```json
Request:  {"type": "http_request", "msg_id": 1, "method": "GET", "path": "/api/users", "headers": {"Host": "example.com", "User-Agent": "Mozilla"}}
Response: {"type": "http_response", "in_reply_to": 1, "status": 200, "headers": {"Content-Type": "application/json"}, "body": "{"users": [{"id": 1, "name": "Alice"}]}", "backend": "api-1"}
```

**Backend pool configuration**:
```json
{
  "backend_pools": {
    "api": {
      "backends": ["api-1:8080", "api-2:8080", "api-3:8080"],
      "algorithm": "round-robin"
    },
    "static": {
      "backends": ["static-1:8080", "static-2:8080"],
      "algorithm": "least-connections"
    }
  }
}
```

## Concepts

- layer 7 load balancing
- HTTP proxy
- request routing
- header inspection
- backend selection

## Hints

- Parse incoming HTTP requests to extract Host header and URL path
- Maintain a backend pool with health status
- Select a backend based on routing rules
- Forward the request to the backend and return the response
- Handle connection pooling and keep-alive

## Test Cases

### 1. Route HTTP GET to correct backend

http_response should return status 200 and indicate which backend handled the request (e.g., api-1).

Input:

```json
{"src":"client","dest":"l7_proxy","body":{"type":"http_request","msg_id":1,"method":"GET","path":"/api/users","headers":{"Host":"example.com"}}}
```

Expected output:

```text
{"src": "l7_proxy", "dest": "client", "body": {"type": "http_response", "in_reply_to": 1, "status": 200, "backend": "api-1"}}
```

### 2. Route based on URL path

Requests to /static/* should route to the static backend pool.

Input:

```json
{"src":"client","dest":"l7_proxy","body":{"type":"http_request","msg_id":1,"method":"GET","path":"/static/logo.png","headers":{"Host":"example.com"}}}
```

Expected output:

```text
{"src": "l7_proxy", "dest": "client", "body": {"type": "http_response", "in_reply_to": 1, "status": 200, "backend": "static-1"}}
```

## Resources

- [Layer 7 Load Balancing](https://www.nginx.com/resources/glossary/layer-7-load-balancing/): Introduction to L7 load balancing with Nginx

## Java Starter

The matching local starter file is:

```text
src/main/java/Main.java
```
