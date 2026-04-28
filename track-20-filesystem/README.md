# 20. The Filesystem

中文名：文件系统：分布式文件存储

## 按子主题分组

### Distributed File Storage

- 1. [`task-12-1-1-architecture`](task-12-1-1-architecture/TASK.zh-CN.md) - Design a GFS-Style Distributed File System Architecture
- 2. [`task-12-1-2-namespace`](task-12-1-2-namespace/TASK.zh-CN.md) - 实现 the Master Namespace Tree
- 3. [`task-12-1-3-chunk-creation`](task-12-1-3-chunk-creation/TASK.zh-CN.md) - 实现 Chunk Creation和Allocation
- 4. [`task-12-1-4-chunk-replication`](task-12-1-4-chunk-replication/TASK.zh-CN.md) - 实现 Chunk 复制，包含Pipeline Writes
- 5. [`task-12-1-5-chunk-lease`](task-12-1-5-chunk-lease/TASK.zh-CN.md) - 实现 Chunk Leases用于Primary Assignment

### Fault Tolerance和Rebalancing

- 6. [`task-12-2-1-heartbeats`](task-12-2-1-heartbeats/TASK.zh-CN.md) - 实现 Chunk Server Heartbeats
- 7. [`task-12-2-2-re-replication`](task-12-2-2-re-replication/TASK.zh-CN.md) - 实现 Automatic Re-复制
- 8. [`task-12-2-3-load-balancing`](task-12-2-3-load-balancing/TASK.zh-CN.md) - 实现 Chunk Server Load Balancing
- 9. [`task-12-2-4-master-failover`](task-12-2-4-master-failover/TASK.zh-CN.md) - 实现 Master Failover，包含Shadow Master
- 10. [`task-12-2-5-checksums`](task-12-2-5-checksums/TASK.zh-CN.md) - 实现 Chunk Checksums用于Data Integrity
