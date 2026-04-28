# 实现两阶段集合

英文标题：Implement Two-Phase Set (2P-Set)
网页：<https://builddistributedsystem.com/tracks/gossiper/tasks/task-3-4-2-twopset>

课程：3. 传播者：Gossip 信息传播
任务序号：17
短标题：两阶段集合
难度：高级
子主题：Epidemic Algorithms and CRDT Gossip

## 中文导读

这道题让你在只增集合的基础上更进一步，实现支持删除操作的两阶段集合（2P-Set）。它的巧妙之处在于：用两个只增集合分别记录"添加过的元素"和"删除过的元素"（即墓碑集合），最终结果就是二者的差集。不过要注意，一旦删除就无法再添加回来。这是理解 CRDT 中删除语义的关键一步。

## 题目说明

**两阶段集合（2P-Set）** 同时支持添加和删除操作。它内部维护两个只增集合：添加集合和删除集合（也叫墓碑集合）。一个元素是否"存在"，取决于它是否在添加集合中但不在删除集合中。

```json
请求:  {"type": "add", "msg_id": 1, "element": "x"}
响应: {"type": "add_ok", "in_reply_to": 1}

请求:  {"type": "remove", "msg_id": 2, "element": "x"}
响应: {"type": "remove_ok", "in_reply_to": 2}

请求:  {"type": "read", "msg_id": 3}
响应: {"type": "read_ok", "in_reply_to": 3, "elements": []}

请求:  {"type": "merge", "msg_id": 4, "add_set": ["a","b"], "remove_set": ["b"]}
响应: {"type": "merge_ok", "in_reply_to": 4}
```

## 涉及概念

- `2P-Set`
- `CRDT`
- `tombstone set`
- `add-remove semantics`

## 实现提示

- 两阶段集合内部包含两个只增集合：添加集合和删除集合
- 添加操作：将元素放入添加集合；删除操作：将元素放入删除集合
- 当前有效值 = 添加集合 - 删除集合
- 一旦元素被删除，就无法再重新添加（墓碑是永久性的）
- 合并时，两个只增集合各自独立地做并集运算

## 测试用例

### 1. 添加后读取

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

### 2. 添加后删除再读取

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"add","msg_id":2,"element":"y"}}
{"src":"c1","dest":"n1","body":{"type":"remove","msg_id":3,"element":"y"}}
{"src":"c1","dest":"n1","body":{"type":"read","msg_id":4}}
```

期望输出：

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
{"src": "n1", "dest": "c1", "body": {"type": "add_ok", "in_reply_to": 2, "msg_id": 1}}
{"src": "n1", "dest": "c1", "body": {"type": "remove_ok", "in_reply_to": 3, "msg_id": 2}}
{"src": "n1", "dest": "c1", "body": {"type": "read_ok", "elements": [], "in_reply_to": 4, "msg_id": 3}}
```

## 参考资料

- [CRDTs for Fun and Profit](https://bartoszsypytkowski.com/the-state-of-crdts/)：各种 CRDT 类型及其权衡的实用概述

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
