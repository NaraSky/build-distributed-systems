# 实现会合哈希（最高随机权重）

英文标题：Implement Rendezvous Hashing (Highest Random Weight)
网页：<https://builddistributedsystem.com/tracks/sharder/tasks/task-18-2-5-rendezvous-hashing>

课程：8. 分片器：水平扩展与数据迁移
任务序号：10
短标题：会合哈希
难度：高级
子主题：Consistent Hashing

## 中文导读

本题要求你实现会合哈希（Rendezvous Hashing），也叫最高随机权重（Highest Random Weight）算法。它是一致性哈希的替代方案，核心思路非常简单：对每个键，为所有节点计算一个分数，分数最高的节点"赢得"这个键。相比一致性哈希，会合哈希不需要维护环结构，实现起来更简单。

## 题目说明

会合哈希是一致性哈希的替代方案。对于每个键，它为所有节点计算一个分数，分数最高的节点获得该键的归属权。

**算法**：
1. 对于每个键 K 和每个节点 N：`score = hash(K + N)`
2. 将 K 分配给分数最高的节点
3. 当节点增减时，只需重新评估受影响的键

**相比一致性哈希的优势**：
- 实现更简单（不需要环数据结构）
- 无需虚拟节点即可实现完美分布
- 容易支持带权节点：`score = hash(K + N) * weight(N)`

**劣势**：
- 每次查找的时间复杂度为 O(N)（需要为所有节点计算分数），而环结构为 O(log N)
- 对于小规模集群（少于 100 个节点），O(N) 的开销可以忽略不计

```json
Request:  {"type": "hrw_lookup", "msg_id": 1, "key": "user:42", "nodes": ["n1", "n2", "n3"]}
Response: {"type": "hrw_lookup_ok", "in_reply_to": 1, "key": "user:42", "winner": "n2", "scores": {"n1": 12345, "n2": 99999, "n3": 45678}}
```

## 涉及概念

- `rendezvous hashing`
- `highest random weight`
- `HRW`
- `consistent hashing alternative`
- `weighted nodes`

## 实现提示

- 对于每个键，计算 `weight(key, node) = hash(key + node_id)`，需要对所有节点都计算
- 权重最高的节点拥有该键
- 当节点增减时，只有该节点曾经拥有最高权重的键会受到影响
- 比一致性哈希更简单：不需要环，不需要虚拟节点
- 天然支持带权节点：将哈希值乘以节点权重即可

## 测试用例

### 1. 返回分数最高的节点

winner 应为 scores 映射中分数最高的节点。

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1","n2","n3"]}}
{"src":"c1","dest":"n1","body":{"type":"hrw_lookup","msg_id":2,"key":"test","nodes":["n1","n2","n3"]}}
```

期望输出：

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

### 2. 相同的键始终映射到相同的节点

两次查找应返回相同的 winner。

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1","n2"]}}
{"src":"c1","dest":"n1","body":{"type":"hrw_lookup","msg_id":2,"key":"k","nodes":["n1","n2"]}}
{"src":"c1","dest":"n1","body":{"type":"hrw_lookup","msg_id":3,"key":"k","nodes":["n1","n2"]}}
```

期望输出：

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

## 参考资料

- [Rendezvous Hashing](https://en.wikipedia.org/wiki/Rendezvous_hashing)：会合哈希（最高随机权重）的维基百科词条

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
