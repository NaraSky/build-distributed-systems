# 实现 Grow-Only Set (G-Set)，包含Gossip

英文标题：Implement Grow-Only Set (G-Set)，包含Gossip
网页：<https://builddistributedsystem.com/tracks/gossiper/tasks/task-3-4-1-gset>

课程：3. 传播者：Gossip 信息传播
任务序号：16
短标题：G-Set
难度：intermediate
子主题：Epidemic Algorithms和CRDT Gossip

## 中文导读

本题要求你完成 `实现 Grow-Only Set (G-Set)，包含Gossip`。

重点关注：`G-Set`、`CRDT`、`set union`、`eventual consistency`。

建议先按提示逐步实现：A G-Set only supports add operations, never remove。

协议字段、消息类型、输入输出格式请以本文件中的代码块和测试用例为准。

## 题目说明

A **Grow-only Set (G-Set)** is the simplest CRDT. Elements can be added but never removed. Merge is set union, which is commutative, associative,和idempotent - guaranteeing 最终一致性 via gossip.

Implement a G-Set replicated via gossip:
1. `add` - Add an element to the set
2. `read` - Return all elements
3. `merge` - Merge a remote G-Set (union)

```JSON
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

- A G-Set only supports add operations, never remove
- Merge is simply set union: merged = local | remote
- Union is commutative, associative,和idempotent - perfect用于gossip
- Convergence is guaranteed because sets only grow
- This is the simplest CRDT to implement

## 测试用例

### 1. 添加和read

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

### 2. Merge adds new elements

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

- [A Comprehensive Study of CRDTs](https://hal.inria.fr/inria-00555588/document)：Shapiro et al. survey of CRDT designs

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
