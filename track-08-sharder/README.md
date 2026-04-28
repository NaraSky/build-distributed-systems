# 8. The Sharder

中文名：分片器：水平扩展与数据迁移

## 按子主题分组

### Range Sharding

- 1. [`task-8-1-shard-controller`](task-8-1-shard-controller/TASK.zh-CN.md) - 实现 分片 Controller
- 2. [`task-8-2-consistent-hash`](task-8-2-consistent-hash/TASK.zh-CN.md) - 实现 Consistent Hashing用于Sharding
- 3. [`task-8-3-config-change`](task-8-3-config-change/TASK.zh-CN.md) -处理Configuration Changes
- 4. [`task-8-4-data-migration`](task-8-4-data-migration/TASK.zh-CN.md) - 实现 Data Migration
- 5. [`task-8-5-sharded-kv`](task-8-5-sharded-kv/TASK.zh-CN.md) - 构建 Complete Sharded 键值 存储

### Consistent Hashing

- 6. [`task-18-2-1-hash-ring`](task-18-2-1-hash-ring/TASK.zh-CN.md) - 实现 a Consistent Hash Ring
- 7. [`task-18-2-2-virtual-nodes`](task-18-2-2-virtual-nodes/TASK.zh-CN.md) - 添加 Virtual Nodes用于Even Distribution
- 8. [`task-18-2-3-node-join`](task-18-2-3-node-join/TASK.zh-CN.md) -处理Node Addition，包含Minimal Key Migration
- 9. [`task-18-2-4-node-removal`](task-18-2-4-node-removal/TASK.zh-CN.md) -处理Node Removal，包含Graceful和Crash Recovery
- 10. [`task-18-2-5-rendezvous-hashing`](task-18-2-5-rendezvous-hashing/TASK.zh-CN.md) - 实现 Rendezvous Hashing (Highest随机Weight)

### Cross-分片 Queries

- 11. [`task-18-3-1-scatter-gather`](task-18-3-1-scatter-gather/TASK.zh-CN.md) - 实现 Scatter-Gather Query Execution
- 12. [`task-18-3-2-aggregations`](task-18-3-2-aggregations/TASK.zh-CN.md) - 实现 Cross-分片 Aggregations
- 13. [`task-18-3-3-joins`](task-18-3-3-joins/TASK.zh-CN.md) - 实现 Cross-分片 JOINs
- 14. [`task-18-3-4-secondary-indexes`](task-18-3-4-secondary-indexes/TASK.zh-CN.md) - 实现 Secondary Indexes on Sharded Data
- 15. [`task-18-3-5-order-limit`](task-18-3-5-order-limit/TASK.zh-CN.md) - 实现 Distributed ORDER BY，包含LIMIT
