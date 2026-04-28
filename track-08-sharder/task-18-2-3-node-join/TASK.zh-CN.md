# 处理节点加入与最小化键迁移

英文标题：Handle Node Addition with Minimal Key Migration
网页：<https://builddistributedsystem.com/tracks/sharder/tasks/task-18-2-3-node-join>

课程：8. 分片器：水平扩展与数据迁移
任务序号：8
短标题：节点加入
难度：进阶
子主题：Consistent Hashing

## 中文导读

本题要求你处理新节点加入一致性哈希环时的键迁移过程。新节点加入后会接管其顺时针邻居的一部分键空间，关键在于只需迁移很少的键（约 1/N），而不是像取模哈希那样几乎全部重新分配。理解这个过程有助于你实现平滑的集群扩容。

## 题目说明

当一个节点加入哈希环时，它会接管其顺时针邻居的一部分键空间。只有落入新节点范围内的键需要迁移。

**加入流程**：
1. 新节点 N4 计算自己在环上的位置
2. N4 找到自己的顺时针邻居（后继节点）N2
3. 位于 N4 的逆时针邻居和 N4 之间的键从 N2 转移到 N4
4. 只有总键数的约 1/N 受到影响（最小化扰动）

**配合虚拟节点**：新节点会在环上占据 V 个位置，从多个现有节点各取一小段范围，使迁移负载均匀分散。

```json
Request:  {"type": "ring_add_node", "msg_id": 1, "new_node": "n4"}
Response: {"type": "ring_add_node_ok", "in_reply_to": 1, "keys_migrated": 250, "total_keys": 1000, "migration_pct": 25.0, "source_nodes": ["n1", "n2", "n3"]}
```

## 涉及概念

- `node addition`
- `key migration`
- `minimal disruption`
- `predecessor takeover`
- `data transfer`

## 实现提示

- 新节点加入时，从其顺时针邻居处接管键
- 只有新节点和它逆时针邻居之间的键需要迁移
- 迁移量约为总键数的 1/N（而取模哈希接近 100%）
- 迁移期间，旧的拥有者继续为迁移中的键提供读服务
- 迁移完成后，将新请求转发给新的拥有者

## 测试用例

### 1. 节点加入时大约迁移 1/N 的键

迁移百分比应大约为 25%（4 个节点时为 1/4）。

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1","n2","n3"]}}
{"src":"c1","dest":"n1","body":{"type":"ring_add_node","msg_id":2,"new_node":"n4"}}
```

期望输出：

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

### 2. 迁移后键仍可访问

`ring_lookup_ok` 应为已迁移的键返回新的拥有者。

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1","n2"]}}
{"src":"c1","dest":"n1","body":{"type":"ring_add_node","msg_id":2,"new_node":"n3"}}
{"src":"c1","dest":"n1","body":{"type":"ring_lookup","msg_id":3,"key":"migrated-key"}}
```

期望输出：

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

## 参考资料

- [Consistent Hashing: Node Addition](https://www.cs.princeton.edu/courses/archive/fall09/cos518/papers/chash.pdf)：Karger 等人关于一致性哈希与随机树的论文

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
