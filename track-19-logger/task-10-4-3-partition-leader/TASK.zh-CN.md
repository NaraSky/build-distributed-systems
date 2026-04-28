# 实现基于 Raft 的分区领导者选举

英文标题：Implement Partition Leader Election via Raft
网页：<https://builddistributedsystem.com/tracks/logger/tasks/task-10-4-3-partition-leader>

课程：19. 日志器：WAL、LSM 与分布式日志
任务序号：18
短标题：Partition Leader
难度：高级
子主题：Distributed Log (Kafka Architecture)

## 中文导读

本题要求你实现 Kafka 风格的分区领导者选举机制。在分布式日志系统中，每个分区必须有且仅有一个领导者（Leader）来处理所有的读写请求，其余的跟随者（Follower）负责复制数据以实现容错。当领导者宕机时，需要从跟随者中选出新的领导者，这是保证系统高可用的关键。

## 题目说明

在 Kafka 这样的分布式日志系统中，每个分区必须有且仅有一个领导者代理（Leader Broker）来处理所有的读写请求。跟随者（Follower）从领导者复制数据以实现容错。

架构如下：
- **领导者**：负责某个分区的代理节点。所有的生产者和消费者都与领导者交互。
- **跟随者**：从领导者复制分区日志。在标准 Kafka 中，跟随者不对外提供读服务。
- **领导者选举**：当领导者宕机时，从同步副本中选举一个跟随者成为新的领导者。

元数据的交互流程：
1. 生产者调用 `metadata_request` 查询哪个代理是某个分区的领导者
2. 生产者将写入请求直接发送给领导者代理
3. 领导者将消息写入自己的本地日志
4. 领导者将消息复制给跟随者
5. 复制完成后，领导者向生产者确认写入成功

这确保了分区内的全序性——所有消息都经过同一个领导者处理。

```json
Request:  {"type": "partition_leader", "msg_id": 1, "topic": "orders", "partition": 0}
Response: {"type": "partition_leader_ok", "in_reply_to": 1, "leader": "broker-1", "followers": ["broker-2", "broker-3"], "term": 3}

Request:  {"type": "partition_failover", "msg_id": 2, "topic": "orders", "partition": 0, "failed_leader": "broker-1"}
Response: {"type": "partition_failover_ok", "in_reply_to": 2, "new_leader": "broker-2", "new_term": 4, "failover_ms": 250}
```

## 涉及概念

- `partition leader`
- `Raft per partition`
- `leader broker`
- `follower replication`
- `metadata`

## 实现提示

- 每个 Kafka 分区都有一个领导者代理，负责处理所有的读写请求
- 其余 N-1 个跟随者代理从领导者复制数据以实现容错
- 使用 Raft 算法在每个分区组内进行领导者选举
- 生产者通过元数据请求发现领导者，然后直接向领导者发送写入请求
- 当领导者故障时，Raft 自动从跟随者中选举出新的领导者

## 测试用例

### 1. 查询分区领导者

返回的 partition_leader_ok 应包含领导者节点、跟随者列表和 Raft 任期号。

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1","n2","n3"]}}
{"src":"c1","dest":"n1","body":{"type":"partition_leader","msg_id":2,"topic":"orders","partition":0}}
```

期望输出：

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

### 2. 领导者故障转移后选举新领导者

返回的 partition_failover_ok 中 new_leader 应不同于 failed_leader，且 new_term 应大于之前的任期号。

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

- [Kafka Replication Design](https://kafka.apache.org/documentation/#replication)：Kafka 官方文档，讲解分区复制、领导者选举和故障转移

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
