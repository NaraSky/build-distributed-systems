# 实现基于八卦传播的只增集合

英文标题：Implement Grow-Only Set (G-Set) with Gossip
网页：<https://builddistributedsystem.com/tracks/gossiper/tasks/task-3-4-1-gset>

课程：3. 传播者：Gossip 信息传播
任务序号：16
短标题：只增集合
难度：进阶
子主题：Epidemic Algorithms and CRDT Gossip

## 中文导读

这道题让你实现最简单的无冲突复制数据类型（CRDT）-- 只增集合（G-Set）。顾名思义，这个集合只能往里添加元素，不能删除。合并操作就是求并集，天然满足交换律、结合律和幂等性，非常适合通过八卦传播来实现最终一致性。这是理解所有 CRDT 的入门基础。

## 题目说明

**只增集合（G-Set）** 是最简单的无冲突复制数据类型（CRDT）。元素只能添加，不能删除。合并操作就是集合求并集，它满足交换律、结合律和幂等性，因此通过八卦传播就能保证最终一致性。

你需要实现一个通过八卦传播复制的只增集合：
1. `add` - 向集合中添加一个元素
2. `read` - 返回集合中的所有元素
3. `merge` - 与远端的只增集合合并（求并集）

```json
请求:  {"type": "add", "msg_id": 1, "element": "x"}
响应: {"type": "add_ok", "in_reply_to": 1}

请求:  {"type": "merge", "msg_id": 2, "elements": ["a","b","c"]}
响应: {"type": "merge_ok", "in_reply_to": 2, "new_count": 2}

请求:  {"type": "read", "msg_id": 3}
响应: {"type": "read_ok", "in_reply_to": 3, "elements": ["a","b","c","x"]}
```

## 涉及概念

- `G-Set`
- `CRDT`
- `set union`
- `eventual consistency`

## 实现提示

- 只增集合只支持添加操作，永远不能删除
- 合并就是简单的集合并集：合并结果 = 本地集合 | 远端集合
- 并集运算满足交换律、结合律和幂等性，天然适合八卦传播
- 因为集合只会增长不会缩小，所以收敛是有保障的
- 这是最简单的 CRDT 实现

## 测试用例

### 1. 添加元素后读取

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"add","msg_id":2,"element":"x"}}
{"src":"c1","dest":"n1","body":{"type":"read","msg_id":3}}
```

期望输出：

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
{"src": "n1", "dest": "c1", "body": {"type": "add_ok", "in_reply_to": 2, "msg_id": 1}}
{"src": "n1", "dest": "c1", "body": {"type": "read_ok", "elements": ["x"], "in_reply_to": 3, "msg_id": 2}}
```

### 2. 合并操作引入新元素

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"add","msg_id":2,"element":"a"}}
{"src":"n2","dest":"n1","body":{"type":"merge","msg_id":3,"elements":["a","b","c"]}}
{"src":"c1","dest":"n1","body":{"type":"read","msg_id":4}}
```

期望输出：

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
{"src": "n1", "dest": "c1", "body": {"type": "add_ok", "in_reply_to": 2, "msg_id": 1}}
{"src": "n1", "dest": "n2", "body": {"type": "merge_ok", "new_count": 2, "in_reply_to": 3, "msg_id": 2}}
{"src": "n1", "dest": "c1", "body": {"type": "read_ok", "elements": ["a", "b", "c"], "in_reply_to": 4, "msg_id": 3}}
```

## 参考资料

- [A Comprehensive Study of CRDTs](https://hal.inria.fr/inria-00555588/document)：Shapiro 等人对各种 CRDT 设计的综合调研

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
