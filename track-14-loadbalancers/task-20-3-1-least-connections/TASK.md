# Implement Least-Connections Load Balancing

Website: <https://builddistributedsystem.com/tracks/loadbalancers/tasks/task-20-3-1-least-connections>

Track: 14. Load Balancers
Task order: 11
Short title: Least-Connections
Difficulty: intermediate
Subtrack: Advanced Balancing Algorithms

## Problem

Least-connections load balancing routes each request to the backend with the fewest active connections. This is superior to round-robin when request durations vary significantly.

**Why least-connections?**
```
Round-robin problem:
  Request 1 → backend-1 (100ms duration)
  Request 2 → backend-2 (10ms duration)
  Request 3 → backend-3 (100ms duration)

  At t=50ms:
    backend-1: 1 active connection
    backend-2: 0 (completed)
    backend-3: 1 active connection

  Request 4 arrives → backend-1 (RR) → now has 2 active!
  Better: send to backend-2 (0 active)
```

**Connection tracking**:
```typescript
backendStates: Map<string, {
  activeConnections: number,
  totalRequests: number,
  lastUsed: timestamp
}>

function routeRequest(): string {
  // Find backend with minimum active connections
  let minBackend = null;
  let minConnections = Infinity;

  for (const [backend, state] of backendStates) {
    if (state.activeConnections < minConnections) {
      minConnections = state.activeConnections;
      minBackend = backend;
    }
  }

  // Increment counter atomically
  backendStates.get(minBackend).activeConnections++;
  return minBackend;
}

function requestComplete(backend: string) {
  backendStates.get(backend).activeConnections--;
}
```

**Example least-connections routing**:
```json
// Initial state: all backends have 0 connections
Request:  {"type": "http_request", "msg_id": 1, "method": "GET", "path": "/api/data", "algorithm": "least-connections"}
Response: {"type": "http_response", "in_reply_to": 1, "status": 200, "backend": "api-1", "active_connections": {"api-1": 1, "api-2": 0, "api-3": 0}}

// Second request routes to api-2 (0 connections)
Request:  {"type": "http_request", "msg_id": 2, "method": "GET", "path": "/api/data", "algorithm": "least-connections"}
Response: {"type": "http_response", "in_reply_to": 2, "status": 200, "backend": "api-2", "active_connections": {"api-1": 1, "api-2": 1, "api-3": 0}}
```

## Concepts

- least-connections
- active connection tracking
- load-based routing
- atomic counters
- variable request durations

## Hints

- Track active connections per backend: increment on request start, decrement on response
- Select backend with minimum active connections
- Use atomic counters for thread-safe updates
- Better than round-robin when request durations vary widely
- Example: long requests don't block other backends

## Test Cases

### 1. Route to backend with fewest connections

Should route to api-2 (2 connections, the minimum).

Input:

```json
{"src":"client","dest":"lb","body":{"type":"init","msg_id":1,"backends":["api-1","api-2","api-3"],"algorithm":"least-connections"}}
{"src":"client","dest":"lb","body":{"type":"http_request","msg_id":2,"method":"GET","path":"/api/data","active_connections":{"api-1":5,"api-2":2,"api-3":8}}}
```

Expected output:

```text
{"src": "lb", "dest": "client", "body": {"type": "init_ok", "in_reply_to": 1}}
```

### 2. Tie-breaking when connections equal

When all backends have equal connections, should use round-robin or consistent tie-breaking.

Input:

```json
{"src":"client","dest":"lb","body":{"type":"http_request","msg_id":1,"method":"GET","path":"/api/data","active_connections":{"api-1":3,"api-2":3,"api-3":3}}}
```

Expected output:

```text
{"src": "lb", "dest": "client", "body": {"type": "http_response", "in_reply_to": 1, "backend": "api-1"}}
```

## Resources

- [Least-Connections Algorithm](https://www.nginx.com/blog/nginx-load-balancing-algorithms/): NGINX documentation on load balancing algorithms

## Java Starter

The matching local starter file is:

```text
src/main/java/Main.java
```
