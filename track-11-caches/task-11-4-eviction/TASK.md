# Add Eviction Strategies (LRU, TTL)

Website: <https://builddistributedsystem.com/tracks/caches/tasks/task-11-4-eviction>

Track: 11. Caches
Task order: 4
Short title: Eviction
Difficulty: intermediate

## Problem

Implement cache eviction policies to manage limited memory. When the cache is full and a new entry must be added, an eviction policy decides what to remove.

Implement two eviction strategies:
1. TTL (Time-To-Live): Remove entries after they expire
2. LRU (Least Recently Used): Remove entries not accessed recently

Combine them: honor TTL, and when at capacity, evict LRU entries.

## Concept Notes

### Why Eviction?

Memory is finite. Without eviction, caches would grow unbounded. Eviction policies determine which entries to remove when space is needed.

### LRU (Least Recently Used)

LRU evicts the entry that has not been accessed for the longest time. The assumption is that recently accessed data will be accessed again (temporal locality). LRU is the most common eviction policy.

### LFU (Least Frequently Used)

LFU tracks access counts and evicts entries with the lowest frequency. This works well for stable access patterns but can keep old cold entries that were once popular.

## Concepts

- LRU
- TTL
- eviction
- cache capacity

## Hints

- Track access time for LRU
- Use ordered dict or doubly-linked list
- Evict when capacity is reached

## Test Cases

### 1. LRU eviction

LRU cache with max_size=3. Sequence: set(a,1), set(b,2), set(c,3) [cache full], get(a), get(c) [a and c accessed recently], set(d,4) [should evict b as least recently used]. Verify b is evicted, a and c remain in cache, d is added.

Input:

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
```

Expected output:

```text
{"src":"n1","dest":"c0","body":{"type":"init_ok","in_reply_to":1,"msg_id":0}}
```

## Resources

- [LRU Cache Implementation](https://leetcode.com/problems/lru-cache/): LeetCode LRU cache problem

## Java Starter

The matching local starter file is:

```text
src/main/java/Main.java
```
