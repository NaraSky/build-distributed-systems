# 7. The Store

中文名：存储：线性一致 KV Store

## 按子主题分组

### Linearizable 键值 存储

- 1. [`task-7-1-kv-interface`](task-7-1-kv-interface/TASK.zh-CN.md) - 实现 键值 Interface
- 2. [`task-7-2-client-routing`](task-7-2-client-routing/TASK.zh-CN.md) -处理Client Request Routing
- 3. [`task-7-3-read-consistency`](task-7-3-read-consistency/TASK.zh-CN.md) - Ensure Read Consistency
- 4. [`task-7-4-client-dedup`](task-7-4-client-dedup/TASK.zh-CN.md) -处理Client 重试和去重
- 5. [`task-7-5-snapshots`](task-7-5-snapshots/TASK.zh-CN.md) - 实现 日志 Compaction，包含Snapshots

### Read Optimization

- 6. [`task-8-2-1-read-index`](task-8-2-1-read-index/TASK.zh-CN.md) - 实现 Read 索引用于Linearizable Reads
- 7. [`task-8-2-2-lease-reads`](task-8-2-2-lease-reads/TASK.zh-CN.md) - 实现 Lease-Based Reads
- 8. [`task-8-2-3-follower-reads`](task-8-2-3-follower-reads/TASK.zh-CN.md) - 添加 Follower Reads，包含Bounded Staleness
- 9. [`task-8-2-4-read-your-writes`](task-8-2-4-read-your-writes/TASK.zh-CN.md) - Guarantee Read-Your-Writes，包含Follower Reads
- 10. [`task-8-2-5-read-benchmark`](task-8-2-5-read-benchmark/TASK.zh-CN.md) - 基准测试 Read Strategies Under Mixed Workload

### Transactions on Raft

- 11. [`task-8-3-1-multi-key-txn`](task-8-3-1-multi-key-txn/TASK.zh-CN.md) - 实现 Multi-Key Transactions as Atomic 日志 Entries
- 12. [`task-8-3-2-occ`](task-8-3-2-occ/TASK.zh-CN.md) - 实现 Optimistic Concurrency Control
- 13. [`task-8-3-3-mvcc`](task-8-3-3-mvcc/TASK.zh-CN.md) - 实现 Multi-Version Concurrency Control
- 14. [`task-8-3-4-tikv-regions`](task-8-3-4-tikv-regions/TASK.zh-CN.md) - 构建 a Mini TiKV，包含Raft + MVCC Regions
- 15. [`task-8-3-5-contention-benchmark`](task-8-3-5-contention-benchmark/TASK.zh-CN.md) - 基准测试 Contended Key Under OCC vs MVCC
