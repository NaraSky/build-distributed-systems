# Add Request Deduplication

Website: <https://builddistributedsystem.com/tracks/proxies/tasks/task-12-2-dedup>

Track: 12. Proxies
Task order: 2
Short title: Deduplication
Difficulty: intermediate
Subtrack: Caching Proxy

## Problem

Deduplicate identical concurrent requests to reduce backend load:

1. Compute a request key (e.g., hash of method + URL + body)
2. If a request with the same key is already in-flight, wait for it
3. When the original completes, return the same response to all waiters
4. After response, remove from in-flight set

This is especially valuable for hot endpoints with many identical requests.

## Concept Notes

### Request Deduplication

When many clients request the same resource simultaneously, sending all requests to the backend wastes resources. Deduplication sends one request and shares the response, reducing backend load dramatically.

### Request Fingerprinting

The dedup key must uniquely identify functionally equivalent requests. For GET requests, URL is often sufficient. For POST, you may need to hash the body. Be careful with headers that affect response.

## Concepts

- deduplication
- idempotency
- request coalescing

## Hints

- Track in-flight requests by key
- Have duplicates wait for original
- Return same response to all waiters

## Test Cases

### 1. Deduplicate concurrent

Multiple clients send identical requests (same idempotency key) to proxy concurrently. Proxy should recognize duplicates, send only ONE request to backend, and return same response to all clients. Track requests by idempotency key.

Input:

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
```

Expected output:

```text
{"src":"n1","dest":"c0","body":{"type":"init_ok","in_reply_to":1,"msg_id":0}}
```

## Java Starter

The matching local starter file is:

```text
src/main/java/Main.java
```
