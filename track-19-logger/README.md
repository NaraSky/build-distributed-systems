# 19. The Logger

中文名：日志器：WAL、LSM 与分布式日志

## 按子主题分组

### The Commit 日志 (WAL)

- 1. [`task-10-1-1-wal-impl`](task-10-1-1-wal-impl/TASK.zh-CN.md) - 实现 a Write-Ahead 日志
- 2. [`task-10-1-2-wal-recovery`](task-10-1-2-wal-recovery/TASK.zh-CN.md) - 实现 WAL Recovery on Startup
- 3. [`task-10-1-3-segments`](task-10-1-3-segments/TASK.zh-CN.md) - 添加 WAL Segment Files，包含Offset 索引
- 4. [`task-10-1-4-compaction`](task-10-1-4-compaction/TASK.zh-CN.md) - 实现 WAL Compaction，包含Atomic Snapshot
- 5. [`task-10-1-5-fsync-bench`](task-10-1-5-fsync-bench/TASK.zh-CN.md) - 基准测试 WAL fsync Strategies

### LSM Tree (日志-Structured Merge Tree)

- 6. [`task-10-2-1-memtable`](task-10-2-1-memtable/TASK.zh-CN.md) - 实现 an In-Memory MemTable
- 7. [`task-10-2-2-sstable-flush`](task-10-2-2-sstable-flush/TASK.zh-CN.md) - 实现 SSTable Flush，包含Bloom Filter
- 8. [`task-10-2-3-multi-level`](task-10-2-3-multi-level/TASK.zh-CN.md) - 实现 a Multi-Level LSM Tree
- 9. [`task-10-2-4-compaction`](task-10-2-4-compaction/TASK.zh-CN.md) - 实现 LSM Compaction，包含Merge Sort
- 10. [`task-10-2-5-lsm-bench`](task-10-2-5-lsm-bench/TASK.zh-CN.md) - 基准测试 LSM Tree vs B-Tree Performance

### B-Tree on Disk

- 11. [`task-10-3-1-btree-node`](task-10-3-1-btree-node/TASK.zh-CN.md) - 实现 a B-Tree Node和Search
- 12. [`task-10-3-2-btree-insert`](task-10-3-2-btree-insert/TASK.zh-CN.md) - 实现 B-Tree Insert，包含Node Splits
- 13. [`task-10-3-3-btree-delete`](task-10-3-3-btree-delete/TASK.zh-CN.md) - 实现 B-Tree Delete，包含Merge和Borrow
- 14. [`task-10-3-4-buffer-pool`](task-10-3-4-buffer-pool/TASK.zh-CN.md) - 实现 a Buffer Pool，包含LRU Eviction
- 15. [`task-10-3-5-btree-vs-lsm`](task-10-3-5-btree-vs-lsm/TASK.zh-CN.md) - Compare B-Tree vs LSM Tree，包含Amplification Metrics

### Distributed 日志 (Kafka Architecture)

- 16. [`task-10-4-1-partition-log`](task-10-4-1-partition-log/TASK.zh-CN.md) -模式l a Kafka Partition as a Write-Ahead 日志
- 17. [`task-10-4-2-consumer-offsets`](task-10-4-2-consumer-offsets/TASK.zh-CN.md) - 实现 Consumer Group Offset Tracking
- 18. [`task-10-4-3-partition-leader`](task-10-4-3-partition-leader/TASK.zh-CN.md) - 实现 Partition Leader 选举 via Raft
- 19. [`task-10-4-4-isr`](task-10-4-4-isr/TASK.zh-CN.md) - 实现 In-Sync Replicas (ISR) Management
- 20. [`task-10-4-5-consumer-rebalance`](task-10-4-5-consumer-rebalance/TASK.zh-CN.md) - 实现 Consumer Group Rebalancing
