# 23. The Searcher

中文名：搜索器：分布式搜索

## 按子主题分组

### Document模式l和Mapping

- 1. [`task-16-1-1-document-store`](task-16-1-1-document-store/TASK.zh-CN.md) - 实现 a JSON Document 存储
- 2. [`task-16-1-2-schema-mapping`](task-16-1-2-schema-mapping/TASK.zh-CN.md) - 实现 Schema Mapping，包含Field Types
- 3. [`task-16-1-3-text-analysis`](task-16-1-3-text-analysis/TASK.zh-CN.md) - 实现 a Text Analysis Pipeline
- 4. [`task-16-1-4-dynamic-mapping`](task-16-1-4-dynamic-mapping/TASK.zh-CN.md) - 实现 Dynamic Mapping，包含Type Auto-Detection
- 5. [`task-16-1-5-search-api`](task-16-1-5-search-api/TASK.zh-CN.md) - 实现 a Full-Text Search API

### Distributed Sharding和复制

- 6. [`task-16-2-1-shard-routing`](task-16-2-1-shard-routing/TASK.zh-CN.md) - 实现 Document Sharding，包含Hash-Based Routing
- 7. [`task-16-2-2-replica-shards`](task-16-2-2-replica-shards/TASK.zh-CN.md) - 添加 Replica Shards用于Fault Tolerance
- 8. [`task-16-2-3-scatter-gather`](task-16-2-3-scatter-gather/TASK.zh-CN.md) - 实现 Scatter-Gather Search Across Shards
- 9. [`task-16-2-4-shard-rebalance`](task-16-2-4-shard-rebalance/TASK.zh-CN.md) - 实现 分片 Rebalancing on节点Join
- 10. [`task-16-2-5-node-failure`](task-16-2-5-node-failure/TASK.zh-CN.md) -处理Node Failure，包含Replica Promotion
