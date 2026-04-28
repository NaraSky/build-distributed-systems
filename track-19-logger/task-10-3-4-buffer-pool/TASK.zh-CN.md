# 实现 a Buffer Pool，包含LRU Eviction

英文标题：Implement a Buffer Pool，包含LRU Eviction
网页：<https://builddistributedsystem.com/tracks/logger/tasks/task-10-3-4-buffer-pool>

课程：19. 日志器：WAL、LSM 与分布式日志
任务序号：14
短标题：Buffer Pool
难度：advanced
子主题：B-Tree on Disk

## 中文导读

本题要求你完成 `实现 a Buffer Pool，包含LRU Eviction`。

重点关注：`buffer pool`、`LRU eviction`、`page cache`、`dirty pages`、`hit rate`。

建议先按提示逐步实现：The buffer pool caches frequently accessed B-Tree pages in memory to avoid disk I/O。

协议字段、消息类型、输入输出格式请以本文件中的代码块和测试用例为准。

## 题目说明

Disk I/O is 1000x slower than memory access. The buffer pool bridges this gap by caching frequently accessed B-Tree pages in RAM. This is how every production database (PostgreSQL, MySQL, Oracle) achieves acceptable performance.

Buffer pool design:
1. **Fixed-size memory region**: holds N pages (e.g. 100 pages * 4KB = 400KB)
2. **Page table**: maps (page_id -> frame_number)用于O(1) lookup
3. **LRU eviction**: when a new page is needed but the pool is full, evict the least recently used page
4. **Dirty page tracking**: pages modified in memory are marked "dirty". Before evicting a dirty page, flush it to disk.
5. **Hit rate monitoring**: track the ratio of 缓存 hits to total reads. High hit rates (>95%) mean the working set fits in memory.

The eviction policy is critical:
- LRU works well用于most workloads but is vulnerable to sequential scans (a full table scan can evict the entire 缓存)
- MySQL uses a "young"和"old" sublist to protect against this
- PostgreSQL uses a 时钟 sweep algorithm (approximated LRU)

```JSON
请求:  {"type": "buffer_pool_config", "msg_id": 1, "max_pages": 100, "page_size_bytes": 4096}
响应: {"type": "buffer_pool_config_ok", "in_reply_to": 1, "total_memory_bytes": 409600}

请求:  {"type": "buffer_pool_read", "msg_id": 2, "page_id": 42}
响应: {"type": "buffer_pool_read_ok", "in_reply_to": 2, "cache_hit": false, "disk_read": true}

请求:  {"type": "buffer_pool_stats", "msg_id": 3}
响应: {"type": "buffer_pool_stats_ok", "in_reply_to": 3, "total_reads": 1000, "cache_hits": 850, "hit_rate": 0.85, "dirty_pages": 12, "evictions": 50}
```

## 涉及概念

- `buffer pool`
- `LRU eviction`
- `page cache`
- `dirty pages`
- `hit rate`

## 实现提示

- The buffer pool caches frequently accessed B-Tree pages in memory to avoid disk I/O
- Use LRU (Least Recently Used) to decide which pages to evict when the pool is full
- Dirty pages (modified but not yet flushed) must be written to disk BEFORE eviction
- Hit rate = 缓存 hits / total reads. A good buffer pool achieves 95%+ hit rates
- This is exactly how PostgreSQL和MySQL manage their shared buffer pool

## 测试用例

### 1. Configure buffer pool size

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"buffer_pool_config","msg_id":2,"max_pages":100,"page_size_bytes":4096}}
```

期望输出：

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
{"src": "n1", "dest": "c1", "body": {"type": "buffer_pool_config_ok", "in_reply_to": 2, "total_memory_bytes": 409600, "msg_id": 1}}
```

### 2. First read is a 缓存 miss

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"buffer_pool_config","msg_id":2,"max_pages":10,"page_size_bytes":4096}}
{"src":"c1","dest":"n1","body":{"type":"buffer_pool_read","msg_id":3,"page_id":1}}
```

期望输出：

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
{"src": "n1", "dest": "c1", "body": {"type": "buffer_pool_config_ok", "in_reply_to": 2, "total_memory_bytes": 40960, "msg_id": 1}}
{"src": "n1", "dest": "c1", "body": {"type": "buffer_pool_read_ok", "in_reply_to": 3, "cache_hit": false, "disk_read": true, "msg_id": 2}}
```

## 参考资料

- [CMU 15-445 Buffer Pool Management](https://15445.courses.cs.cmu.edu/fall2023/slides/05-bufferpool.pdf)：Carnegie Mellon database course lecture on buffer pool design和eviction policies

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
