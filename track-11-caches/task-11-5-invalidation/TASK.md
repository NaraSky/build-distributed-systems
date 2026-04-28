# Handle Cache Invalidation and Consistency

Website: <https://builddistributedsystem.com/tracks/caches/tasks/task-11-5-invalidation>

Track: 11. Caches
Task order: 5
Short title: Invalidation
Difficulty: advanced

## Problem

Implement cache invalidation strategies to maintain consistency between cache and database. When data changes, cached copies must be updated or removed.

Three main strategies:
1. Write-Through: Update cache and DB synchronously
2. Write-Behind: Update cache, async update DB
3. Cache-Aside with Invalidation: Delete cache, update DB

Also handle cache stampede: when many requests hit an expired key simultaneously.

## Concept Notes

### Cache Invalidation

"There are only two hard things in Computer Science: cache invalidation and naming things." - Phil Karlton. Keeping cache consistent with the source of truth is notoriously difficult.

### Write-Through

Every write goes to both cache and database synchronously. Simple to reason about but adds latency to writes. Cache is always consistent but writes are slow.

### Write-Behind (Write-Back)

Writes go to cache immediately, then asynchronously to database. Fast writes but risk of data loss if cache fails before flush. Requires careful durability handling.

### Cache Stampede

When a popular key expires, many requests simultaneously miss and hit the database. Solutions include: locking (only one fetches), early expiration (refresh before actual expiry), or probabilistic early expiration.

## Concepts

- invalidation
- consistency
- write-through
- write-behind

## Hints

- Invalidate on every write
- Consider eventual vs strong consistency
- Handle cache stampede scenarios

## Test Cases

### 1. Write-through consistency

Write-through pattern: Set key "x" with value 100. Verify write goes to BOTH cache and database synchronously. Get key "x" from cache should return 100. Database should also contain x=100. Cache and DB are always consistent.

Input:

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
```

Expected output:

```text
{"src":"n1","dest":"c0","body":{"type":"init_ok","in_reply_to":1,"msg_id":0}}
```

## Resources

- [XFetch Paper](https://cseweb.ucsd.edu/~avattani/papers/cache_stampede.pdf): Optimal probabilistic cache stampede prevention
- [Redis Patterns](https://redis.io/topics/data-types-intro): Caching patterns with Redis

## Java Starter

The matching local starter file is:

```text
src/main/java/Main.java
```
