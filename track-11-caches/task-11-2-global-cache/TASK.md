# Build Global Cache

Website: <https://builddistributedsystem.com/tracks/caches/tasks/task-11-2-global-cache>

Track: 11. Caches
Task order: 2
Short title: Global Cache
Difficulty: intermediate

## Problem

Implement a shared cache accessible by all nodes. Instead of each node maintaining its own cache, a dedicated cache server handles all cache operations.

Benefits:
1. No duplicate cached data
2. Single point for invalidation
3. Better memory utilization

Trade-offs:
1. Network hop for every cache access
2. Cache server becomes a bottleneck
3. Single point of failure

## Concept Notes

### Global Cache Architecture

A global cache centralizes cached data in one or more dedicated servers. All application nodes contact the cache server instead of maintaining local caches. This is the model used by Redis and Memcached.

### Look-Aside Cache Pattern

In look-aside (cache-aside), the application checks the cache, and on miss, queries the database and populates the cache. The cache is passive - it does not know about the database.

### Look-Through Cache Pattern

In look-through, the cache handles database interaction. On miss, the cache fetches from the database automatically. This simplifies application code but couples cache to database.

## Concepts

- shared cache
- cache coherence
- single point of truth

## Hints

- All nodes access a single cache instance
- Use network protocol for cache access
- Handle concurrent access safely
- Go/Python tip: avoid holding the lock while calling reply/send - this causes deadlocks with non-reentrant locks

## Test Cases

### 1. Global cache get/set

Input:

```json
{"src":"c0","dest":"cache","body":{"type":"init","msg_id":1,"node_id":"cache","node_ids":["cache","n1","n2"]}}
{"src":"n1","dest":"cache","body":{"type":"get","msg_id":2,"key":"x"}}
{"src":"n2","dest":"cache","body":{"type":"set","msg_id":3,"key":"x","value":100}}
{"src":"n1","dest":"cache","body":{"type":"get","msg_id":4,"key":"x"}}
```

Expected output:

```text
{"src":"cache","dest":"c0","body":{"type":"init_ok","in_reply_to":1,"msg_id":0}}
{"src":"cache","dest":"n1","body":{"type":"get_ok","in_reply_to":2,"msg_id":1,"value":null}}
{"src":"cache","dest":"n2","body":{"type":"set_ok","in_reply_to":3,"msg_id":2}}
{"src":"cache","dest":"n1","body":{"type":"get_ok","in_reply_to":4,"msg_id":3,"value":100}}
```

## Resources

- [Redis Documentation](https://redis.io/documentation): Redis as a global cache

## Java Starter

The matching local starter file is:

```text
src/main/java/Main.java
```
