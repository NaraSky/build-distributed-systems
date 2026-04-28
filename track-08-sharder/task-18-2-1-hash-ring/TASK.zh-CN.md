# 实现一致性哈希环

英文标题：Implement a Consistent Hash Ring
网页：<https://builddistributedsystem.com/tracks/sharder/tasks/task-18-2-1-hash-ring>

课程：8. 分片器：水平扩展与数据迁移
任务序号：6
短标题：哈希环
难度：进阶
子主题：Consistent Hashing

## 中文导读

本题要求你实现一个一致性哈希环（Consistent Hash Ring）。一致性哈希的核心思想是把节点和键都映射到一个环形空间上，查找键时沿顺时针方向找到最近的节点。这种设计的最大优势在于：当节点增减时，只有约 1/N 的键需要迁移，而不是像取模哈希那样几乎全部重新分配。

## 题目说明

一致性哈希将节点（Node）和键放置在一个环形空间上，当节点加入或离开时，键的重新分配量最小。与取模哈希（`hash(key) % N`）不同，新增一个节点只会导致约 1/N 的键需要迁移。

**哈希环的构建**：
1. 对每个节点，计算 `position = hash(node_id) % 2^32`
2. 将节点放置在大小为 2^32 的环上

**键的查找**：
1. 计算 `position = hash(key) % 2^32`
2. 从该位置沿顺时针方向查找，直到遇到一个节点
3. 该节点即为这个键的归属节点

**节点加入时的键重分配**：只有位于新节点和它逆时针方向邻居之间的键需要迁移，其余所有键保持不变。

```json
Request:  {"type": "ring_lookup", "msg_id": 1, "key": "user:42"}
Response: {"type": "ring_lookup_ok", "in_reply_to": 1, "key": "user:42", "node": "n2", "position": 1048576}
```

## 涉及概念

- `consistent hashing`
- `hash ring`
- `key ownership`
- `clockwise lookup`
- `minimal disruption`

## 实现提示

- 在环上的 `hash(node_id) % 2^32` 位置放置节点
- 键归属于从 `hash(key) % 2^32` 出发顺时针方向遇到的第一个节点
- 当节点加入时，只有新节点和它前驱之间的键需要迁移
- 当节点离开时，只有它的键会转移给它的后继节点
- 与取模哈希对比：新增节点时约迁移 1/N 的键，而取模哈希几乎要迁移全部键

## 测试用例

### 1. 键映射到最近的顺时针节点

`ring_lookup_ok` 应该返回环上的一个有效节点。

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1","n2","n3"]}}
{"src":"c1","dest":"n1","body":{"type":"ring_lookup","msg_id":2,"key":"user:42"}}
```

期望输出：

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

### 2. 相同的键始终映射到相同的节点

两次查找应该返回同一个节点。

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1","n2"]}}
{"src":"c1","dest":"n1","body":{"type":"ring_lookup","msg_id":2,"key":"k1"}}
{"src":"c1","dest":"n1","body":{"type":"ring_lookup","msg_id":3,"key":"k1"}}
```

期望输出：

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

## 参考资料

- [Consistent Hashing](https://en.wikipedia.org/wiki/Consistent_hashing)：一致性哈希的维基百科词条

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
