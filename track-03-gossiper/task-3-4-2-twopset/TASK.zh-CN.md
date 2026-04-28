# 实现 Two-Phase Set (2P-Set)

英文标题：Implement Two-Phase Set (2P-Set)
网页：<https://builddistributedsystem.com/tracks/gossiper/tasks/task-3-4-2-twopset>

课程：3. 传播者：Gossip 信息传播
任务序号：17
短标题：2P-Set
难度：advanced
子主题：Epidemic Algorithms和CRDT Gossip

## 中文导读

本题要求你完成 `实现 Two-Phase Set (2P-Set)`。

重点关注：`2P-Set`、`CRDT`、`tombstone set`、`add-remove semantics`。

建议先按提示逐步实现：A 2P-Set has two internal G-Sets: add-set和remove-set。

协议字段、消息类型、输入输出格式请以本文件中的代码块和测试用例为准。

## 题目说明

A **2P-Set** (two-phase set) supports both add和remove by maintaining two G-Sets: the add-set和the remove-set (tombstones). An element is in the set if it is in the add-set but NOT in the remove-set.

```JSON
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

- A 2P-Set has two internal G-Sets: add-set和remove-set
- To add: insert into add-set. To remove: insert into remove-set
- Value = add-set - remove-set
- Once removed, an element cannot be re-added (tombstone is permanent)
- Merge both G-Sets independently via union

## 测试用例

### 1. 添加 then read

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

### 2. 添加 then remove then read

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

- [CRDTs用于Fun和Profit](https://bartoszsypytkowski.com/the-state-of-crdts/)：Practical overview of CRDT types和their tradeoffs

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
