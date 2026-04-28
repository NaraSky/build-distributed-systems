# Implement Service Mesh Architecture

Website: <https://builddistributedsystem.com/tracks/orchestrator/tasks/task-26-2-1-service-mesh>

Track: 28. The Orchestrator
Task order: 6
Short title: Service Mesh
Difficulty: advanced
Subtrack: Service Mesh

## Problem

A service mesh adds a sidecar proxy to every service. All traffic flows through these proxies, which transparently handle service discovery, retries, circuit breaking, and distributed tracing without any application code changes.

Implement a node that simulates sidecar proxy behaviour:

```json
// Sidecar intercepts a request and adds tracing context
{ "type": "call", "msg_id": 1, "path": "/api/users/123", "proxy": true }
-> { "type": "proxied", "in_reply_to": 1,
    "proxied_by": "sidecar-a", "trace_id": "<uuid>" }

// Discover healthy instances of a service
{ "type": "discover", "msg_id": 2, "service": "service-b" }
-> { "type": "discovered", "in_reply_to": 2,
    "service": "service-b",
    "instances": [{"host": "10.0.1.1", "port": 8080},
                  {"host": "10.0.1.2", "port": 8080}] }

// Circuit breaker opens after too many failures
{ "type": "call", "msg_id": 3,
  "force_failures": 6, "circuit_breaker": true }
-> { "type": "circuit_breaker_open", "in_reply_to": 3,
    "service": "service-b", "reason": "Too many failures" }
```

Every request proxied through the sidecar must receive a unique `trace_id` that can be propagated to downstream services for end-to-end tracing.

## Concepts

- service mesh
- sidecar proxy
- service discovery
- circuit breaker
- retry
- distributed tracing

## Hints

- A sidecar proxy intercepts all inbound and outbound traffic for its service
- discover queries the service registry for healthy instances of a named service
- Add a trace_id to every proxied request so traces can be correlated across services
- Circuit breaker opens when failure count exceeds the threshold; fail immediately while open
- Retry with exponential backoff: first retry after base_ms, second after base_ms*2, etc.

## Test Cases

### 1. Sidecar proxy intercepts traffic

Sidecar should intercept and forward request with a trace_id.

Input:

```json
{"src":"service-a","dest":"service-b","body":{"type":"call","msg_id":1,"path":"/api/users/123"},"proxy":true}
```

Expected output:

```text
{"type": "proxied", "in_reply_to": 1, "proxied_by": "sidecar-a", "trace_id": ".*"}
```

### 2. Service discovery routes to instances

Should return healthy instances from the service registry.

Input:

```json
{"src":"sidecar","dest":"registry","body":{"type":"discover","msg_id":1,"service":"service-b"}}
```

Expected output:

```text
{"type": "discovered", "in_reply_to": 1, "service": "service-b", "instances": [{"host": "10.0.1.1", "port": 8080}, {"host": "10.0.1.2", "port": 8080}]}
```

## Resources

- [Service Mesh Explained](https://www.nginx.com/blog/what-is-a-service-mesh/): What a service mesh is and why you need one
- [Envoy Proxy](https://www.envoyproxy.io/): Envoy proxy documentation

## Java Starter

The matching local starter file is:

```text
src/main/java/Main.java
```
