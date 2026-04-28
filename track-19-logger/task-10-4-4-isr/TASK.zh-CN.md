# 实现 In-Sync Replicas (ISR) Management

英文标题：Implement In-Sync Replicas (ISR) Management
网页：<https://builddistributedsystem.com/tracks/logger/tasks/task-10-4-4-isr>

课程：19. 日志器：WAL、LSM 与分布式日志
任务序号：19
短标题：ISR Management
难度：advanced
子主题：Distributed 日志 (Kafka Architecture)

## 中文导读

本题要求你完成 `实现 In-Sync Replicas (ISR) Management`。

重点关注：`ISR`、`in-sync replicas`、`replication lag`、`acks=all`、`durability guarantee`。

建议先按提示逐步实现：The ISR is the set of replicas that are "caught up"，包含the Leader (within a lag threshold)。

协议字段、消息类型、输入输出格式请以本文件中的代码块和测试用例为准。

## 题目说明

The In-Sync Replica (ISR) set is Kafka's mechanism用于balancing durability和availability. It tracks which replicas are "caught up"，包含the Leader和determines the durability guarantee用于writes.

ISR behavior:
1. **Write，包含acks=all**: Leader replicates the 消息 to ALL ISR members, then acknowledges the producer. This guarantees the 消息 survives any single broker 故障.
2. **Follower falls behind**: if a Follower's 复制 lag exceeds `replica.lag.time.max.ms` (default 10s), the Leader removes it from the ISR.
3. **ISR shrinks**:，包含fewer ISR members, writes are acknowledged，包含fewer replicas. Durability is reduced but availability is maintained.
4. **Follower catches up**: when the slow Follower catches up to the Leader's 日志 end offset, it is added back to the ISR.
5. **Min ISR**: `min.insync.replicas` (e.g. 2) prevents writes when ISR drops below a threshold, trading availability用于durability.

```JSON
请求:  {"type": "isr_status", "msg_id": 1, "topic": "orders", "partition": 0}
响应: {"type": "isr_status_ok", "in_reply_to": 1, "Leader": "n1", "isr": ["n1", "n2", "n3"], "out_of_sync": []}

请求:  {"type": "isr_simulate_lag", "msg_id": 2, "节点": "n3", "lag_seconds": 15}
响应: {"type": "isr_simulate_lag_ok", "in_reply_to": 2, "removed_from_isr": true, "new_isr": ["n1", "n2"], "reason": "lag_15s_exceeds_threshold_10s"}

请求:  {"type": "isr_recover", "msg_id": 3, "节点": "n3"}
响应: {"type": "isr_recover_ok", "in_reply_to": 3, "added_to_isr": true, "new_isr": ["n1", "n2", "n3"]}
```

## 涉及概念

- `ISR`
- `in-sync replicas`
- `replication lag`
- `acks=all`
- `durability guarantee`

## 实现提示

- The ISR is the set of replicas that are "caught up"，包含the Leader (within a lag threshold)
- With acks=all, the Leader only acknowledges a write after ALL ISR members have replicated it
- Remove a Follower from ISR if it falls more than 10 seconds behind (replica.lag.time.max.ms)
- When a slow Follower catches up, add it back to the ISR
- acks=all means "all ISR members", NOT "all replicas" — shrinking ISR reduces the durability guarantee

## 测试用例

### 1. All replicas initially in sync

isr_status_ok should show all 节点 in ISR，包含empty out_of_sync list.

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1","n2","n3"]}}
{"src":"c1","dest":"n1","body":{"type":"isr_status","msg_id":2,"topic":"orders","partition":0}}
```

期望输出：

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

### 2. Lagging node removed from ISR

isr_simulate_lag_ok should show removed_from_isr: true because 15s > 10s threshold.

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1","n2","n3"]}}
{"src":"c1","dest":"n1","body":{"type":"isr_simulate_lag","msg_id":2,"node":"n3","lag_seconds":15}}
```

期望输出：

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

## 参考资料

- [Kafka ISR和Replication](https://kafka.apache.org/documentation/#design_replicatedlog)：Kafka documentation on in-sync replicas, 复制 lag,和durability guarantees

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
