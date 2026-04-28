# 6. The Consensus

中文名：共识：Raft 与日志复制

## 按子主题分组

### Raft 日志 复制

- 1. [`task-6-1-log-replication`](task-6-1-log-replication/TASK.zh-CN.md) - 实现 日志 复制
- 2. [`task-6-2-log-matching`](task-6-2-log-matching/TASK.zh-CN.md) - Ensure 日志 Matching Property
- 3. [`task-6-3-commitment`](task-6-3-commitment/TASK.zh-CN.md) - 实现 Entry Commitment
- 4. [`task-6-4-state-machine`](task-6-4-state-machine/TASK.zh-CN.md) - Apply Committed Entries to State Machine
- 5. [`task-6-5-safety`](task-6-5-safety/TASK.zh-CN.md) - 实现 选举 Restriction用于Safety

### Commitment和Application

- 6. [`task-7-2-1-commit-rule`](task-7-2-1-commit-rule/TASK.zh-CN.md) - 实现 the Raft Commitment Rule
- 7. [`task-7-2-2-apply-channel`](task-7-2-2-apply-channel/TASK.zh-CN.md) - 实现 the Apply Channel用于State Machine
- 8. [`task-7-2-3-noop-on-election`](task-7-2-3-noop-on-election/TASK.zh-CN.md) -处理Leader Changes，包含No-Op on 选举
- 9. [`task-7-2-4-snapshot`](task-7-2-4-snapshot/TASK.zh-CN.md) - 添加 Snapshot Support用于日志 Compaction
- 10. [`task-7-2-5-lin-kv-partition`](task-7-2-5-lin-kv-partition/TASK.zh-CN.md) - Pass Linearizable KV，包含Network Partitions

### Paxos

- 11. [`task-7-3-1-single-decree`](task-7-3-1-single-decree/TASK.zh-CN.md) - 实现 Single-Decree Paxos Phase 1 (Prepare/Promise)
- 12. [`task-7-3-2-accept-phase`](task-7-3-2-accept-phase/TASK.zh-CN.md) - 实现 Paxos Phase 2 (Accept/Accepted)
- 13. [`task-7-3-3-paxos-safety`](task-7-3-3-paxos-safety/TASK.zh-CN.md) - Prove Paxos Safety: Chosen Values Are Immutable
- 14. [`task-7-3-4-multi-paxos`](task-7-3-4-multi-paxos/TASK.zh-CN.md) - 实现 Multi-Paxos用于an Infinite 日志
- 15. [`task-7-3-5-raft-vs-paxos`](task-7-3-5-raft-vs-paxos/TASK.zh-CN.md) - Compare Raft vs Multi-Paxos

### Byzantine Fault Tolerance

- 16. [`task-7-4-1-byzantine-faults`](task-7-4-1-byzantine-faults/TASK.zh-CN.md) - Understand Byzantine Faults，包含Real-World Examples
- 17. [`task-7-4-2-pbft-impl`](task-7-4-2-pbft-impl/TASK.zh-CN.md) - 实现 Simplified PBFT，包含4 Nodes
- 18. [`task-7-4-3-equivocation-defense`](task-7-4-3-equivocation-defense/TASK.zh-CN.md) - Detect和Handle Equivocation Attacks
- 19. [`task-7-4-4-bft-threshold`](task-7-4-4-bft-threshold/TASK.zh-CN.md) - Prove the N >= 3f+1 Byzantine Fault Threshold
- 20. [`task-7-4-5-tendermint`](task-7-4-5-tendermint/TASK.zh-CN.md) - 实现 Tendermint-Style BFT Voting Rounds
