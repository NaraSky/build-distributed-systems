# 2. The Identifier

中文名：标识符：分布式唯一 ID

## 按子主题分组

### Why 唯一 IDs Are Hard

- 1. [`task-2-1-basic-id`](task-2-1-basic-id/TASK.zh-CN.md) - Generate 唯一 IDs使用Node ID和Timestamp
- 2. [`task-2-2-random-salt`](task-2-2-random-salt/TASK.zh-CN.md) - 添加随机Salt to Prevent Collisions
- 3. [`task-2-3-partition-resilient`](task-2-3-partition-resilient/TASK.zh-CN.md) - 实现 ID Generation During Network Partition
- 4. [`task-2-4-uniqueness-validation`](task-2-4-uniqueness-validation/TASK.zh-CN.md) - Validate Uniqueness Across Distributed Nodes
- 5. [`task-2-5-high-throughput`](task-2-5-high-throughput/TASK.zh-CN.md) - Optimize用于High-吞吐量 ID Generation

### Snowflake IDs (Twitter's Approach)

- 6. [`task-2-2-1-bit-layout`](task-2-2-1-bit-layout/TASK.zh-CN.md) - 实现 Snowflake ID Bit Layout
- 7. [`task-2-2-2-timestamp-component`](task-2-2-2-timestamp-component/TASK.zh-CN.md) - 实现 Timestamp Component，包含Custom Epoch
- 8. [`task-2-2-3-sequence-counter`](task-2-2-3-sequence-counter/TASK.zh-CN.md) - 实现 Sequence 计数器，包含Overflow处理
- 10. [`task-2-2-5-multi-node`](task-2-2-5-multi-node/TASK.zh-CN.md) - Multi-Node Snowflake ID Verification

### Logical Clocks as IDs

- 11. [`task-2-3-1-lamport-clock`](task-2-3-1-lamport-clock/TASK.zh-CN.md) - 实现 a Lamport 时钟
- 12. [`task-2-3-2-lamport-limitation`](task-2-3-2-lamport-limitation/TASK.zh-CN.md) - Demonstrate Lamport 时钟 Causality Limitation
- 13. [`task-2-3-3-vector-clock`](task-2-3-3-vector-clock/TASK.zh-CN.md) - 实现 向量 Clocks
- 14. [`task-2-3-4-happened-before`](task-2-3-4-happened-before/TASK.zh-CN.md) - 实现 Happened-Before Detector，包含向量 Clocks
- 15. [`task-2-3-5-vc-conflict-kv`](task-2-3-5-vc-conflict-kv/TASK.zh-CN.md) - 向量 时钟 Conflict Detection in 键值 存储

### 混合逻辑 Clocks (HLC)

- 16. [`task-2-4-1-hlc-format`](task-2-4-1-hlc-format/TASK.zh-CN.md) - Understand和实现 HLC格式
- 17. [`task-2-4-2-hlc-receive`](task-2-4-2-hlc-receive/TASK.zh-CN.md) - 实现 HLC Receive Rule
- 18. [`task-2-4-3-clock-backward`](task-2-4-3-clock-backward/TASK.zh-CN.md) - HLC Handles Backward 时钟 Gracefully
- 19. [`task-2-4-4-id-comparison`](task-2-4-4-id-comparison/TASK.zh-CN.md) - Compare HLC, UUID v4,和Snowflake IDs
- 20. [`task-2-4-5-hlc-unique-ids`](task-2-4-5-hlc-unique-ids/TASK.zh-CN.md) - HLC-Based 唯一 ID Generation用于Maelstrom
