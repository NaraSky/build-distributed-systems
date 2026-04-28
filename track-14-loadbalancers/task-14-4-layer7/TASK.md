# Build Layer 7 Load Balancer

Website: <https://builddistributedsystem.com/tracks/loadbalancers/tasks/task-14-4-layer7>

Track: 14. Load Balancers
Task order: 4
Short title: Layer 7 LB
Difficulty: intermediate
Subtrack: Layer 4 Load Balancing

## Problem

Build an HTTP-aware (Layer 7) load balancer:

1. Parse HTTP request (method, path, headers)
2. Route based on Host header (virtual hosts)
3. Route based on URL path (/api/* -> api-servers)
4. Implement session stickiness via cookie
5. Support URL rewriting

Layer 7 enables intelligent routing based on request content.

## Concept Notes

### Layer 4 vs Layer 7

Layer 4 LBs see only TCP/UDP - fast but limited. Layer 7 LBs understand HTTP - can route by URL, read cookies, modify headers. More powerful but higher overhead.

### Session Stickiness

Some apps require all requests from a user to reach the same server (sessions). The LB can track sessions via cookies or source IP. Trade-off: stickiness can cause uneven load.

## Concepts

- Layer 7
- HTTP routing
- content-based

## Hints

- Parse HTTP headers
- Route based on path or host
- Support session stickiness

## Test Cases

### 1. Path-based routing

Layer 7 LB with path-based rules: /api/* -> [s1, s2], /web/* -> [s3]. Request for /api/users routes to s1 or s2.

Input:

```json
{"src":"c0","dest":"lb","body":{"type":"init","msg_id":1,"node_id":"lb","node_ids":["lb","s1","s2","s3"]}}
{"src":"client","dest":"lb","body":{"type":"http_request","msg_id":2,"path":"/api/users","method":"GET"}}
```

Expected output:

```text
{"src":"lb","dest":"c0","body":{"type":"init_ok","in_reply_to":1,"msg_id":0}}
{"src":"lb","dest":"client","body":{"type":"http_response","in_reply_to":2,"msg_id":1,"path":"/api/users","routed_to":"s1","status":200}}
```

## Java Starter

The matching local starter file is:

```text
src/main/java/Main.java
```
