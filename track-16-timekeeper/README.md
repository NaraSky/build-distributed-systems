# 16. The Timekeeper

中文名：时间守卫：逻辑时钟

## 按子主题分组

### Physical Time和Its Failures

- 1. [`task-4-1-1-clock-read`](task-4-1-1-clock-read/TASK.zh-CN.md) - Read System 时钟和Detect Backward Jumps
- 2. [`task-4-1-2-monotonic-clock`](task-4-1-2-monotonic-clock/TASK.zh-CN.md) - 实现 Monotonic 时钟 Wrapper
- 3. [`task-4-1-3-split-brain-lease`](task-4-1-3-split-brain-lease/TASK.zh-CN.md) - Simulate Split-Brain Caused by 时钟 Drift
- 4. [`task-4-1-4-truetime-mock`](task-4-1-4-truetime-mock/TASK.zh-CN.md) - 实现 Mock TrueTime API
- 5. [`task-4-1-5-wait-out-uncertainty`](task-4-1-5-wait-out-uncertainty/TASK.zh-CN.md) - Wait-Out-Uncertainty用于External Consistency

### Lamport Clocks

- 6. [`task-4-2-1-lamport-basic`](task-4-2-1-lamport-basic/TASK.zh-CN.md) - 实现 a Lamport 时钟 from Scratch
- 7. [`task-4-2-2-causality-proof`](task-4-2-2-causality-proof/TASK.zh-CN.md) - Prove Lamport 时钟 Causality和Its Limitation
- 8. [`task-4-2-3-lamport-mutex`](task-4-2-3-lamport-mutex/TASK.zh-CN.md) - 实现 Distributed Mutual Exclusion，包含Lamport Clocks
- 9. [`task-4-2-4-mutex-contention`](task-4-2-4-mutex-contention/TASK.zh-CN.md) - Simulate并发Mutex Requests from Multiple Nodes
- 10. [`task-4-2-5-mutex-comparison`](task-4-2-5-mutex-comparison/TASK.zh-CN.md) - Compare Mutex Algorithms: Lamport vs Token Ring vs Centralized

### 向量 Clocks

- 11. [`task-4-3-1-vector-clock-impl`](task-4-3-1-vector-clock-impl/TASK.zh-CN.md) - 实现 向量 Clocks
- 12. [`task-4-3-2-happens-before`](task-4-3-2-happens-before/TASK.zh-CN.md) - 实现 Happens-Before和Concurrency Detection
- 13. [`task-4-3-3-causal-chat`](task-4-3-3-causal-chat/TASK.zh-CN.md) - 构建 a Causal-Order Chat System
- 14. [`task-4-3-4-dotted-version-vectors`](task-4-3-4-dotted-version-vectors/TASK.zh-CN.md) - 实现 Dotted Version Vectors
- 15. [`task-4-3-5-conflict-kv`](task-4-3-5-conflict-kv/TASK.zh-CN.md) - 构建 a Conflict-Detecting 键值 存储

### 混合逻辑 Clocks

- 16. [`task-4-4-1-hlc-impl`](task-4-4-1-hlc-impl/TASK.zh-CN.md) - 实现 混合逻辑 Clocks
- 17. [`task-4-4-2-hlc-causality-bound`](task-4-4-2-hlc-causality-bound/TASK.zh-CN.md) - Prove HLC Preserves Causality Within Epsilon
- 18. [`task-4-4-3-hlc-lock`](task-4-4-3-hlc-lock/TASK.zh-CN.md) - 实现 a Distributed Lock使用HLC时间戳
- 19. [`task-4-4-4-time-oracle`](task-4-4-4-time-oracle/TASK.zh-CN.md) - 构建 a Time Oracle 服务，包含Failover
- 20. [`task-4-4-5-clock-comparison-adr`](task-4-4-5-clock-comparison-adr/TASK.zh-CN.md) - Architecture Decision Record: Choosing a 时钟 System
