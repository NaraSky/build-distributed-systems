# Implement Collapsed Forwarding

Website: <https://builddistributedsystem.com/tracks/proxies/tasks/task-12-3-collapsed>

Track: 12. Proxies
Task order: 3
Short title: Collapsed Forwarding
Difficulty: intermediate
Subtrack: Caching Proxy

## Problem

Implement collapsed forwarding for cache misses to prevent thundering herd:

When a cached item expires and multiple requests arrive:
1. First request goes to the origin (is "collapsed")
2. Subsequent requests for the same key wait
3. When origin responds, cache the response
4. Return the cached response to all waiting requests

This prevents the backend from being overwhelmed when popular items expire.

## Concept Notes

### Thundering Herd Problem

When a popular cached item expires, thousands of requests might simultaneously miss the cache and hit the backend. This can overwhelm the backend and cause cascading failures.

### Collapsed Forwarding

Collapsed forwarding allows only one request through to the origin while others wait. When the response arrives, it is cached and returned to all waiters. CDNs like Varnish implement this.

## Concepts

- collapsed forwarding
- thundering herd
- cache miss handling

## Hints

- Similar to deduplication but for cache misses
- Only one request goes to origin
- Queue waiters until response arrives

## Test Cases

### 1. Collapse concurrent requests

Cache miss for key "x". Three concurrent requests for key "x" arrive at proxy simultaneously. First request goes to backend (collapsed), other 2 wait. When backend responds, all 3 clients get the cached response. Verify only 1 backend call made.

Input:

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
```

Expected output:

```text
{"src":"n1","dest":"c0","body":{"type":"init_ok","in_reply_to":1,"msg_id":0}}
```

## Resources

- [Varnish Collapsed Forwarding](https://varnish-cache.org/docs/): Varnish documentation on request coalescing

## Java Starter

The matching local starter file is:

```text
src/main/java/Main.java
```
