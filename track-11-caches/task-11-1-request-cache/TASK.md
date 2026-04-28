# Implement Request Node Cache

Website: <https://builddistributedsystem.com/tracks/caches/tasks/task-11-1-request-cache>

Track: 11. Caches
Task order: 1
Short title: Request Cache
Difficulty: intermediate

## Problem

Implement a local cache at each request-handling node. When a request comes in:

1. Check if the key exists in the local cache
2. If cache hit and not expired, return cached value
3. If cache miss or expired, fetch from backend
4. Store result in cache with TTL
5. Return result

Track cache hit rate to measure effectiveness.

## Concept Notes

### Why Caching?

Caching trades space for time. By storing frequently accessed data closer to the requester, we reduce latency and backend load. A cache with 90% hit rate reduces backend traffic by 10x.

### Request Node Cache

The simplest cache sits at each request handler. It is fast (no network hop) but duplicates data across nodes. This works well for hot data that all nodes access.

### TTL (Time-To-Live)

TTL defines how long cached data remains valid. Short TTL = more freshness, more backend load. Long TTL = less freshness, less load. Choose based on how often data changes and tolerance for staleness.

## Concepts

- caching
- local cache
- TTL

## Hints

- Cache responses at the request node
- Use TTL for freshness control
- Check cache before calling backend

## Test Cases

### 1. Cache hit

Input:

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"cache_write","msg_id":2,"key":"x","value":100}}
{"src":"c2","dest":"n1","body":{"type":"cache_read","msg_id":3,"key":"x"}}
```

Expected output:

```text
{"src":"n1","dest":"c0","body":{"type":"init_ok","in_reply_to":1,"msg_id":0}}
{"src":"n1","dest":"c1","body":{"type":"cache_write_ok","in_reply_to":2,"msg_id":1}}
{"src":"n1","dest":"c2","body":{"type":"cache_read_ok","in_reply_to":3,"msg_id":2,"hit":true,"value":100}}
```

## Resources

- [Caching Strategies](https://aws.amazon.com/caching/): AWS guide to caching strategies
- [DDIA Chapter 5](https://dataintensive.net/): Replication and caching concepts

## Java Starter

The matching local starter file is:

```text
src/main/java/Main.java
```
