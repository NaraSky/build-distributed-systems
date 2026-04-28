# Implement a Buffer Pool with LRU Eviction

Website: <https://builddistributedsystem.com/tracks/logger/tasks/task-10-3-4-buffer-pool>

Track: 19. The Logger
Task order: 14
Short title: Buffer Pool
Difficulty: advanced
Subtrack: B-Tree on Disk

## Problem

Disk I/O is 1000x slower than memory access. The buffer pool bridges this gap by caching frequently accessed B-Tree pages in RAM. This is how every production database (PostgreSQL, MySQL, Oracle) achieves acceptable performance.

Buffer pool design:
1. **Fixed-size memory region**: holds N pages (e.g. 100 pages * 4KB = 400KB)
2. **Page table**: maps (page_id -> frame_number) for O(1) lookup
3. **LRU eviction**: when a new page is needed but the pool is full, evict the least recently used page
4. **Dirty page tracking**: pages modified in memory are marked "dirty". Before evicting a dirty page, flush it to disk.
5. **Hit rate monitoring**: track the ratio of cache hits to total reads. High hit rates (>95%) mean the working set fits in memory.

The eviction policy is critical:
- LRU works well for most workloads but is vulnerable to sequential scans (a full table scan can evict the entire cache)
- MySQL uses a "young" and "old" sublist to protect against this
- PostgreSQL uses a clock sweep algorithm (approximated LRU)

```json
Request:  {"type": "buffer_pool_config", "msg_id": 1, "max_pages": 100, "page_size_bytes": 4096}
Response: {"type": "buffer_pool_config_ok", "in_reply_to": 1, "total_memory_bytes": 409600}

Request:  {"type": "buffer_pool_read", "msg_id": 2, "page_id": 42}
Response: {"type": "buffer_pool_read_ok", "in_reply_to": 2, "cache_hit": false, "disk_read": true}

Request:  {"type": "buffer_pool_stats", "msg_id": 3}
Response: {"type": "buffer_pool_stats_ok", "in_reply_to": 3, "total_reads": 1000, "cache_hits": 850, "hit_rate": 0.85, "dirty_pages": 12, "evictions": 50}
```

## Concepts

- buffer pool
- LRU eviction
- page cache
- dirty pages
- hit rate

## Hints

- The buffer pool caches frequently accessed B-Tree pages in memory to avoid disk I/O
- Use LRU (Least Recently Used) to decide which pages to evict when the pool is full
- Dirty pages (modified but not yet flushed) must be written to disk BEFORE eviction
- Hit rate = cache hits / total reads. A good buffer pool achieves 95%+ hit rates
- This is exactly how PostgreSQL and MySQL manage their shared buffer pool

## Test Cases

### 1. Configure buffer pool size

Input:

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"buffer_pool_config","msg_id":2,"max_pages":100,"page_size_bytes":4096}}
```

Expected output:

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
{"src": "n1", "dest": "c1", "body": {"type": "buffer_pool_config_ok", "in_reply_to": 2, "total_memory_bytes": 409600, "msg_id": 1}}
```

### 2. First read is a cache miss

Input:

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"buffer_pool_config","msg_id":2,"max_pages":10,"page_size_bytes":4096}}
{"src":"c1","dest":"n1","body":{"type":"buffer_pool_read","msg_id":3,"page_id":1}}
```

Expected output:

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
{"src": "n1", "dest": "c1", "body": {"type": "buffer_pool_config_ok", "in_reply_to": 2, "total_memory_bytes": 40960, "msg_id": 1}}
{"src": "n1", "dest": "c1", "body": {"type": "buffer_pool_read_ok", "in_reply_to": 3, "cache_hit": false, "disk_read": true, "msg_id": 2}}
```

## Resources

- [CMU 15-445 Buffer Pool Management](https://15445.courses.cs.cmu.edu/fall2023/slides/05-bufferpool.pdf): Carnegie Mellon database course lecture on buffer pool design and eviction policies

## Java Starter

The matching local starter file is:

```text
src/main/java/Main.java
```
