# 3. The Gossiper

中文名：传播者：Gossip 信息传播

## 按子主题分组

### Naive 广播 (Flooding)

- 1. [`task-3-1-basic-broadcast`](task-3-1-basic-broadcast/TASK.zh-CN.md) - 实现 基础 广播 to All Nodes
- 2. [`task-3-2-tree-topology`](task-3-2-tree-topology/TASK.zh-CN.md) - 构建 Flat Tree Topology Gossip
- 3. [`task-3-3-random-gossip`](task-3-3-random-gossip/TASK.zh-CN.md) - 实现 Peer-to-Peer Gossip，包含Random Neighbors
- 4. [`task-3-4-batching`](task-3-4-batching/TASK.zh-CN.md) - 添加 消息 Batching to Reduce Network Overhead
- 5. [`task-3-5-partition-healing`](task-3-5-partition-healing/TASK.zh-CN.md) -处理Network Partition Healing和Resynchronization

### Gossip Protocol

- 6. [`task-3-2-1-gossip-fanout`](task-3-2-1-gossip-fanout/TASK.zh-CN.md) - 实现 Gossip Fanout，包含Random Peer Selection
- 7. [`task-3-2-2-fanout-probability`](task-3-2-2-fanout-probability/TASK.zh-CN.md) - Calculate Minimum Fanout用于Reliable Delivery
- 8. [`task-3-2-3-gossip-timer`](task-3-2-3-gossip-timer/TASK.zh-CN.md) - 添加 Periodic Gossip Rounds on a Timer
- 9. [`task-3-2-4-anti-entropy`](task-3-2-4-anti-entropy/TASK.zh-CN.md) - 实现 Anti-Entropy，包含Digest Comparison
- 10. [`task-3-2-5-tuning`](task-3-2-5-tuning/TASK.zh-CN.md) - Tune Gossip Parameters用于Maelstrom 广播

### Topology-Aware Gossip

- 11. [`task-3-3-1-tree-broadcast`](task-3-3-1-tree-broadcast/TASK.zh-CN.md) - 实现 Tree-Based 广播 Overlay
- 12. [`task-3-3-2-tree-failure`](task-3-3-2-tree-failure/TASK.zh-CN.md) -处理Tree节点Failure，包含Direct Fallback
- 13. [`task-3-3-3-hybrid-gossip`](task-3-3-3-hybrid-gossip/TASK.zh-CN.md) - 实现 Hybrid Tree和Gossip 广播
- 15. [`task-3-3-5-partition-heal`](task-3-3-5-partition-heal/TASK.zh-CN.md) - Simulate Network Partition和Healing

### Epidemic Algorithms和CRDT Gossip

- 16. [`task-3-4-1-gset`](task-3-4-1-gset/TASK.zh-CN.md) - 实现 Grow-Only Set (G-Set)，包含Gossip
- 17. [`task-3-4-2-twopset`](task-3-4-2-twopset/TASK.zh-CN.md) - 实现 Two-Phase Set (2P-Set)
- 18. [`task-3-4-3-lww-kv`](task-3-4-3-lww-kv/TASK.zh-CN.md) - 实现 Last-Writer-Wins 键值 存储
- 19. [`task-3-4-4-lww-problem`](task-3-4-4-lww-problem/TASK.zh-CN.md) - Demonstrate LWW Data Loss，包含Version Vectors
- 20. [`task-3-4-5-gossip-kv-bench`](task-3-4-5-gossip-kv-bench/TASK.zh-CN.md) - 基准测试 Gossip KV 存储 Performance
