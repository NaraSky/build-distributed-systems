# 添加虚拟节点实现均匀分布

英文标题：Add Virtual Nodes for Even Distribution
网页：<https://builddistributedsystem.com/tracks/sharder/tasks/task-18-2-2-virtual-nodes>

课程：8. 分片器：水平扩展与数据迁移
任务序号：7
短标题：虚拟节点
难度：进阶
子主题：Consistent Hashing

## 中文导读

本题要求你通过虚拟节点（Virtual Nodes）来改善一致性哈希环上数据分布不均的问题。当物理节点较少时，由于哈希值的随机性，各节点负责的数据量可能差异很大。虚拟节点让每个物理节点在环上拥有多个位置，从而让数据分布更加均匀。

## 题目说明

当物理节点较少时，一致性哈希环上的键分布会不均匀。虚拟节点通过让每个物理节点在环上拥有 V 个位置来解决这个问题。

**问题**：假设只有 3 个物理节点，其中一个节点可能占据环的 50%，另一个占 35%，最后一个只占 15%。这是因为哈希位置是伪随机的。

**解决方案**：为每个物理节点创建 V 个虚拟节点，它们的位置分别在 `hash(node_id + "-" + i)`（i 从 0 到 V）。

**分布质量**（V 为每个物理节点的虚拟节点数）：
- V=1：方差很高（标准差约 40%）
- V=10：方差中等（标准差约 15%）
- V=150：方差较低（标准差约 5.5%）
- V=500：方差很低（标准差约 3%）

```json
Request:  {"type": "ring_create", "msg_id": 1, "nodes": ["n1", "n2", "n3"], "vnodes_per_node": 150}
Response: {"type": "ring_create_ok", "in_reply_to": 1, "total_vnodes": 450, "distribution": {"n1": 0.34, "n2": 0.33, "n3": 0.33}}
```

## 涉及概念

- `virtual nodes`
- `vnodes`
- `even distribution`
- `load balancing`
- `hash collision`

## 实现提示

- 仅有 3 个物理节点时，数据分布不均（某个节点可能拥有 60% 的键）
- 虚拟节点：每个物理节点拥有 V 个位置，计算方式为 `hash(node_id + "-" + i)`（i 从 0 到 V）
- V=150 时，各节点数据量的标准差约为理想值 1/N 的 5.5%
- 键查找：找到最近的顺时针虚拟节点，然后映射回物理节点
- 虚拟节点越多，分布越均匀，但环的数据结构占用的内存也越多

## 测试用例

### 1. 虚拟节点改善数据分布

每个节点应大致拥有环的 33%。

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1","n2","n3"]}}
{"src":"c1","dest":"n1","body":{"type":"ring_create","msg_id":2,"nodes":["n1","n2","n3"],"vnodes_per_node":150}}
```

期望输出：

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

### 2. 虚拟节点总数等于节点数乘以每节点虚拟节点数

total_vnodes 应为 200。

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

- [DynamoDB Virtual Nodes](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/HowItWorks.Partitions.html)：AWS DynamoDB 关于分区键分布的文档

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
