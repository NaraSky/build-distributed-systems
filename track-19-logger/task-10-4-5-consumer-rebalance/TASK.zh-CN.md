# 实现 Consumer Group Rebalancing

英文标题：Implement Consumer Group Rebalancing
网页：<https://builddistributedsystem.com/tracks/logger/tasks/task-10-4-5-consumer-rebalance>

课程：19. 日志器：WAL、LSM 与分布式日志
任务序号：20
短标题：Consumer Rebalance
难度：advanced
子主题：Distributed 日志 (Kafka Architecture)

## 中文导读

本题要求你完成 `实现 Consumer Group Rebalancing`。

重点关注：`consumer group`、`rebalancing`、`partition assignment`、`range strategy`、`group coordinator`。

建议先按提示逐步实现：When a consumer joins or leaves a group, all partition assignments must be recalculated。

协议字段、消息类型、输入输出格式请以本文件中的代码块和测试用例为准。

## 题目说明

Consumer group rebalancing ensures that partitions are evenly distributed among consumers. When the group membership changes (a consumer joins, leaves, or crashes), the partitions must be reassigned.

The rebalancing protocol:
1. **Trigger**: a consumer joins the group, leaves the group, or is removed (心跳 超时)
2. **Stop**: all consumers in the group stop reading (consumption is paused)
3. **Elect Leader**: the group coordinator (a broker) elects one consumer as the group Leader
4. **Assign**: the Leader runs the assignment strategy和assigns partitions to consumers
5. **Resume**: all consumers receive their new assignments和resume reading

**Range assignment strategy** (the simplest):
- Sort the partition IDs和consumer IDs
- Divide partitions into contiguous ranges
- Example: 6 partitions, 3 consumers -> c1: [0,1], c2: [2,3], c3: [4,5]
- With uneven division: 7 partitions, 3 consumers -> c1: [0,1,2], c2: [3,4], c3: [5,6]

```JSON
请求:  {"type": "consumer_rebalance", "msg_id": 1, "group": "analytics", "consumers": ["c1", "c2", "c3"], "partitions": [0, 1, 2, 3, 4, 5], "strategy": "range"}
响应: {"type": "consumer_rebalance_ok", "in_reply_to": 1, "assignments": {"c1": [0, 1], "c2": [2, 3], "c3": [4, 5]}}

请求:  {"type": "consumer_rebalance", "msg_id": 2, "group": "analytics", "consumers": ["c1", "c2"], "partitions": [0, 1, 2, 3, 4, 5], "strategy": "range"}
响应: {"type": "consumer_rebalance_ok", "in_reply_to": 2, "assignments": {"c1": [0, 1, 2], "c2": [3, 4, 5]}}
```

## 涉及概念

- `consumer group`
- `rebalancing`
- `partition assignment`
- `range strategy`
- `group coordinator`

## 实现提示

- When a consumer joins or leaves a group, all partition assignments must be recalculated
- Range strategy: sort consumers和partitions, divide partitions into contiguous ranges per consumer
- During rebalancing, all consumers in the group pause consumption briefly (stop-the-world)
- The group coordinator (a broker) manages the rebalancing protocol
- Uneven distribution: if 6 partitions / 4 consumers, some consumers get 2和some get 1

## 测试用例

### 1. Even distribution: 6 partitions, 3 consumers

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

### 2. Redistribution after consumer leaves: 6 partitions, 2 consumers

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

- [Kafka Consumer Group Protocol](https://kafka.apache.org/documentation/#impl_consumerrebalance)：Kafka documentation on consumer group rebalancing protocol和partition assignment strategies

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
