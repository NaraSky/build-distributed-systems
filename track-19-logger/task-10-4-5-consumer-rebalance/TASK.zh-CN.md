# 实现消费者组的重平衡

英文标题：Implement Consumer Group Rebalancing
网页：<https://builddistributedsystem.com/tracks/logger/tasks/task-10-4-5-consumer-rebalance>

课程：19. 日志器：WAL、LSM 与分布式日志
任务序号：20
短标题：Consumer Rebalance
难度：高级
子主题：Distributed Log (Kafka Architecture)

## 中文导读

本题要求你实现消费者组的重平衡（Rebalance）机制。当消费者组的成员发生变化（有消费者加入、离开或宕机）时，需要将分区重新均匀分配给各个消费者。这是 Kafka 实现弹性伸缩和容错消费的核心协议，理解它有助于排查生产环境中的消费延迟抖动问题。

## 题目说明

消费者组重平衡（Consumer Group Rebalancing）确保分区在消费者之间均匀分配。当组的成员发生变化（有消费者加入、离开或因心跳超时被移除）时，需要重新分配所有分区。

重平衡协议的流程：
1. **触发**：有消费者加入、离开或被移除（心跳超时）
2. **暂停**：组内所有消费者停止读取消息（消费暂停）
3. **选举组长**：组协调者（一个代理节点）选出一个消费者作为组长
4. **分配**：组长运行分配策略，将分区分配给各个消费者
5. **恢复**：所有消费者收到新的分配方案后恢复消费

**范围分配策略（Range Assignment Strategy）**（最简单的策略）：
- 将分区编号和消费者编号分别排序
- 将分区按连续的范围分配
- 例如：6 个分区、3 个消费者 -> c1: [0,1]、c2: [2,3]、c3: [4,5]
- 不能整除时：7 个分区、3 个消费者 -> c1: [0,1,2]、c2: [3,4]、c3: [5,6]

```json
Request:  {"type": "consumer_rebalance", "msg_id": 1, "group": "analytics", "consumers": ["c1", "c2", "c3"], "partitions": [0, 1, 2, 3, 4, 5], "strategy": "range"}
Response: {"type": "consumer_rebalance_ok", "in_reply_to": 1, "assignments": {"c1": [0, 1], "c2": [2, 3], "c3": [4, 5]}}

Request:  {"type": "consumer_rebalance", "msg_id": 2, "group": "analytics", "consumers": ["c1", "c2"], "partitions": [0, 1, 2, 3, 4, 5], "strategy": "range"}
Response: {"type": "consumer_rebalance_ok", "in_reply_to": 2, "assignments": {"c1": [0, 1, 2], "c2": [3, 4, 5]}}
```

## 涉及概念

- `consumer group`
- `rebalancing`
- `partition assignment`
- `range strategy`
- `group coordinator`

## 实现提示

- 当消费者加入或离开组时，需要重新计算所有分区的分配方案
- 范围分配策略：对消费者和分区分别排序，将分区按连续的范围分配给各消费者
- 重平衡期间，组内所有消费者会短暂暂停消费（全局暂停）
- 组协调者（一个代理节点）负责管理重平衡协议
- 不能整除的情况：如果 6 个分区分给 4 个消费者，部分消费者分到 2 个，部分分到 1 个

## 测试用例

### 1. 均匀分配：6 个分区、3 个消费者

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"consumer_rebalance","msg_id":2,"group":"g1","consumers":["c1","c2","c3"],"partitions":[0,1,2,3,4,5],"strategy":"range"}}
```

期望输出：

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
{"src": "n1", "dest": "c1", "body": {"type": "consumer_rebalance_ok", "in_reply_to": 2, "assignments": {"c1": [0, 1], "c2": [2, 3], "c3": [4, 5]}, "msg_id": 1}}
```

### 2. 消费者离开后重新分配：6 个分区、2 个消费者

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"consumer_rebalance","msg_id":2,"group":"g1","consumers":["c1","c2"],"partitions":[0,1,2,3,4,5],"strategy":"range"}}
```

期望输出：

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
{"src": "n1", "dest": "c1", "body": {"type": "consumer_rebalance_ok", "in_reply_to": 2, "assignments": {"c1": [0, 1, 2], "c2": [3, 4, 5]}, "msg_id": 1}}
```

## 参考资料

- [Kafka Consumer Group Protocol](https://kafka.apache.org/documentation/#impl_consumerrebalance)：Kafka 官方文档，讲解消费者组重平衡协议和分区分配策略

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
