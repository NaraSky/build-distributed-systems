# 9. The Coordinator

中文名：协调器：分布式事务

## 按子主题分组

### Two-Phase Commit

- 1. [`task-9-1-two-phase-commit`](task-9-1-two-phase-commit/TASK.zh-CN.md) - 实现 Two-Phase Commit
- 2. [`task-9-2-coordinator-failure`](task-9-2-coordinator-failure/TASK.zh-CN.md) -处理Coordinator Failure
- 3. [`task-9-3-three-phase-commit`](task-9-3-three-phase-commit/TASK.zh-CN.md) - 实现 Three-Phase Commit
- 4. [`task-9-4-sagas`](task-9-4-sagas/TASK.zh-CN.md) - 实现 Saga Pattern
- 5. [`task-9-5-txn-kv`](task-9-5-txn-kv/TASK.zh-CN.md) - 构建 Transactional 键值 存储

### Three-Phase Commit (3PC)

- 6. [`task-19-2-1-three-phase`](task-19-2-1-three-phase/TASK.zh-CN.md) - 实现 Three-Phase Commit Protocol
- 7. [`task-19-2-2-unblocking`](task-19-2-2-unblocking/TASK.zh-CN.md) - Show How 3PC Unblocks 2PC Scenarios
- 8. [`task-19-2-3-network-partition`](task-19-2-3-network-partition/TASK.zh-CN.md) - Show 3PC Blocking Under Network Partition
- 9. [`task-19-2-4-comparison`](task-19-2-4-comparison/TASK.zh-CN.md) - Compare 2PC vs 3PC Protocols
- 10. [`task-19-2-5-paxos-commit`](task-19-2-5-paxos-commit/TASK.zh-CN.md) - 实现 Paxos Commit Protocol

### Saga Pattern

- 11. [`task-19-3-1-saga-fundamentals`](task-19-3-1-saga-fundamentals/TASK.zh-CN.md) - 实现 Saga Pattern，包含Compensating Transactions
- 12. [`task-19-3-2-choreography`](task-19-3-2-choreography/TASK.zh-CN.md) - 实现 Choreography-Based Saga
- 13. [`task-19-3-3-orchestration`](task-19-3-3-orchestration/TASK.zh-CN.md) - 实现 Orchestration-Based Saga
- 14. [`task-19-3-4-idempotency`](task-19-3-4-idempotency/TASK.zh-CN.md) - 实现 Idempotency in Sagas
- 15. [`task-19-3-5-shopping-cart`](task-19-3-5-shopping-cart/TASK.zh-CN.md) - 实现 E-Commerce Checkout Saga
