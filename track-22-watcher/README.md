# 22. The Watcher

中文名：观察者：ZooKeeper/etcd 模型

## 按子主题分组

### The ZNode Data模式l

- 1. [`task-15-1-1-znode-tree`](task-15-1-1-znode-tree/TASK.zh-CN.md) - 实现 a ZNode Tree Data模式l
- 2. [`task-15-1-2-crud`](task-15-1-2-crud/TASK.zh-CN.md) - 实现 ZNode CRUD Operations
- 3. [`task-15-1-3-versioning`](task-15-1-3-versioning/TASK.zh-CN.md) - 实现 Optimistic Concurrency，包含Version Checks
- 4. [`task-15-1-4-ephemeral`](task-15-1-4-ephemeral/TASK.zh-CN.md) - 实现 Ephemeral Nodes用于Session-Bound State
- 5. [`task-15-1-5-sequential`](task-15-1-5-sequential/TASK.zh-CN.md) - 实现 Sequential Nodes用于Ordering

### Watches和Sessions

- 6. [`task-15-2-1-watches`](task-15-2-1-watches/TASK.zh-CN.md) - 实现 One-Shot Watches用于Change Notification
- 7. [`task-15-2-2-sessions`](task-15-2-2-sessions/TASK.zh-CN.md) - 实现 Client Session Management
- 8. [`task-15-2-3-distributed-lock`](task-15-2-3-distributed-lock/TASK.zh-CN.md) - 构建 a Distributed Lock，包含ZooKeeper Primitives
- 9. [`task-15-2-4-leader-election`](task-15-2-4-leader-election/TASK.zh-CN.md) - 构建 Leader 选举，包含ZooKeeper
- 10. [`task-15-2-5-service-discovery`](task-15-2-5-service-discovery/TASK.zh-CN.md) - 构建 a 服务 Discovery System

### Consistency和the ZAB Protocol

- 11. [`task-15-3-1-zab`](task-15-3-1-zab/TASK.zh-CN.md) - 实现 ZAB Atomic 广播 Protocol
- 12. [`task-15-3-2-zab-leader-election`](task-15-3-2-zab-leader-election/TASK.zh-CN.md) - 实现 ZAB Leader 选举，包含FastLeaderElection
- 13. [`task-15-3-3-sequential-consistency`](task-15-3-3-sequential-consistency/TASK.zh-CN.md) - Prove ZAB Sequential Consistency
- 14. [`task-15-3-4-etcd-api`](task-15-3-4-etcd-api/TASK.zh-CN.md) - 实现 an etcd-Compatible API Layer
- 15. [`task-15-3-5-mvcc`](task-15-3-5-mvcc/TASK.zh-CN.md) - 实现 etcd MVCC用于Versioned 键值 存储
