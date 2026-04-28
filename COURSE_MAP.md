# Course Map

Website: <https://builddistributedsystem.com/tracks>

本文件是本地课程总目录。

## 1. 信使：消息通信基础

本地目录：`track-01-messenger`

### Hello, Distributed World

- 1. [`task-1-1-json-parser`](track-01-messenger/task-1-1-json-parser/TASK.zh-CN.md) - 实现 基础 JSON 消息 解析器
- 2. [`task-1-2-init-handler`](track-01-messenger/task-1-2-init-handler/TASK.zh-CN.md) -处理初始化 消息和存储集群元数据
- 3. [`task-1-3-echo-service`](track-01-messenger/task-1-3-echo-service/TASK.zh-CN.md) - 实现 回声 服务，包含正确的 确认响应
- 4. [`task-1-4-envelope-validation`](track-01-messenger/task-1-4-envelope-validation/TASK.zh-CN.md) - 添加 消息 信封 校验
- 5. [`task-1-5-async-handler`](track-01-messenger/task-1-5-async-handler/TASK.zh-CN.md) - 创建 异步 事件循环用于Concurrent 消息处理

### RPC和the Request-Response模式l

- 6. [`task-1-2-1-sync-rpc`](track-01-messenger/task-1-2-1-sync-rpc/TASK.zh-CN.md) - 实现 同步 RPC，包含超时
- 7. [`task-1-2-2-timeout-retry`](track-01-messenger/task-1-2-2-timeout-retry/TASK.zh-CN.md) - 实现 超时和重试循环用于RPC
- 8. [`task-1-2-3-async-rpc`](track-01-messenger/task-1-2-3-async-rpc/TASK.zh-CN.md) - 实现 异步 RPC使用Callbacks
- 9. [`task-1-2-4-callback-reaper`](track-01-messenger/task-1-2-4-callback-reaper/TASK.zh-CN.md) - 实现 回调 清理器用于Leaked RPCs
- 10. [`task-1-2-5-exponential-backoff`](track-01-messenger/task-1-2-5-exponential-backoff/TASK.zh-CN.md) - 实现 指数退避用于Retries

### The Protocol Beneath

- 11. [`task-1-3-1-typed-schema`](track-01-messenger/task-1-3-1-typed-schema/TASK.zh-CN.md) -模式l 消息格式，包含类型化模式
- 12. [`task-1-3-2-envelope-logger`](track-01-messenger/task-1-3-2-envelope-logger/TASK.zh-CN.md) - 添加 消息 信封 日志器，包含Timestamps
- 13. [`task-1-3-3-deduplication`](track-01-messenger/task-1-3-3-deduplication/TASK.zh-CN.md) - 实现 消息 去重，包含LRU 缓存
- 14. [`task-1-3-4-throughput-bench`](track-01-messenger/task-1-3-4-throughput-bench/TASK.zh-CN.md) - 基准测试节点吞吐量和延迟
- 15. [`task-1-3-5-chaos-mode`](track-01-messenger/task-1-3-5-chaos-mode/TASK.zh-CN.md) - 添加 混沌模式，包含Random 消息丢弃

## 2. 标识符：分布式唯一 ID

本地目录：`track-02-identifier`

### Why 唯一 IDs Are Hard

- 1. [`task-2-1-basic-id`](track-02-identifier/task-2-1-basic-id/TASK.zh-CN.md) - Generate 唯一 IDs使用Node ID和Timestamp
- 2. [`task-2-2-random-salt`](track-02-identifier/task-2-2-random-salt/TASK.zh-CN.md) - 添加随机Salt to Prevent Collisions
- 3. [`task-2-3-partition-resilient`](track-02-identifier/task-2-3-partition-resilient/TASK.zh-CN.md) - 实现 ID Generation During Network Partition
- 4. [`task-2-4-uniqueness-validation`](track-02-identifier/task-2-4-uniqueness-validation/TASK.zh-CN.md) - Validate Uniqueness Across Distributed Nodes
- 5. [`task-2-5-high-throughput`](track-02-identifier/task-2-5-high-throughput/TASK.zh-CN.md) - Optimize用于High-吞吐量 ID Generation

### Snowflake IDs (Twitter's Approach)

- 6. [`task-2-2-1-bit-layout`](track-02-identifier/task-2-2-1-bit-layout/TASK.zh-CN.md) - 实现 Snowflake ID Bit Layout
- 7. [`task-2-2-2-timestamp-component`](track-02-identifier/task-2-2-2-timestamp-component/TASK.zh-CN.md) - 实现 Timestamp Component，包含Custom Epoch
- 8. [`task-2-2-3-sequence-counter`](track-02-identifier/task-2-2-3-sequence-counter/TASK.zh-CN.md) - 实现 Sequence 计数器，包含Overflow处理
- 10. [`task-2-2-5-multi-node`](track-02-identifier/task-2-2-5-multi-node/TASK.zh-CN.md) - Multi-Node Snowflake ID Verification

### Logical Clocks as IDs

- 11. [`task-2-3-1-lamport-clock`](track-02-identifier/task-2-3-1-lamport-clock/TASK.zh-CN.md) - 实现 a Lamport 时钟
- 12. [`task-2-3-2-lamport-limitation`](track-02-identifier/task-2-3-2-lamport-limitation/TASK.zh-CN.md) - Demonstrate Lamport 时钟 Causality Limitation
- 13. [`task-2-3-3-vector-clock`](track-02-identifier/task-2-3-3-vector-clock/TASK.zh-CN.md) - 实现 向量 Clocks
- 14. [`task-2-3-4-happened-before`](track-02-identifier/task-2-3-4-happened-before/TASK.zh-CN.md) - 实现 Happened-Before Detector，包含向量 Clocks
- 15. [`task-2-3-5-vc-conflict-kv`](track-02-identifier/task-2-3-5-vc-conflict-kv/TASK.zh-CN.md) - 向量 时钟 Conflict Detection in 键值 存储

### 混合逻辑 Clocks (HLC)

- 16. [`task-2-4-1-hlc-format`](track-02-identifier/task-2-4-1-hlc-format/TASK.zh-CN.md) - Understand和实现 HLC格式
- 17. [`task-2-4-2-hlc-receive`](track-02-identifier/task-2-4-2-hlc-receive/TASK.zh-CN.md) - 实现 HLC Receive Rule
- 18. [`task-2-4-3-clock-backward`](track-02-identifier/task-2-4-3-clock-backward/TASK.zh-CN.md) - HLC Handles Backward 时钟 Gracefully
- 19. [`task-2-4-4-id-comparison`](track-02-identifier/task-2-4-4-id-comparison/TASK.zh-CN.md) - Compare HLC, UUID v4,和Snowflake IDs
- 20. [`task-2-4-5-hlc-unique-ids`](track-02-identifier/task-2-4-5-hlc-unique-ids/TASK.zh-CN.md) - HLC-Based 唯一 ID Generation用于Maelstrom

## 3. 传播者：Gossip 信息传播

本地目录：`track-03-gossiper`

### Naive 广播 (Flooding)

- 1. [`task-3-1-basic-broadcast`](track-03-gossiper/task-3-1-basic-broadcast/TASK.zh-CN.md) - 实现 基础 广播 to All Nodes
- 2. [`task-3-2-tree-topology`](track-03-gossiper/task-3-2-tree-topology/TASK.zh-CN.md) - 构建 Flat Tree Topology Gossip
- 3. [`task-3-3-random-gossip`](track-03-gossiper/task-3-3-random-gossip/TASK.zh-CN.md) - 实现 Peer-to-Peer Gossip，包含Random Neighbors
- 4. [`task-3-4-batching`](track-03-gossiper/task-3-4-batching/TASK.zh-CN.md) - 添加 消息 Batching to Reduce Network Overhead
- 5. [`task-3-5-partition-healing`](track-03-gossiper/task-3-5-partition-healing/TASK.zh-CN.md) -处理Network Partition Healing和Resynchronization

### Gossip Protocol

- 6. [`task-3-2-1-gossip-fanout`](track-03-gossiper/task-3-2-1-gossip-fanout/TASK.zh-CN.md) - 实现 Gossip Fanout，包含Random Peer Selection
- 7. [`task-3-2-2-fanout-probability`](track-03-gossiper/task-3-2-2-fanout-probability/TASK.zh-CN.md) - Calculate Minimum Fanout用于Reliable Delivery
- 8. [`task-3-2-3-gossip-timer`](track-03-gossiper/task-3-2-3-gossip-timer/TASK.zh-CN.md) - 添加 Periodic Gossip Rounds on a Timer
- 9. [`task-3-2-4-anti-entropy`](track-03-gossiper/task-3-2-4-anti-entropy/TASK.zh-CN.md) - 实现 Anti-Entropy，包含Digest Comparison
- 10. [`task-3-2-5-tuning`](track-03-gossiper/task-3-2-5-tuning/TASK.zh-CN.md) - Tune Gossip Parameters用于Maelstrom 广播

### Topology-Aware Gossip

- 11. [`task-3-3-1-tree-broadcast`](track-03-gossiper/task-3-3-1-tree-broadcast/TASK.zh-CN.md) - 实现 Tree-Based 广播 Overlay
- 12. [`task-3-3-2-tree-failure`](track-03-gossiper/task-3-3-2-tree-failure/TASK.zh-CN.md) -处理Tree节点Failure，包含Direct Fallback
- 13. [`task-3-3-3-hybrid-gossip`](track-03-gossiper/task-3-3-3-hybrid-gossip/TASK.zh-CN.md) - 实现 Hybrid Tree和Gossip 广播
- 15. [`task-3-3-5-partition-heal`](track-03-gossiper/task-3-3-5-partition-heal/TASK.zh-CN.md) - Simulate Network Partition和Healing

### Epidemic Algorithms和CRDT Gossip

- 16. [`task-3-4-1-gset`](track-03-gossiper/task-3-4-1-gset/TASK.zh-CN.md) - 实现 Grow-Only Set (G-Set)，包含Gossip
- 17. [`task-3-4-2-twopset`](track-03-gossiper/task-3-4-2-twopset/TASK.zh-CN.md) - 实现 Two-Phase Set (2P-Set)
- 18. [`task-3-4-3-lww-kv`](track-03-gossiper/task-3-4-3-lww-kv/TASK.zh-CN.md) - 实现 Last-Writer-Wins 键值 存储
- 19. [`task-3-4-4-lww-problem`](track-03-gossiper/task-3-4-4-lww-problem/TASK.zh-CN.md) - Demonstrate LWW Data Loss，包含Version Vectors
- 20. [`task-3-4-5-gossip-kv-bench`](track-03-gossiper/task-3-4-5-gossip-kv-bench/TASK.zh-CN.md) - 基准测试 Gossip KV 存储 Performance

## 4. 计数器：分布式状态与 CRDT

本地目录：`track-04-counter`

### The Lost Update Problem

- 1. [`task-4-1-lost-update`](track-04-counter/task-4-1-lost-update/TASK.zh-CN.md) - 实现 基础 计数器，包含Lost Update Problem
- 2. [`task-4-2-kv-integration`](track-04-counter/task-4-2-kv-integration/TASK.zh-CN.md) - Integrate Sequentially Consistent 键值 存储
- 3. [`task-4-3-cas-operation`](track-04-counter/task-4-3-cas-operation/TASK.zh-CN.md) - 实现 Compare-And-Swap (CAS) Operation
- 4. [`task-4-4-g-counter`](track-04-counter/task-4-4-g-counter/TASK.zh-CN.md) - 构建 Grow-Only 计数器 (G-计数器) CRDT
- 5. [`task-4-5-concurrent-increments`](track-04-counter/task-4-5-concurrent-increments/TASK.zh-CN.md) -处理Concurrent Increments Across Multiple Nodes

### G-计数器和PN-计数器

- 6. [`task-17-2-1-g-counter`](track-04-counter/task-17-2-1-g-counter/TASK.zh-CN.md) - 实现 a G-计数器 (Grow-Only CRDT)
- 7. [`task-17-2-2-g-counter-proof`](track-04-counter/task-17-2-2-g-counter-proof/TASK.zh-CN.md) - Prove G-计数器 CRDT Properties
- 8. [`task-17-2-3-pn-counter`](track-04-counter/task-17-2-3-pn-counter/TASK.zh-CN.md) - 实现 a PN-计数器用于Increment和Decrement
- 9. [`task-17-2-4-gossip-counter`](track-04-counter/task-17-2-4-gossip-counter/TASK.zh-CN.md) - Gossip PN-计数器 Across a Cluster
- 10. [`task-17-2-5-maelstrom-counter`](track-04-counter/task-17-2-5-maelstrom-counter/TASK.zh-CN.md) - Pass the Maelstrom G-计数器 Workload

### More CRDTs

- 11. [`task-17-3-1-or-set`](track-04-counter/task-17-3-1-or-set/TASK.zh-CN.md) - 实现 an OR-Set (Observed-Remove Set)
- 12. [`task-17-3-2-mv-register`](track-04-counter/task-17-3-2-mv-register/TASK.zh-CN.md) - 实现 a Multi-Value Register (MV-Register)
- 13. [`task-17-3-3-sequence-crdt`](track-04-counter/task-17-3-3-sequence-crdt/TASK.zh-CN.md) - 实现 a Sequence CRDT用于Collaborative Text Editing
- 14. [`task-17-3-4-crdt-tradeoffs`](track-04-counter/task-17-3-4-crdt-tradeoffs/TASK.zh-CN.md) - Analyze CRDT Tradeoffs vs. OCC和Locking
- 15. [`task-17-3-5-shopping-cart`](track-04-counter/task-17-3-5-shopping-cart/TASK.zh-CN.md) - 构建 a Distributed Shopping Cart，包含CRDTs

## 5. 选举器：Leader Election

本地目录：`track-05-elector`

### Raft Leader 选举

- 1. [`task-5-1-node-states`](track-05-elector/task-5-1-node-states/TASK.zh-CN.md) - 实现节点States (Leader, Follower, Candidate)
- 2. [`task-5-2-heartbeat`](track-05-elector/task-5-2-heartbeat/TASK.zh-CN.md) - 添加 Heartbeat Mechanism
- 3. [`task-5-3-election-timeout`](track-05-elector/task-5-3-election-timeout/TASK.zh-CN.md) - 实现 Randomized 选举 超时
- 4. [`task-5-4-request-vote`](track-05-elector/task-5-4-request-vote/TASK.zh-CN.md) -处理RequestVote RPC
- 5. [`task-5-5-split-vote`](track-05-elector/task-5-5-split-vote/TASK.zh-CN.md) - Prevent Split Votes Through Term Management

## 6. 共识：Raft 与日志复制

本地目录：`track-06-consensus`

### Raft 日志 复制

- 1. [`task-6-1-log-replication`](track-06-consensus/task-6-1-log-replication/TASK.zh-CN.md) - 实现 日志 复制
- 2. [`task-6-2-log-matching`](track-06-consensus/task-6-2-log-matching/TASK.zh-CN.md) - Ensure 日志 Matching Property
- 3. [`task-6-3-commitment`](track-06-consensus/task-6-3-commitment/TASK.zh-CN.md) - 实现 Entry Commitment
- 4. [`task-6-4-state-machine`](track-06-consensus/task-6-4-state-machine/TASK.zh-CN.md) - Apply Committed Entries to State Machine
- 5. [`task-6-5-safety`](track-06-consensus/task-6-5-safety/TASK.zh-CN.md) - 实现 选举 Restriction用于Safety

### Commitment和Application

- 6. [`task-7-2-1-commit-rule`](track-06-consensus/task-7-2-1-commit-rule/TASK.zh-CN.md) - 实现 the Raft Commitment Rule
- 7. [`task-7-2-2-apply-channel`](track-06-consensus/task-7-2-2-apply-channel/TASK.zh-CN.md) - 实现 the Apply Channel用于State Machine
- 8. [`task-7-2-3-noop-on-election`](track-06-consensus/task-7-2-3-noop-on-election/TASK.zh-CN.md) -处理Leader Changes，包含No-Op on 选举
- 9. [`task-7-2-4-snapshot`](track-06-consensus/task-7-2-4-snapshot/TASK.zh-CN.md) - 添加 Snapshot Support用于日志 Compaction
- 10. [`task-7-2-5-lin-kv-partition`](track-06-consensus/task-7-2-5-lin-kv-partition/TASK.zh-CN.md) - Pass Linearizable KV，包含Network Partitions

### Paxos

- 11. [`task-7-3-1-single-decree`](track-06-consensus/task-7-3-1-single-decree/TASK.zh-CN.md) - 实现 Single-Decree Paxos Phase 1 (Prepare/Promise)
- 12. [`task-7-3-2-accept-phase`](track-06-consensus/task-7-3-2-accept-phase/TASK.zh-CN.md) - 实现 Paxos Phase 2 (Accept/Accepted)
- 13. [`task-7-3-3-paxos-safety`](track-06-consensus/task-7-3-3-paxos-safety/TASK.zh-CN.md) - Prove Paxos Safety: Chosen Values Are Immutable
- 14. [`task-7-3-4-multi-paxos`](track-06-consensus/task-7-3-4-multi-paxos/TASK.zh-CN.md) - 实现 Multi-Paxos用于an Infinite 日志
- 15. [`task-7-3-5-raft-vs-paxos`](track-06-consensus/task-7-3-5-raft-vs-paxos/TASK.zh-CN.md) - Compare Raft vs Multi-Paxos

### Byzantine Fault Tolerance

- 16. [`task-7-4-1-byzantine-faults`](track-06-consensus/task-7-4-1-byzantine-faults/TASK.zh-CN.md) - Understand Byzantine Faults，包含Real-World Examples
- 17. [`task-7-4-2-pbft-impl`](track-06-consensus/task-7-4-2-pbft-impl/TASK.zh-CN.md) - 实现 Simplified PBFT，包含4 Nodes
- 18. [`task-7-4-3-equivocation-defense`](track-06-consensus/task-7-4-3-equivocation-defense/TASK.zh-CN.md) - Detect和Handle Equivocation Attacks
- 19. [`task-7-4-4-bft-threshold`](track-06-consensus/task-7-4-4-bft-threshold/TASK.zh-CN.md) - Prove the N >= 3f+1 Byzantine Fault Threshold
- 20. [`task-7-4-5-tendermint`](track-06-consensus/task-7-4-5-tendermint/TASK.zh-CN.md) - 实现 Tendermint-Style BFT Voting Rounds

## 7. 存储：线性一致 KV Store

本地目录：`track-07-store`

### Linearizable 键值 存储

- 1. [`task-7-1-kv-interface`](track-07-store/task-7-1-kv-interface/TASK.zh-CN.md) - 实现 键值 Interface
- 2. [`task-7-2-client-routing`](track-07-store/task-7-2-client-routing/TASK.zh-CN.md) -处理Client Request Routing
- 3. [`task-7-3-read-consistency`](track-07-store/task-7-3-read-consistency/TASK.zh-CN.md) - Ensure Read Consistency
- 4. [`task-7-4-client-dedup`](track-07-store/task-7-4-client-dedup/TASK.zh-CN.md) -处理Client 重试和去重
- 5. [`task-7-5-snapshots`](track-07-store/task-7-5-snapshots/TASK.zh-CN.md) - 实现 日志 Compaction，包含Snapshots

### Read Optimization

- 6. [`task-8-2-1-read-index`](track-07-store/task-8-2-1-read-index/TASK.zh-CN.md) - 实现 Read 索引用于Linearizable Reads
- 7. [`task-8-2-2-lease-reads`](track-07-store/task-8-2-2-lease-reads/TASK.zh-CN.md) - 实现 Lease-Based Reads
- 8. [`task-8-2-3-follower-reads`](track-07-store/task-8-2-3-follower-reads/TASK.zh-CN.md) - 添加 Follower Reads，包含Bounded Staleness
- 9. [`task-8-2-4-read-your-writes`](track-07-store/task-8-2-4-read-your-writes/TASK.zh-CN.md) - Guarantee Read-Your-Writes，包含Follower Reads
- 10. [`task-8-2-5-read-benchmark`](track-07-store/task-8-2-5-read-benchmark/TASK.zh-CN.md) - 基准测试 Read Strategies Under Mixed Workload

### Transactions on Raft

- 11. [`task-8-3-1-multi-key-txn`](track-07-store/task-8-3-1-multi-key-txn/TASK.zh-CN.md) - 实现 Multi-Key Transactions as Atomic 日志 Entries
- 12. [`task-8-3-2-occ`](track-07-store/task-8-3-2-occ/TASK.zh-CN.md) - 实现 Optimistic Concurrency Control
- 13. [`task-8-3-3-mvcc`](track-07-store/task-8-3-3-mvcc/TASK.zh-CN.md) - 实现 Multi-Version Concurrency Control
- 14. [`task-8-3-4-tikv-regions`](track-07-store/task-8-3-4-tikv-regions/TASK.zh-CN.md) - 构建 a Mini TiKV，包含Raft + MVCC Regions
- 15. [`task-8-3-5-contention-benchmark`](track-07-store/task-8-3-5-contention-benchmark/TASK.zh-CN.md) - 基准测试 Contended Key Under OCC vs MVCC

## 8. 分片器：水平扩展与数据迁移

本地目录：`track-08-sharder`

### Range Sharding

- 1. [`task-8-1-shard-controller`](track-08-sharder/task-8-1-shard-controller/TASK.zh-CN.md) - 实现 分片 Controller
- 2. [`task-8-2-consistent-hash`](track-08-sharder/task-8-2-consistent-hash/TASK.zh-CN.md) - 实现 Consistent Hashing用于Sharding
- 3. [`task-8-3-config-change`](track-08-sharder/task-8-3-config-change/TASK.zh-CN.md) -处理Configuration Changes
- 4. [`task-8-4-data-migration`](track-08-sharder/task-8-4-data-migration/TASK.zh-CN.md) - 实现 Data Migration
- 5. [`task-8-5-sharded-kv`](track-08-sharder/task-8-5-sharded-kv/TASK.zh-CN.md) - 构建 Complete Sharded 键值 存储

### Consistent Hashing

- 6. [`task-18-2-1-hash-ring`](track-08-sharder/task-18-2-1-hash-ring/TASK.zh-CN.md) - 实现 a Consistent Hash Ring
- 7. [`task-18-2-2-virtual-nodes`](track-08-sharder/task-18-2-2-virtual-nodes/TASK.zh-CN.md) - 添加 Virtual Nodes用于Even Distribution
- 8. [`task-18-2-3-node-join`](track-08-sharder/task-18-2-3-node-join/TASK.zh-CN.md) -处理Node Addition，包含Minimal Key Migration
- 9. [`task-18-2-4-node-removal`](track-08-sharder/task-18-2-4-node-removal/TASK.zh-CN.md) -处理Node Removal，包含Graceful和Crash Recovery
- 10. [`task-18-2-5-rendezvous-hashing`](track-08-sharder/task-18-2-5-rendezvous-hashing/TASK.zh-CN.md) - 实现 Rendezvous Hashing (Highest随机Weight)

### Cross-分片 Queries

- 11. [`task-18-3-1-scatter-gather`](track-08-sharder/task-18-3-1-scatter-gather/TASK.zh-CN.md) - 实现 Scatter-Gather Query Execution
- 12. [`task-18-3-2-aggregations`](track-08-sharder/task-18-3-2-aggregations/TASK.zh-CN.md) - 实现 Cross-分片 Aggregations
- 13. [`task-18-3-3-joins`](track-08-sharder/task-18-3-3-joins/TASK.zh-CN.md) - 实现 Cross-分片 JOINs
- 14. [`task-18-3-4-secondary-indexes`](track-08-sharder/task-18-3-4-secondary-indexes/TASK.zh-CN.md) - 实现 Secondary Indexes on Sharded Data
- 15. [`task-18-3-5-order-limit`](track-08-sharder/task-18-3-5-order-limit/TASK.zh-CN.md) - 实现 Distributed ORDER BY，包含LIMIT

## 9. 协调器：分布式事务

本地目录：`track-09-coordinator`

### Two-Phase Commit

- 1. [`task-9-1-two-phase-commit`](track-09-coordinator/task-9-1-two-phase-commit/TASK.zh-CN.md) - 实现 Two-Phase Commit
- 2. [`task-9-2-coordinator-failure`](track-09-coordinator/task-9-2-coordinator-failure/TASK.zh-CN.md) -处理Coordinator Failure
- 3. [`task-9-3-three-phase-commit`](track-09-coordinator/task-9-3-three-phase-commit/TASK.zh-CN.md) - 实现 Three-Phase Commit
- 4. [`task-9-4-sagas`](track-09-coordinator/task-9-4-sagas/TASK.zh-CN.md) - 实现 Saga Pattern
- 5. [`task-9-5-txn-kv`](track-09-coordinator/task-9-5-txn-kv/TASK.zh-CN.md) - 构建 Transactional 键值 存储

### Three-Phase Commit (3PC)

- 6. [`task-19-2-1-three-phase`](track-09-coordinator/task-19-2-1-three-phase/TASK.zh-CN.md) - 实现 Three-Phase Commit Protocol
- 7. [`task-19-2-2-unblocking`](track-09-coordinator/task-19-2-2-unblocking/TASK.zh-CN.md) - Show How 3PC Unblocks 2PC Scenarios
- 8. [`task-19-2-3-network-partition`](track-09-coordinator/task-19-2-3-network-partition/TASK.zh-CN.md) - Show 3PC Blocking Under Network Partition
- 9. [`task-19-2-4-comparison`](track-09-coordinator/task-19-2-4-comparison/TASK.zh-CN.md) - Compare 2PC vs 3PC Protocols
- 10. [`task-19-2-5-paxos-commit`](track-09-coordinator/task-19-2-5-paxos-commit/TASK.zh-CN.md) - 实现 Paxos Commit Protocol

### Saga Pattern

- 11. [`task-19-3-1-saga-fundamentals`](track-09-coordinator/task-19-3-1-saga-fundamentals/TASK.zh-CN.md) - 实现 Saga Pattern，包含Compensating Transactions
- 12. [`task-19-3-2-choreography`](track-09-coordinator/task-19-3-2-choreography/TASK.zh-CN.md) - 实现 Choreography-Based Saga
- 13. [`task-19-3-3-orchestration`](track-09-coordinator/task-19-3-3-orchestration/TASK.zh-CN.md) - 实现 Orchestration-Based Saga
- 14. [`task-19-3-4-idempotency`](track-09-coordinator/task-19-3-4-idempotency/TASK.zh-CN.md) - 实现 Idempotency in Sagas
- 15. [`task-19-3-5-shopping-cart`](track-09-coordinator/task-19-3-5-shopping-cart/TASK.zh-CN.md) - 实现 E-Commerce Checkout Saga

## 10. 高级主题

本地目录：`track-10-advanced`

### 高级 Paradigms

- 1. [`task-10-1-mapreduce`](track-10-advanced/task-10-1-mapreduce/TASK.zh-CN.md) - 实现 MapReduce
- 2. [`task-10-2-dht`](track-10-advanced/task-10-2-dht/TASK.zh-CN.md) - 构建 Distributed Hash Table (Chord)
- 3. [`task-10-3-pbft`](track-10-advanced/task-10-3-pbft/TASK.zh-CN.md) - 实现 Byzantine Fault Tolerance
- 4. [`task-10-4-streaming`](track-10-advanced/task-10-4-streaming/TASK.zh-CN.md) - 构建 Stream Processing Pipeline
- 5. [`task-10-5-crdt`](track-10-advanced/task-10-5-crdt/TASK.zh-CN.md) - 实现 CRDTs

## 11. 缓存

本地目录：`track-11-caches`

### 未分组

- 1. [`task-11-1-request-cache`](track-11-caches/task-11-1-request-cache/TASK.zh-CN.md) - 实现 Request节点缓存
- 2. [`task-11-2-global-cache`](track-11-caches/task-11-2-global-cache/TASK.zh-CN.md) - 构建 Global 缓存
- 3. [`task-11-3-distributed-cache`](track-11-caches/task-11-3-distributed-cache/TASK.zh-CN.md) - 实现 Distributed 缓存，包含Consistent Hashing
- 4. [`task-11-4-eviction`](track-11-caches/task-11-4-eviction/TASK.zh-CN.md) - 添加 Eviction Strategies (LRU, TTL)
- 5. [`task-11-5-invalidation`](track-11-caches/task-11-5-invalidation/TASK.zh-CN.md) -处理缓存 Invalidation和Consistency

## 12. 代理

本地目录：`track-12-proxies`

### Caching 代理

- 1. [`task-12-1-relay`](track-12-proxies/task-12-1-relay/TASK.zh-CN.md) - 实现 基础 Relay 代理
- 2. [`task-12-2-dedup`](track-12-proxies/task-12-2-dedup/TASK.zh-CN.md) - 添加 Request 去重
- 3. [`task-12-3-collapsed`](track-12-proxies/task-12-3-collapsed/TASK.zh-CN.md) - 实现 Collapsed Forwarding
- 4. [`task-12-4-reverse-proxy`](track-12-proxies/task-12-4-reverse-proxy/TASK.zh-CN.md) - 构建 Reverse 代理，包含Caching
- 5. [`task-12-5-health-routing`](track-12-proxies/task-12-5-health-routing/TASK.zh-CN.md) - 添加 Health-Based Routing

### API Gateway

- 6. [`task-21-2-1-api-gateway-routing`](track-12-proxies/task-21-2-1-api-gateway-routing/TASK.zh-CN.md) - 实现 API Gateway 服务 Routing
- 7. [`task-21-2-2-auth-gateway`](track-12-proxies/task-21-2-2-auth-gateway/TASK.zh-CN.md) - 实现 Authentication和Authorization at Gateway
- 8. [`task-21-2-3-transformation`](track-12-proxies/task-21-2-3-transformation/TASK.zh-CN.md) - 实现 Request/Response Transformation
- 9. [`task-21-2-4-aggregation`](track-12-proxies/task-21-2-4-aggregation/TASK.zh-CN.md) - 实现 API Composition和Aggregation
- 10. [`task-21-2-5-quota-management`](track-12-proxies/task-21-2-5-quota-management/TASK.zh-CN.md) - 实现 Rate Limiting和Quota Management

## 13. 索引

本地目录：`track-13-indexes`

### 未分组

- 1. [`task-13-1-hash-index`](track-13-indexes/task-13-1-hash-index/TASK.zh-CN.md) - 实现 Hash 索引
- 2. [`task-13-2-btree`](track-13-indexes/task-13-2-btree/TASK.zh-CN.md) - 构建 B-Tree 索引
- 3. [`task-13-3-lsm-tree`](track-13-indexes/task-13-3-lsm-tree/TASK.zh-CN.md) - 实现 LSM Tree
- 4. [`task-13-4-secondary-index`](track-13-indexes/task-13-4-secondary-index/TASK.zh-CN.md) - 添加 Secondary Indexes
- 5. [`task-13-5-distributed-index`](track-13-indexes/task-13-5-distributed-index/TASK.zh-CN.md) - Distribute 索引 Across Nodes

## 14. 负载均衡器

本地目录：`track-14-loadbalancers`

### Layer 4 Load Balancing

- 1. [`task-14-1-round-robin`](track-14-loadbalancers/task-14-1-round-robin/TASK.zh-CN.md) - 实现 Round Robin Load Balancer
- 2. [`task-14-2-least-connections`](track-14-loadbalancers/task-14-2-least-connections/TASK.zh-CN.md) - 实现 Least Connections Algorithm
- 3. [`task-14-3-health-checks`](track-14-loadbalancers/task-14-3-health-checks/TASK.zh-CN.md) - 添加 Health Checks和Failover
- 4. [`task-14-4-layer7`](track-14-loadbalancers/task-14-4-layer7/TASK.zh-CN.md) - 构建 Layer 7 Load Balancer
- 5. [`task-14-5-consistent-hashing-lb`](track-14-loadbalancers/task-14-5-consistent-hashing-lb/TASK.zh-CN.md) - 实现 Consistent Hashing用于Load Balancing

### Layer 7 Load Balancing

- 6. [`task-20-2-1-http-proxy`](track-14-loadbalancers/task-20-2-1-http-proxy/TASK.zh-CN.md) - 实现 Layer 7 HTTP 代理
- 7. [`task-20-2-2-path-routing`](track-14-loadbalancers/task-20-2-2-path-routing/TASK.zh-CN.md) - 实现 Path-Based Routing
- 8. [`task-20-2-3-sticky-sessions`](track-14-loadbalancers/task-20-2-3-sticky-sessions/TASK.zh-CN.md) - 实现 Sticky Sessions
- 9. [`task-20-2-4-circuit-breaking`](track-14-loadbalancers/task-20-2-4-circuit-breaking/TASK.zh-CN.md) - 实现 Circuit Breaking
- 10. [`task-20-2-5-rate-limiting`](track-14-loadbalancers/task-20-2-5-rate-limiting/TASK.zh-CN.md) - 实现 Rate Limiting

### 高级 Balancing Algorithms

- 11. [`task-20-3-1-least-connections`](track-14-loadbalancers/task-20-3-1-least-connections/TASK.zh-CN.md) - 实现 Least-Connections Load Balancing
- 12. [`task-20-3-2-weighted-round-robin`](track-14-loadbalancers/task-20-3-2-weighted-round-robin/TASK.zh-CN.md) - 实现 Weighted Round-Robin Load Balancing
- 13. [`task-20-3-3-power-of-two-choices`](track-14-loadbalancers/task-20-3-3-power-of-two-choices/TASK.zh-CN.md) - 实现 Power-of-Two-Choices Load Balancing
- 14. [`task-20-3-4-consistent-hashing-lb`](track-14-loadbalancers/task-20-3-4-consistent-hashing-lb/TASK.zh-CN.md) - 实现 Consistent Hashing用于Load Balancing
- 15. [`task-20-3-5-thundering-herd`](track-14-loadbalancers/task-20-3-5-thundering-herd/TASK.zh-CN.md) - Simulate Thundering Herd，包含Circuit Breaking

## 15. 队列

本地目录：`track-15-queues`

### At-Most-Once和At-Least-Once Delivery

- 1. [`task-15-1-basic-queue`](track-15-queues/task-15-1-basic-queue/TASK.zh-CN.md) - 实现 基础 消息 队列
- 2. [`task-15-2-consumer-groups`](track-15-queues/task-15-2-consumer-groups/TASK.zh-CN.md) - 添加 Consumer Groups，包含Partitions
- 3. [`task-15-3-at-least-once`](track-15-queues/task-15-3-at-least-once/TASK.zh-CN.md) - 实现 At-Least-Once Delivery
- 4. [`task-15-4-exactly-once`](track-15-queues/task-15-4-exactly-once/TASK.zh-CN.md) - 实现 Exactly-Once Semantics
- 5. [`task-15-5-dlq`](track-15-queues/task-15-5-dlq/TASK.zh-CN.md) - 添加 Dead Letter Queues

### Exactly-Once Delivery

- 6. [`task-29-2-1-exactly-once-challenges`](track-15-queues/task-29-2-1-exactly-once-challenges/TASK.zh-CN.md) - Understand Exactly-Once Delivery Challenges
- 7. [`task-29-2-2-idempotent-consumers`](track-15-queues/task-29-2-2-idempotent-consumers/TASK.zh-CN.md) - 实现 Idempotent Consumers
- 8. [`task-29-2-3-transactional-processing`](track-15-queues/task-29-2-3-transactional-processing/TASK.zh-CN.md) - 实现 Transactional 消息 Processing
- 9. [`task-29-2-4-outbox-pattern`](track-15-queues/task-29-2-4-outbox-pattern/TASK.zh-CN.md) - 实现 Outbox Pattern
- 10. [`task-29-2-5-two-phase-commit`](track-15-queues/task-29-2-5-two-phase-commit/TASK.zh-CN.md) - 实现 Two-Phase Commit用于队列和Database

## 16. 时间守卫：逻辑时钟

本地目录：`track-16-timekeeper`

### Physical Time和Its Failures

- 1. [`task-4-1-1-clock-read`](track-16-timekeeper/task-4-1-1-clock-read/TASK.zh-CN.md) - Read System 时钟和Detect Backward Jumps
- 2. [`task-4-1-2-monotonic-clock`](track-16-timekeeper/task-4-1-2-monotonic-clock/TASK.zh-CN.md) - 实现 Monotonic 时钟 Wrapper
- 3. [`task-4-1-3-split-brain-lease`](track-16-timekeeper/task-4-1-3-split-brain-lease/TASK.zh-CN.md) - Simulate Split-Brain Caused by 时钟 Drift
- 4. [`task-4-1-4-truetime-mock`](track-16-timekeeper/task-4-1-4-truetime-mock/TASK.zh-CN.md) - 实现 Mock TrueTime API
- 5. [`task-4-1-5-wait-out-uncertainty`](track-16-timekeeper/task-4-1-5-wait-out-uncertainty/TASK.zh-CN.md) - Wait-Out-Uncertainty用于External Consistency

### Lamport Clocks

- 6. [`task-4-2-1-lamport-basic`](track-16-timekeeper/task-4-2-1-lamport-basic/TASK.zh-CN.md) - 实现 a Lamport 时钟 from Scratch
- 7. [`task-4-2-2-causality-proof`](track-16-timekeeper/task-4-2-2-causality-proof/TASK.zh-CN.md) - Prove Lamport 时钟 Causality和Its Limitation
- 8. [`task-4-2-3-lamport-mutex`](track-16-timekeeper/task-4-2-3-lamport-mutex/TASK.zh-CN.md) - 实现 Distributed Mutual Exclusion，包含Lamport Clocks
- 9. [`task-4-2-4-mutex-contention`](track-16-timekeeper/task-4-2-4-mutex-contention/TASK.zh-CN.md) - Simulate并发Mutex Requests from Multiple Nodes
- 10. [`task-4-2-5-mutex-comparison`](track-16-timekeeper/task-4-2-5-mutex-comparison/TASK.zh-CN.md) - Compare Mutex Algorithms: Lamport vs Token Ring vs Centralized

### 向量 Clocks

- 11. [`task-4-3-1-vector-clock-impl`](track-16-timekeeper/task-4-3-1-vector-clock-impl/TASK.zh-CN.md) - 实现 向量 Clocks
- 12. [`task-4-3-2-happens-before`](track-16-timekeeper/task-4-3-2-happens-before/TASK.zh-CN.md) - 实现 Happens-Before和Concurrency Detection
- 13. [`task-4-3-3-causal-chat`](track-16-timekeeper/task-4-3-3-causal-chat/TASK.zh-CN.md) - 构建 a Causal-Order Chat System
- 14. [`task-4-3-4-dotted-version-vectors`](track-16-timekeeper/task-4-3-4-dotted-version-vectors/TASK.zh-CN.md) - 实现 Dotted Version Vectors
- 15. [`task-4-3-5-conflict-kv`](track-16-timekeeper/task-4-3-5-conflict-kv/TASK.zh-CN.md) - 构建 a Conflict-Detecting 键值 存储

### 混合逻辑 Clocks

- 16. [`task-4-4-1-hlc-impl`](track-16-timekeeper/task-4-4-1-hlc-impl/TASK.zh-CN.md) - 实现 混合逻辑 Clocks
- 17. [`task-4-4-2-hlc-causality-bound`](track-16-timekeeper/task-4-4-2-hlc-causality-bound/TASK.zh-CN.md) - Prove HLC Preserves Causality Within Epsilon
- 18. [`task-4-4-3-hlc-lock`](track-16-timekeeper/task-4-4-3-hlc-lock/TASK.zh-CN.md) - 实现 a Distributed Lock使用HLC时间戳
- 19. [`task-4-4-4-time-oracle`](track-16-timekeeper/task-4-4-4-time-oracle/TASK.zh-CN.md) - 构建 a Time Oracle 服务，包含Failover
- 20. [`task-4-4-5-clock-comparison-adr`](track-16-timekeeper/task-4-4-5-clock-comparison-adr/TASK.zh-CN.md) - Architecture Decision Record: Choosing a 时钟 System

## 17. 网络器：TCP 与协议基础

本地目录：`track-17-networker`

### TCP From Scratch

- 1. [`task-5-1-1-tcp-echo`](track-17-networker/task-5-1-1-tcp-echo/TASK.zh-CN.md) - 构建 a TCP 回声 Server from Raw Syscalls
- 2. [`task-5-1-2-connection-pool`](track-17-networker/task-5-1-2-connection-pool/TASK.zh-CN.md) - 添加 a Connection Pool，包含Configurable Backlog
- 3. [`task-5-1-3-graceful-shutdown`](track-17-networker/task-5-1-3-graceful-shutdown/TASK.zh-CN.md) - 实现 Graceful Shutdown，包含In-Flight Drain
- 4. [`task-5-1-4-keepalive`](track-17-networker/task-5-1-4-keepalive/TASK.zh-CN.md) - 实现 Application-Level TCP Keep-Alive
- 5. [`task-5-1-5-throughput-bench`](track-17-networker/task-5-1-5-throughput-bench/TASK.zh-CN.md) - 基准测试 Server 吞吐量和延迟

### 消息 Framing和Serialization

- 6. [`task-5-2-1-length-prefix`](track-17-networker/task-5-2-1-length-prefix/TASK.zh-CN.md) - 实现 Length-Prefixed 消息 Framing
- 7. [`task-5-2-2-line-delimited`](track-17-networker/task-5-2-2-line-delimited/TASK.zh-CN.md) - 实现 Line-Delimited Framing (Redis RESP Style)
- 8. [`task-5-2-3-binary-serialization`](track-17-networker/task-5-2-3-binary-serialization/TASK.zh-CN.md) - 实现 a Binary Serialization格式
- 9. [`task-5-2-4-compression`](track-17-networker/task-5-2-4-compression/TASK.zh-CN.md) - 添加 消息 Compression，包含CPU-Bandwidth Tradeoff Analysis
- 10. [`task-5-2-5-protocol-versioning`](track-17-networker/task-5-2-5-protocol-versioning/TASK.zh-CN.md) - 实现 Protocol Versioning，包含Backward Compatibility

### gRPC和Protocol Buffers

- 11. [`task-5-3-1-protobuf-schema`](track-17-networker/task-5-3-1-protobuf-schema/TASK.zh-CN.md) - Define和Encode Protocol Buffer Messages
- 12. [`task-5-3-2-grpc-unary`](track-17-networker/task-5-3-2-grpc-unary/TASK.zh-CN.md) - 实现 a gRPC Unary RPC 服务
- 13. [`task-5-3-3-grpc-streaming`](track-17-networker/task-5-3-3-grpc-streaming/TASK.zh-CN.md) - 实现 gRPC Server和Bidirectional Streaming
- 14. [`task-5-3-4-grpc-interceptors`](track-17-networker/task-5-3-4-grpc-interceptors/TASK.zh-CN.md) - 构建 gRPC Interceptors用于Logging, Auth,和Rate Limiting
- 15. [`task-5-3-5-grpc-vs-rest`](track-17-networker/task-5-3-5-grpc-vs-rest/TASK.zh-CN.md) - Compare gRPC vs REST: 延迟, Size,和DX

## 19. 日志器：WAL、LSM 与分布式日志

本地目录：`track-19-logger`

### The Commit 日志 (WAL)

- 1. [`task-10-1-1-wal-impl`](track-19-logger/task-10-1-1-wal-impl/TASK.zh-CN.md) - 实现 a Write-Ahead 日志
- 2. [`task-10-1-2-wal-recovery`](track-19-logger/task-10-1-2-wal-recovery/TASK.zh-CN.md) - 实现 WAL Recovery on Startup
- 3. [`task-10-1-3-segments`](track-19-logger/task-10-1-3-segments/TASK.zh-CN.md) - 添加 WAL Segment Files，包含Offset 索引
- 4. [`task-10-1-4-compaction`](track-19-logger/task-10-1-4-compaction/TASK.zh-CN.md) - 实现 WAL Compaction，包含Atomic Snapshot
- 5. [`task-10-1-5-fsync-bench`](track-19-logger/task-10-1-5-fsync-bench/TASK.zh-CN.md) - 基准测试 WAL fsync Strategies

### LSM Tree (日志-Structured Merge Tree)

- 6. [`task-10-2-1-memtable`](track-19-logger/task-10-2-1-memtable/TASK.zh-CN.md) - 实现 an In-Memory MemTable
- 7. [`task-10-2-2-sstable-flush`](track-19-logger/task-10-2-2-sstable-flush/TASK.zh-CN.md) - 实现 SSTable Flush，包含Bloom Filter
- 8. [`task-10-2-3-multi-level`](track-19-logger/task-10-2-3-multi-level/TASK.zh-CN.md) - 实现 a Multi-Level LSM Tree
- 9. [`task-10-2-4-compaction`](track-19-logger/task-10-2-4-compaction/TASK.zh-CN.md) - 实现 LSM Compaction，包含Merge Sort
- 10. [`task-10-2-5-lsm-bench`](track-19-logger/task-10-2-5-lsm-bench/TASK.zh-CN.md) - 基准测试 LSM Tree vs B-Tree Performance

### B-Tree on Disk

- 11. [`task-10-3-1-btree-node`](track-19-logger/task-10-3-1-btree-node/TASK.zh-CN.md) - 实现 a B-Tree Node和Search
- 12. [`task-10-3-2-btree-insert`](track-19-logger/task-10-3-2-btree-insert/TASK.zh-CN.md) - 实现 B-Tree Insert，包含Node Splits
- 13. [`task-10-3-3-btree-delete`](track-19-logger/task-10-3-3-btree-delete/TASK.zh-CN.md) - 实现 B-Tree Delete，包含Merge和Borrow
- 14. [`task-10-3-4-buffer-pool`](track-19-logger/task-10-3-4-buffer-pool/TASK.zh-CN.md) - 实现 a Buffer Pool，包含LRU Eviction
- 15. [`task-10-3-5-btree-vs-lsm`](track-19-logger/task-10-3-5-btree-vs-lsm/TASK.zh-CN.md) - Compare B-Tree vs LSM Tree，包含Amplification Metrics

### Distributed 日志 (Kafka Architecture)

- 16. [`task-10-4-1-partition-log`](track-19-logger/task-10-4-1-partition-log/TASK.zh-CN.md) -模式l a Kafka Partition as a Write-Ahead 日志
- 17. [`task-10-4-2-consumer-offsets`](track-19-logger/task-10-4-2-consumer-offsets/TASK.zh-CN.md) - 实现 Consumer Group Offset Tracking
- 18. [`task-10-4-3-partition-leader`](track-19-logger/task-10-4-3-partition-leader/TASK.zh-CN.md) - 实现 Partition Leader 选举 via Raft
- 19. [`task-10-4-4-isr`](track-19-logger/task-10-4-4-isr/TASK.zh-CN.md) - 实现 In-Sync Replicas (ISR) Management
- 20. [`task-10-4-5-consumer-rebalance`](track-19-logger/task-10-4-5-consumer-rebalance/TASK.zh-CN.md) - 实现 Consumer Group Rebalancing

## 20. 文件系统：分布式文件存储

本地目录：`track-20-filesystem`

### Distributed File Storage

- 1. [`task-12-1-1-architecture`](track-20-filesystem/task-12-1-1-architecture/TASK.zh-CN.md) - Design a GFS-Style Distributed File System Architecture
- 2. [`task-12-1-2-namespace`](track-20-filesystem/task-12-1-2-namespace/TASK.zh-CN.md) - 实现 the Master Namespace Tree
- 3. [`task-12-1-3-chunk-creation`](track-20-filesystem/task-12-1-3-chunk-creation/TASK.zh-CN.md) - 实现 Chunk Creation和Allocation
- 4. [`task-12-1-4-chunk-replication`](track-20-filesystem/task-12-1-4-chunk-replication/TASK.zh-CN.md) - 实现 Chunk 复制，包含Pipeline Writes
- 5. [`task-12-1-5-chunk-lease`](track-20-filesystem/task-12-1-5-chunk-lease/TASK.zh-CN.md) - 实现 Chunk Leases用于Primary Assignment

### Fault Tolerance和Rebalancing

- 6. [`task-12-2-1-heartbeats`](track-20-filesystem/task-12-2-1-heartbeats/TASK.zh-CN.md) - 实现 Chunk Server Heartbeats
- 7. [`task-12-2-2-re-replication`](track-20-filesystem/task-12-2-2-re-replication/TASK.zh-CN.md) - 实现 Automatic Re-复制
- 8. [`task-12-2-3-load-balancing`](track-20-filesystem/task-12-2-3-load-balancing/TASK.zh-CN.md) - 实现 Chunk Server Load Balancing
- 9. [`task-12-2-4-master-failover`](track-20-filesystem/task-12-2-4-master-failover/TASK.zh-CN.md) - 实现 Master Failover，包含Shadow Master
- 10. [`task-12-2-5-checksums`](track-20-filesystem/task-12-2-5-checksums/TASK.zh-CN.md) - 实现 Chunk Checksums用于Data Integrity

## 22. 观察者：ZooKeeper/etcd 模型

本地目录：`track-22-watcher`

### The ZNode Data模式l

- 1. [`task-15-1-1-znode-tree`](track-22-watcher/task-15-1-1-znode-tree/TASK.zh-CN.md) - 实现 a ZNode Tree Data模式l
- 2. [`task-15-1-2-crud`](track-22-watcher/task-15-1-2-crud/TASK.zh-CN.md) - 实现 ZNode CRUD Operations
- 3. [`task-15-1-3-versioning`](track-22-watcher/task-15-1-3-versioning/TASK.zh-CN.md) - 实现 Optimistic Concurrency，包含Version Checks
- 4. [`task-15-1-4-ephemeral`](track-22-watcher/task-15-1-4-ephemeral/TASK.zh-CN.md) - 实现 Ephemeral Nodes用于Session-Bound State
- 5. [`task-15-1-5-sequential`](track-22-watcher/task-15-1-5-sequential/TASK.zh-CN.md) - 实现 Sequential Nodes用于Ordering

### Watches和Sessions

- 6. [`task-15-2-1-watches`](track-22-watcher/task-15-2-1-watches/TASK.zh-CN.md) - 实现 One-Shot Watches用于Change Notification
- 7. [`task-15-2-2-sessions`](track-22-watcher/task-15-2-2-sessions/TASK.zh-CN.md) - 实现 Client Session Management
- 8. [`task-15-2-3-distributed-lock`](track-22-watcher/task-15-2-3-distributed-lock/TASK.zh-CN.md) - 构建 a Distributed Lock，包含ZooKeeper Primitives
- 9. [`task-15-2-4-leader-election`](track-22-watcher/task-15-2-4-leader-election/TASK.zh-CN.md) - 构建 Leader 选举，包含ZooKeeper
- 10. [`task-15-2-5-service-discovery`](track-22-watcher/task-15-2-5-service-discovery/TASK.zh-CN.md) - 构建 a 服务 Discovery System

### Consistency和the ZAB Protocol

- 11. [`task-15-3-1-zab`](track-22-watcher/task-15-3-1-zab/TASK.zh-CN.md) - 实现 ZAB Atomic 广播 Protocol
- 12. [`task-15-3-2-zab-leader-election`](track-22-watcher/task-15-3-2-zab-leader-election/TASK.zh-CN.md) - 实现 ZAB Leader 选举，包含FastLeaderElection
- 13. [`task-15-3-3-sequential-consistency`](track-22-watcher/task-15-3-3-sequential-consistency/TASK.zh-CN.md) - Prove ZAB Sequential Consistency
- 14. [`task-15-3-4-etcd-api`](track-22-watcher/task-15-3-4-etcd-api/TASK.zh-CN.md) - 实现 an etcd-Compatible API Layer
- 15. [`task-15-3-5-mvcc`](track-22-watcher/task-15-3-5-mvcc/TASK.zh-CN.md) - 实现 etcd MVCC用于Versioned 键值 存储

## 23. 搜索器：分布式搜索

本地目录：`track-23-searcher`

### Document模式l和Mapping

- 1. [`task-16-1-1-document-store`](track-23-searcher/task-16-1-1-document-store/TASK.zh-CN.md) - 实现 a JSON Document 存储
- 2. [`task-16-1-2-schema-mapping`](track-23-searcher/task-16-1-2-schema-mapping/TASK.zh-CN.md) - 实现 Schema Mapping，包含Field Types
- 3. [`task-16-1-3-text-analysis`](track-23-searcher/task-16-1-3-text-analysis/TASK.zh-CN.md) - 实现 a Text Analysis Pipeline
- 4. [`task-16-1-4-dynamic-mapping`](track-23-searcher/task-16-1-4-dynamic-mapping/TASK.zh-CN.md) - 实现 Dynamic Mapping，包含Type Auto-Detection
- 5. [`task-16-1-5-search-api`](track-23-searcher/task-16-1-5-search-api/TASK.zh-CN.md) - 实现 a Full-Text Search API

### Distributed Sharding和复制

- 6. [`task-16-2-1-shard-routing`](track-23-searcher/task-16-2-1-shard-routing/TASK.zh-CN.md) - 实现 Document Sharding，包含Hash-Based Routing
- 7. [`task-16-2-2-replica-shards`](track-23-searcher/task-16-2-2-replica-shards/TASK.zh-CN.md) - 添加 Replica Shards用于Fault Tolerance
- 8. [`task-16-2-3-scatter-gather`](track-23-searcher/task-16-2-3-scatter-gather/TASK.zh-CN.md) - 实现 Scatter-Gather Search Across Shards
- 9. [`task-16-2-4-shard-rebalance`](track-23-searcher/task-16-2-4-shard-rebalance/TASK.zh-CN.md) - 实现 分片 Rebalancing on节点Join
- 10. [`task-16-2-5-node-failure`](track-23-searcher/task-16-2-5-node-failure/TASK.zh-CN.md) -处理Node Failure，包含Replica Promotion

## 24. 调度器：任务调度

本地目录：`track-24-scheduler`

### Centralized Job Scheduling

- 1. [`task-22-1-1-centralized-scheduler`](track-24-scheduler/task-22-1-1-centralized-scheduler/TASK.zh-CN.md) - 实现 Centralized Job 调度器
- 2. [`task-22-1-2-deadlock-prevention`](track-24-scheduler/task-22-1-2-deadlock-prevention/TASK.zh-CN.md) - 实现 Deadlock Prevention in Scheduling
- 3. [`task-22-1-3-fair-scheduling`](track-24-scheduler/task-22-1-3-fair-scheduling/TASK.zh-CN.md) - 实现 Fair Job Scheduling
- 4. [`task-22-1-4-dependency-scheduling`](track-24-scheduler/task-22-1-4-dependency-scheduling/TASK.zh-CN.md) - 实现 Dependency-Aware Job Scheduling
- 5. [`task-22-1-5-resource-estimation`](track-24-scheduler/task-22-1-5-resource-estimation/TASK.zh-CN.md) - 实现 Resource Estimation和Provisioning

### Distributed Work Allocation

- 6. [`task-22-2-1-work-stealing`](track-24-scheduler/task-22-2-1-work-stealing/TASK.zh-CN.md) - 实现 Work Stealing 调度器
- 7. [`task-22-2-2-work-partitioning`](track-24-scheduler/task-22-2-2-work-partitioning/TASK.zh-CN.md) - 实现 MapReduce-Style Work Partitioning
- 8. [`task-22-2-3-scheduler-fault-tolerance`](track-24-scheduler/task-22-2-3-scheduler-fault-tolerance/TASK.zh-CN.md) - 实现 Fault-Tolerant 调度器
- 9. [`task-22-2-4-distributed-queue`](track-24-scheduler/task-22-2-4-distributed-queue/TASK.zh-CN.md) - 实现 Distributed Job 队列
- 10. [`task-22-2-5-dynamic-scheduling`](track-24-scheduler/task-22-2-5-dynamic-scheduling/TASK.zh-CN.md) - 实现 Dynamic Scheduling，包含Locality Awareness

## 25. 追踪器：可观测性

本地目录：`track-25-tracer`

### Distributed Tracing

- 1. [`task-23-1-1-trace-context-propagation`](track-25-tracer/task-23-1-1-trace-context-propagation/TASK.zh-CN.md) - 实现 Distributed Trace Context Propagation
- 2. [`task-23-1-2-span-lifecycle`](track-25-tracer/task-23-1-2-span-lifecycle/TASK.zh-CN.md) - 实现 Span Lifecycle Management
- 3. [`task-23-1-3-trace-collector`](track-25-tracer/task-23-1-3-trace-collector/TASK.zh-CN.md) - 实现 Distributed Trace Collector
- 4. [`task-23-1-4-trace-analysis`](track-25-tracer/task-23-1-4-trace-analysis/TASK.zh-CN.md) - 实现 Trace Analysis和Insights
- 5. [`task-23-1-5-distributed-tracing`](track-25-tracer/task-23-1-5-distributed-tracing/TASK.zh-CN.md) - 实现 End-to-End Distributed Tracing System

### Metrics和Alerting

- 6. [`task-23-2-1-metrics-collection`](track-25-tracer/task-23-2-1-metrics-collection/TASK.zh-CN.md) - 实现 Metrics Collection
- 7. [`task-23-2-2-alerting-rules`](track-25-tracer/task-23-2-2-alerting-rules/TASK.zh-CN.md) - 实现 Alerting Rules Engine
- 8. [`task-23-2-3-metrics-aggregation`](track-25-tracer/task-23-2-3-metrics-aggregation/TASK.zh-CN.md) - 实现 Metrics Aggregation和Rollups
- 9. [`task-23-2-4-dashboards-visualization`](track-25-tracer/task-23-2-4-dashboards-visualization/TASK.zh-CN.md) - 实现 Monitoring Dashboards和Visualization
- 10. [`task-23-2-5-alert-integrations`](track-25-tracer/task-23-2-5-alert-integrations/TASK.zh-CN.md) - 实现 Alert Integrations和On-Call Management

## 26. 安全器：认证、授权与加密

本地目录：`track-26-securitor`

### Authentication和Authorization

- 1. [`task-24-1-1-jwt-authentication`](track-26-securitor/task-24-1-1-jwt-authentication/TASK.zh-CN.md) - 实现 JWT Authentication System
- 2. [`task-24-1-2-oauth-authorization`](track-26-securitor/task-24-1-2-oauth-authorization/TASK.zh-CN.md) - 实现 OAuth 2.0 Authorization Flow
- 3. [`task-24-1-3-session-management`](track-26-securitor/task-24-1-3-session-management/TASK.zh-CN.md) - 实现 Secure Session Management
- 4. [`task-24-1-4-role-based-access-control`](track-26-securitor/task-24-1-4-role-based-access-control/TASK.zh-CN.md) - 实现 Role-Based Access Control (RBAC)
- 5. [`task-24-1-5-api-security`](track-26-securitor/task-24-1-5-api-security/TASK.zh-CN.md) - 实现 API 安全 Best Practices

### Encryption at Rest和in Transit

- 6. [`task-24-2-1-symmetric-encryption`](track-26-securitor/task-24-2-1-symmetric-encryption/TASK.zh-CN.md) - 实现 Symmetric Encryption
- 7. [`task-24-2-2-asymmetric-encryption`](track-26-securitor/task-24-2-2-asymmetric-encryption/TASK.zh-CN.md) - 实现 Asymmetric Encryption (RSA)
- 8. [`task-24-2-3-hash-functions`](track-26-securitor/task-24-2-3-hash-functions/TASK.zh-CN.md) - 实现 Cryptographic Hash Functions
- 9. [`task-24-2-4-key-management`](track-26-securitor/task-24-2-4-key-management/TASK.zh-CN.md) - 实现 Secure Key Management
- 10. [`task-24-2-5-end-to-end-encryption`](track-26-securitor/task-24-2-5-end-to-end-encryption/TASK.zh-CN.md) - 实现 End-to-End Encryption (E2EE)

## 27. 迁移器：数据与协议演进

本地目录：`track-27-migrator`

### Schema Migrations

- 1. [`task-25-1-1-database-migrations`](track-27-migrator/task-25-1-1-database-migrations/TASK.zh-CN.md) - 实现 Database Schema Migrations
- 2. [`task-25-1-2-backward-compatible-migrations`](track-27-migrator/task-25-1-2-backward-compatible-migrations/TASK.zh-CN.md) - 实现 Backward-Compatible Schema Migrations
- 3. [`task-25-1-3-zero-downtime-migrations`](track-27-migrator/task-25-1-3-zero-downtime-migrations/TASK.zh-CN.md) - 实现 Zero-Downtime Database Migrations
- 4. [`task-25-1-4-data-migrations`](track-27-migrator/task-25-1-4-data-migrations/TASK.zh-CN.md) - 实现 Data Migrations
- 5. [`task-25-1-5-rollback-strategies`](track-27-migrator/task-25-1-5-rollback-strategies/TASK.zh-CN.md) - 实现 Migration Rollback Strategies

### Protocol和API Evolution

- 6. [`task-25-2-1-api-versioning`](track-27-migrator/task-25-2-1-api-versioning/TASK.zh-CN.md) - 实现 API Versioning
- 7. [`task-25-2-2-backward-compatibility`](track-27-migrator/task-25-2-2-backward-compatibility/TASK.zh-CN.md) - 实现 Backward-Compatible API Changes
- 8. [`task-25-2-3-graceful-degradation`](track-27-migrator/task-25-2-3-graceful-degradation/TASK.zh-CN.md) - 实现 Graceful API Degradation
- 9. [`task-25-2-4-protocol-evolution`](track-27-migrator/task-25-2-4-protocol-evolution/TASK.zh-CN.md) - 实现 Protocol Evolution
- 10. [`task-25-2-5-client-migration`](track-27-migrator/task-25-2-5-client-migration/TASK.zh-CN.md) - 实现 Client Migration Strategy

## 28. 编排器：容器调度与服务网格

本地目录：`track-28-orchestrator`

### Scheduling

- 1. [`task-26-1-1-job-scheduling`](track-28-orchestrator/task-26-1-1-job-scheduling/TASK.zh-CN.md) - 实现 Job Scheduling System
- 2. [`task-26-1-2-dag-scheduling`](track-28-orchestrator/task-26-1-2-dag-scheduling/TASK.zh-CN.md) - 实现 DAG-Based Task Scheduling
- 3. [`task-26-1-3-resource-management`](track-28-orchestrator/task-26-1-3-resource-management/TASK.zh-CN.md) - 实现 Resource Management用于Jobs
- 4. [`task-26-1-4-job-monitoring`](track-28-orchestrator/task-26-1-4-job-monitoring/TASK.zh-CN.md) - 实现 Job Monitoring和Observability
- 5. [`task-26-1-5-job-deadlines`](track-28-orchestrator/task-26-1-5-job-deadlines/TASK.zh-CN.md) - 实现 Job Deadlines和Timeouts

### 服务 Mesh

- 6. [`task-26-2-1-service-mesh`](track-28-orchestrator/task-26-2-1-service-mesh/TASK.zh-CN.md) - 实现 服务 Mesh Architecture
- 7. [`task-26-2-2-mtls`](track-28-orchestrator/task-26-2-2-mtls/TASK.zh-CN.md) - 实现 mTLS Authentication in 服务 Mesh
- 8. [`task-26-2-3-traffic-splitting`](track-28-orchestrator/task-26-2-3-traffic-splitting/TASK.zh-CN.md) - 实现 Traffic Splitting in 服务 Mesh
- 9. [`task-26-2-4-circuit-breaking`](track-28-orchestrator/task-26-2-4-circuit-breaking/TASK.zh-CN.md) - 实现 Circuit Breaking in 服务 Mesh
- 10. [`task-26-2-5-observability`](track-28-orchestrator/task-26-2-5-observability/TASK.zh-CN.md) - 实现 服务 Mesh Observability

## 29. 反应器：事件溯源与 CQRS

本地目录：`track-29-reactor`

### Event Sourcing

- 1. [`task-27-1-1-event-store`](track-29-reactor/task-27-1-1-event-store/TASK.zh-CN.md) - 实现 Event 存储
- 2. [`task-27-1-2-event-replay`](track-29-reactor/task-27-1-2-event-replay/TASK.zh-CN.md) - 实现 Event Replay
- 3. [`task-27-1-3-event-versioning`](track-29-reactor/task-27-1-3-event-versioning/TASK.zh-CN.md) - 实现 Event Versioning和Migration
- 4. [`task-27-1-4-event-projections`](track-29-reactor/task-27-1-4-event-projections/TASK.zh-CN.md) - 实现 Event Projections
- 5. [`task-27-1-5-event-compensation`](track-29-reactor/task-27-1-5-event-compensation/TASK.zh-CN.md) - 实现 Event Compensation和Sagas

### CQRS (Command Query Responsibility Segregation)

- 6. [`task-27-2-1-cqrs-fundamentals`](track-29-reactor/task-27-2-1-cqrs-fundamentals/TASK.zh-CN.md) - 实现 CQRS Fundamentals
- 7. [`task-27-2-2-command-side`](track-29-reactor/task-27-2-2-command-side/TASK.zh-CN.md) - 实现 Command Side 校验和Execution
- 8. [`task-27-2-3-query-side`](track-29-reactor/task-27-2-3-query-side/TASK.zh-CN.md) - 实现 Query Side Optimization
- 9. [`task-27-2-4-event-driven-updates`](track-29-reactor/task-27-2-4-event-driven-updates/TASK.zh-CN.md) - 实现 Event-Driven Read模式l Updates
- 10. [`task-27-2-5-cqrs-event-sourcing`](track-29-reactor/task-27-2-5-cqrs-event-sourcing/TASK.zh-CN.md) - 实现 CQRS，包含Event Sourcing

## 30. MapReducer：批处理与流处理

本地目录：`track-30-mapreducer`

### MapReduce Fundamentals

- 1. [`task-28-1-1-mapreduce-basics`](track-30-mapreducer/task-28-1-1-mapreduce-basics/TASK.zh-CN.md) - 实现 Single-Machine MapReduce
- 2. [`task-28-1-2-distributed-mapreduce`](track-30-mapreducer/task-28-1-2-distributed-mapreduce/TASK.zh-CN.md) - 实现 Distributed MapReduce
- 3. [`task-28-1-3-shuffle-phase`](track-30-mapreducer/task-28-1-3-shuffle-phase/TASK.zh-CN.md) - 实现 Shuffle Phase，包含Hash Partitioning
- 4. [`task-28-1-4-fault-tolerance`](track-30-mapreducer/task-28-1-4-fault-tolerance/TASK.zh-CN.md) - 实现 Fault Tolerance in MapReduce
- 5. [`task-28-1-5-chained-mapreduce`](track-30-mapreducer/task-28-1-5-chained-mapreduce/TASK.zh-CN.md) - 实现 Chained MapReduce Pipeline

### Stream Processing

- 6. [`task-28-2-1-streaming-wordcount`](track-30-mapreducer/task-28-2-1-streaming-wordcount/TASK.zh-CN.md) - 实现 Streaming Word Count
- 7. [`task-28-2-2-tumbling-windows`](track-30-mapreducer/task-28-2-2-tumbling-windows/TASK.zh-CN.md) - 实现 Tumbling Windows
- 8. [`task-28-2-3-sliding-windows`](track-30-mapreducer/task-28-2-3-sliding-windows/TASK.zh-CN.md) - 实现 Sliding Windows
- 9. [`task-28-2-4-watermarks`](track-30-mapreducer/task-28-2-4-watermarks/TASK.zh-CN.md) -处理Out-of-Order Events，包含Watermarks
- 10. [`task-28-2-5-exactly-once`](track-30-mapreducer/task-28-2-5-exactly-once/TASK.zh-CN.md) - 实现 Exactly-Once Processing
