# 添加 Virtual Nodes用于Even Distribution

英文标题：Add Virtual Nodes用于Even Distribution
网页：<https://builddistributedsystem.com/tracks/sharder/tasks/task-18-2-2-virtual-nodes>

课程：8. 分片器：水平扩展与数据迁移
任务序号：7
短标题：Virtual Nodes
难度：intermediate
子主题：Consistent Hashing

## 中文导读

本题要求你完成 `添加 Virtual Nodes用于Even Distribution`。

重点关注：`virtual nodes`、`vnodes`、`even distribution`、`load balancing`、`hash collision`。

建议先按提示逐步实现：With only 3 physical 节点, distribution is uneven (one 节点 may own 60% of keys)。

协议字段、消息类型、输入输出格式请以本文件中的代码块和测试用例为准。

## 题目说明

With few physical 节点, a consistent hash ring has uneven key distribution. Virtual 节点 fix this by giving each physical 节点 V positions on the ring.

**Problem**:，包含3 physical 节点, one 节点 might own 50% of the ring, another 35%,和the last 15%. This is because hash positions are pseudo-random.

**Solution**: create V virtual 节点用于each physical 节点 at positions `hash(node_id + "-" + i)`用于i in 0..V.

**Distribution quality** (V = virtual 节点 per physical 节点):
- V=1: high variance (~40% standard deviation)
- V=10: moderate (~15% standard deviation)
- V=150: low (~5.5% standard deviation)
- V=500: very low (~3% standard deviation)

```JSON
请求:  {"type": "ring_create", "msg_id": 1, "节点": ["n1", "n2", "n3"], "vnodes_per_node": 150}
响应: {"type": "ring_create_ok", "in_reply_to": 1, "total_vnodes": 450, "distribution": {"n1": 0.34, "n2": 0.33, "n3": 0.33}}
```

## 涉及概念

- `virtual nodes`
- `vnodes`
- `even distribution`
- `load balancing`
- `hash collision`

## 实现提示

- With only 3 physical 节点, distribution is uneven (one 节点 may own 60% of keys)
- Virtual 节点: each physical 节点 has V positions: hash(node_id + "-" + i)用于i in 0..V
- V=150 gives a standard deviation of ~5.5% around the ideal 1/N per 节点
- Key lookup: find the nearest vnode clockwise, then map vnode -> physical 节点
- More vnodes = better distribution, but more memory用于the ring data structure

## 测试用例

### 1. Virtual nodes improve distribution

Each 节点 should own roughly 33% of the ring.

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1","n2","n3"]}}
{"src":"c1","dest":"n1","body":{"type":"ring_create","msg_id":2,"nodes":["n1","n2","n3"],"vnodes_per_node":150}}
```

期望输出：

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

### 2. Total vnodes equals nodes * vnodes_per_node

total_vnodes should be 200.

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1","n2"]}}
{"src":"c1","dest":"n1","body":{"type":"ring_create","msg_id":2,"nodes":["n1","n2"],"vnodes_per_node":100}}
```

期望输出：

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

## 参考资料

- [DynamoDB Virtual Nodes](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/HowItWorks.Partitions.html)：AWS DynamoDB documentation on partition key distribution

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
