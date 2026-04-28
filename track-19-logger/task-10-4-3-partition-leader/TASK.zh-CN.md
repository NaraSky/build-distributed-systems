# 实现 Partition Leader 选举 via Raft

英文标题：Implement Partition Leader Election via Raft
网页：<https://builddistributedsystem.com/tracks/logger/tasks/task-10-4-3-partition-leader>

课程：19. 日志器：WAL、LSM 与分布式日志
任务序号：18
短标题：Partition Leader
难度：advanced
子主题：Distributed 日志 (Kafka Architecture)

## 中文导读

本题要求你完成 `实现 Partition Leader 选举 via Raft`。

重点关注：`partition leader`、`Raft per partition`、`leader broker`、`follower replication`、`metadata`。

建议先按提示逐步实现：Each Kafka partition has a Leader broker that handles all reads和writes。

协议字段、消息类型、输入输出格式请以本文件中的代码块和测试用例为准。

## 题目说明

In a distributed 日志 like Kafka, each partition must have exactly one Leader broker that handles all reads和writes. Followers replicate data from the Leader用于故障 tolerance.

Architecture:
- **Leader**: the broker responsible用于a partition. All producers和consumers interact，包含the Leader.
- **Followers**: replicate the partition 日志 from the Leader. They do not serve reads (in standard Kafka).
- **Leader election**: when the Leader crashes, one of the in-sync followers is elected as the new Leader.

The 元数据 flow:
1. Producer calls `metadata_request` to discover which broker is the Leader用于a partition
2. Producer sends `ProduceRequest` directly to the Leader broker
3. Leader writes the 消息 to its local 日志
4. Leader replicates to followers
5. After 复制, Leader acknowledges the producer

This ensures total order within a partition — all 消息 pass through a single Leader.

```JSON
请求:  {"type": "partition_leader", "msg_id": 1, "topic": "orders", "partition": 0}
响应: {"type": "partition_leader_ok", "in_reply_to": 1, "Leader": "broker-1", "followers": ["broker-2", "broker-3"], "term": 3}

请求:  {"type": "partition_failover", "msg_id": 2, "topic": "orders", "partition": 0, "failed_leader": "broker-1"}
响应: {"type": "partition_failover_ok", "in_reply_to": 2, "new_leader": "broker-2", "new_term": 4, "failover_ms": 250}
```

## 涉及概念

- `partition leader`
- `Raft per partition`
- `leader broker`
- `follower replication`
- `metadata`

## 实现提示

- Each Kafka partition has a Leader broker that handles all reads和writes
- N-1 Follower brokers replicate from the Leader用于故障 tolerance
- Use Raft用于Leader election within each partition group
- Producers discover the Leader via a 元数据 请求和send writes directly to it
- On Leader 故障, Raft automatically elects a new Leader from the followers

## 测试用例

### 1. Query partition Leader

partition_leader_ok should include Leader 节点, followers list,和Raft term.

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1","n2","n3"]}}
{"src":"c1","dest":"n1","body":{"type":"partition_leader","msg_id":2,"topic":"orders","partition":0}}
```

期望输出：

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

### 2. Leader failover elects new Leader

partition_failover_ok should show a new_leader different from failed_leader,和new_term > previous term.

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1","n2","n3"]}}
{"src":"c1","dest":"n1","body":{"type":"partition_failover","msg_id":2,"topic":"orders","partition":0,"failed_leader":"n1"}}
```

期望输出：

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

## 参考资料

- [Kafka Replication Design](https://kafka.apache.org/documentation/#replication)：Kafka documentation on partition 复制, Leader election,和failover

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
