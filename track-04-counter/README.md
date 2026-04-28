# 4. The Counter

中文名：计数器：分布式状态与 CRDT

## 按子主题分组

### The Lost Update Problem

- 1. [`task-4-1-lost-update`](task-4-1-lost-update/TASK.zh-CN.md) - 实现 基础 计数器，包含Lost Update Problem
- 2. [`task-4-2-kv-integration`](task-4-2-kv-integration/TASK.zh-CN.md) - Integrate Sequentially Consistent 键值 存储
- 3. [`task-4-3-cas-operation`](task-4-3-cas-operation/TASK.zh-CN.md) - 实现 Compare-And-Swap (CAS) Operation
- 4. [`task-4-4-g-counter`](task-4-4-g-counter/TASK.zh-CN.md) - 构建 Grow-Only 计数器 (G-计数器) CRDT
- 5. [`task-4-5-concurrent-increments`](task-4-5-concurrent-increments/TASK.zh-CN.md) -处理Concurrent Increments Across Multiple Nodes

### G-计数器和PN-计数器

- 6. [`task-17-2-1-g-counter`](task-17-2-1-g-counter/TASK.zh-CN.md) - 实现 a G-计数器 (Grow-Only CRDT)
- 7. [`task-17-2-2-g-counter-proof`](task-17-2-2-g-counter-proof/TASK.zh-CN.md) - Prove G-计数器 CRDT Properties
- 8. [`task-17-2-3-pn-counter`](task-17-2-3-pn-counter/TASK.zh-CN.md) - 实现 a PN-计数器用于Increment和Decrement
- 9. [`task-17-2-4-gossip-counter`](task-17-2-4-gossip-counter/TASK.zh-CN.md) - Gossip PN-计数器 Across a Cluster
- 10. [`task-17-2-5-maelstrom-counter`](task-17-2-5-maelstrom-counter/TASK.zh-CN.md) - Pass the Maelstrom G-计数器 Workload

### More CRDTs

- 11. [`task-17-3-1-or-set`](task-17-3-1-or-set/TASK.zh-CN.md) - 实现 an OR-Set (Observed-Remove Set)
- 12. [`task-17-3-2-mv-register`](task-17-3-2-mv-register/TASK.zh-CN.md) - 实现 a Multi-Value Register (MV-Register)
- 13. [`task-17-3-3-sequence-crdt`](task-17-3-3-sequence-crdt/TASK.zh-CN.md) - 实现 a Sequence CRDT用于Collaborative Text Editing
- 14. [`task-17-3-4-crdt-tradeoffs`](task-17-3-4-crdt-tradeoffs/TASK.zh-CN.md) - Analyze CRDT Tradeoffs vs. OCC和Locking
- 15. [`task-17-3-5-shopping-cart`](task-17-3-5-shopping-cart/TASK.zh-CN.md) - 构建 a Distributed Shopping Cart，包含CRDTs
