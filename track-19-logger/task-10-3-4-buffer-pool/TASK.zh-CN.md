# 实现带 LRU 淘汰策略的缓冲池

英文标题：Implement a Buffer Pool with LRU Eviction
网页：<https://builddistributedsystem.com/tracks/logger/tasks/task-10-3-4-buffer-pool>

课程：19. 日志器：WAL、LSM 与分布式日志
任务序号：14
短标题：Buffer Pool
难度：高级
子主题：B-Tree on Disk

## 中文导读

本题要求你实现一个缓冲池（Buffer Pool），把频繁访问的 B 树页面缓存在内存中，并在内存满时使用 LRU（最近最少使用）策略淘汰旧页面。这正是 PostgreSQL、MySQL 等生产数据库实现高性能的核心机制——磁盘读写比内存慢约 1000 倍，缓冲池就是弥补这一差距的桥梁。

## 题目说明

磁盘读写的速度比内存访问慢大约 1000 倍。缓冲池（Buffer Pool）通过将频繁访问的 B 树页面缓存到内存中来弥补这一差距。所有生产级数据库（PostgreSQL、MySQL、Oracle）都依赖缓冲池来达到可接受的性能。

缓冲池的设计要点：
1. **固定大小的内存区域**：可容纳 N 个页面（例如 100 个页面 * 4KB = 400KB）
2. **页表**：建立 page_id 到 frame_number 的映射，实现 O(1) 查找
3. **LRU 淘汰策略**：当需要加载新页面但缓冲池已满时，淘汰最近最少使用的页面
4. **脏页追踪**：在内存中被修改过的页面标记为"脏页（Dirty Page）"。淘汰脏页之前，必须先将它写回磁盘
5. **命中率监控**：追踪缓存命中次数与总读取次数的比值。高命中率（大于 95%）说明工作集可以装入内存

淘汰策略的选择至关重要：
- LRU 对大多数负载表现良好，但面对顺序扫描时容易失效（一次全表扫描可能把整个缓存冲掉）
- MySQL 使用"年轻"和"老年"两个子链表来防止这种情况
- PostgreSQL 使用时钟扫描算法（近似 LRU）

```json
Request:  {"type": "buffer_pool_config", "msg_id": 1, "max_pages": 100, "page_size_bytes": 4096}
Response: {"type": "buffer_pool_config_ok", "in_reply_to": 1, "total_memory_bytes": 409600}

Request:  {"type": "buffer_pool_read", "msg_id": 2, "page_id": 42}
Response: {"type": "buffer_pool_read_ok", "in_reply_to": 2, "cache_hit": false, "disk_read": true}

Request:  {"type": "buffer_pool_stats", "msg_id": 3}
Response: {"type": "buffer_pool_stats_ok", "in_reply_to": 3, "total_reads": 1000, "cache_hits": 850, "hit_rate": 0.85, "dirty_pages": 12, "evictions": 50}
```

## 涉及概念

- `buffer pool`
- `LRU eviction`
- `page cache`
- `dirty pages`
- `hit rate`

## 实现提示

- 缓冲池将频繁访问的 B 树页面缓存在内存中，以减少磁盘读写
- 使用 LRU（最近最少使用）算法决定当缓冲池满时淘汰哪个页面
- 脏页（已修改但尚未写回磁盘的页面）在被淘汰之前必须先写回磁盘
- 命中率 = 缓存命中次数 / 总读取次数。好的缓冲池应达到 95% 以上的命中率
- 这正是 PostgreSQL 和 MySQL 管理共享缓冲池的方式

## 测试用例

### 1. 配置缓冲池大小

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

### 2. 首次读取应为缓存未命中

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

- [CMU 15-445 Buffer Pool Management](https://15445.courses.cs.cmu.edu/fall2023/slides/05-bufferpool.pdf)：卡内基梅隆大学数据库课程关于缓冲池设计和淘汰策略的讲义

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
