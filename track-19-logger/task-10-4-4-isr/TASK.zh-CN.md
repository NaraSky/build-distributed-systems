# 实现同步副本集管理

英文标题：Implement In-Sync Replicas (ISR) Management
网页：<https://builddistributedsystem.com/tracks/logger/tasks/task-10-4-4-isr>

课程：19. 日志器：WAL、LSM 与分布式日志
任务序号：19
短标题：ISR Management
难度：高级
子主题：Distributed Log (Kafka Architecture)

## 中文导读

本题要求你实现 Kafka 的同步副本集（ISR）管理机制。同步副本集记录了哪些副本与领导者保持同步，它是 Kafka 在持久性和可用性之间取得平衡的核心手段。理解同步副本集的工作原理，对掌握分布式系统中"数据不丢"和"服务不停"之间的权衡至关重要。

## 题目说明

同步副本集（In-Sync Replica，简称 ISR）是 Kafka 用来平衡持久性（Durability）和可用性（Availability）的机制。它追踪哪些副本与领导者"保持同步"，并据此决定写入操作的持久性保证级别。

同步副本集的行为如下：
1. **acks=all 模式写入**：领导者将消息复制到所有 ISR 成员后，才向生产者确认。这保证了即使任意单个代理故障，消息也不会丢失。
2. **跟随者掉队**：如果某个跟随者的复制延迟超过 `replica.lag.time.max.ms`（默认 10 秒），领导者会将它从 ISR 中移除。
3. **ISR 收缩**：ISR 成员减少后，写入操作只需要更少的副本确认。持久性降低了，但可用性得以维持。
4. **跟随者追赶上来**：当掉队的跟随者追上领导者的日志末尾偏移量后，它会被重新加入 ISR。
5. **最小 ISR 数量**：`min.insync.replicas`（例如设为 2）可以阻止当 ISR 成员数量低于阈值时的写入操作，用可用性换取持久性。

```json
Request:  {"type": "isr_status", "msg_id": 1, "topic": "orders", "partition": 0}
Response: {"type": "isr_status_ok", "in_reply_to": 1, "leader": "n1", "isr": ["n1", "n2", "n3"], "out_of_sync": []}

Request:  {"type": "isr_simulate_lag", "msg_id": 2, "node": "n3", "lag_seconds": 15}
Response: {"type": "isr_simulate_lag_ok", "in_reply_to": 2, "removed_from_isr": true, "new_isr": ["n1", "n2"], "reason": "lag_15s_exceeds_threshold_10s"}

Request:  {"type": "isr_recover", "msg_id": 3, "node": "n3"}
Response: {"type": "isr_recover_ok", "in_reply_to": 3, "added_to_isr": true, "new_isr": ["n1", "n2", "n3"]}
```

## 涉及概念

- `ISR`
- `in-sync replicas`
- `replication lag`
- `acks=all`
- `durability guarantee`

## 实现提示

- 同步副本集是指那些与领导者"保持同步"（延迟在阈值范围内）的副本集合
- 在 acks=all 模式下，领导者只有在所有 ISR 成员都完成复制后才确认写入
- 如果某个跟随者的延迟超过 10 秒（replica.lag.time.max.ms），就将它从 ISR 中移除
- 当掉队的跟随者追赶上来后，将它重新加入 ISR
- acks=all 的含义是"所有 ISR 成员"，而不是"所有副本"——ISR 收缩会降低持久性保证

## 测试用例

### 1. 所有副本初始时均同步

返回的 isr_status_ok 应显示所有节点都在 ISR 中，out_of_sync 列表为空。

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1","n2","n3"]}}
{"src":"c1","dest":"n1","body":{"type":"isr_status","msg_id":2,"topic":"orders","partition":0}}
```

期望输出：

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

### 2. 延迟过高的节点被移出 ISR

返回的 isr_simulate_lag_ok 应显示 removed_from_isr: true，因为 15 秒超过了 10 秒的阈值。

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

- [Kafka ISR and Replication](https://kafka.apache.org/documentation/#design_replicatedlog)：Kafka 官方文档，讲解同步副本集、复制延迟和持久性保证

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
