# Build Reverse Proxy with Caching

Website: <https://builddistributedsystem.com/tracks/proxies/tasks/task-12-4-reverse-proxy>

Track: 12. Proxies
Task order: 4
Short title: Reverse Proxy
Difficulty: intermediate
Subtrack: Caching Proxy

## Problem

Build an HTTP-aware reverse proxy with caching:

1. Parse incoming HTTP requests
2. Check cache for valid response
3. On cache miss, forward to backend
4. Parse response headers for caching policy
5. Cache response according to Cache-Control
6. Return response to client

Support ETag and If-Modified-Since for cache validation.

## Concept Notes

### HTTP Caching Headers

HTTP provides rich cache control: Cache-Control sets freshness duration, ETag enables validation without full fetch, Vary handles content negotiation. A good proxy respects all of these.

### Cache Validation

Instead of fetching a full response, validation asks "has this changed?" using If-None-Match (with ETag) or If-Modified-Since. A 304 Not Modified response confirms the cached copy is still valid.

## Concepts

- reverse proxy
- HTTP caching
- Cache-Control

## Hints

- Parse HTTP headers for caching hints
- Honor Cache-Control directives
- Implement ETag validation

## Test Cases

### 1. Cache with max-age

Backend responds with Cache-Control: max-age=60. Reverse proxy should cache response for 60 seconds. Requests within 60s should return cached response without hitting backend. After 60s, cache expires and proxy should fetch fresh response.

Input:

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
```

Expected output:

```text
{"src":"n1","dest":"c0","body":{"type":"init_ok","in_reply_to":1,"msg_id":0}}
```

### 2. Honor no-store

Backend responds with Cache-Control: no-store. Reverse proxy should NOT cache this response. Every request should go to backend, even for same URL. Verify proxy respects no-store directive.

Input:

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
```

Expected output:

```text
{"src":"n1","dest":"c0","body":{"type":"init_ok","in_reply_to":1,"msg_id":0}}
```

## Resources

- [HTTP Caching](https://developer.mozilla.org/en-US/docs/Web/HTTP/Caching): MDN guide to HTTP caching

## Java Starter

The matching local starter file is:

```text
src/main/java/Main.java
```
