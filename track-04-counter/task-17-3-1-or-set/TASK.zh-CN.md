# 实现 an OR-Set (Observed-Remove Set)

英文标题：Implement an OR-Set (Observed-Remove Set)
网页：<https://builddistributedsystem.com/tracks/counter/tasks/task-17-3-1-or-set>

课程：4. 计数器：分布式状态与 CRDT
任务序号：11
短标题：OR-Set
难度：advanced
子主题：More CRDTs

## 中文导读

本题要求你完成 `实现 an OR-Set (Observed-Remove Set)`。

重点关注：`OR-Set`、`observed-remove`、`unique tags`、`add-wins semantics`、`concurrent remove`。

建议先按提示逐步实现：Each element is stored，包含a unique tag (UUID) when added。

协议字段、消息类型、输入输出格式请以本文件中的代码块和测试用例为准。

## 题目说明

The OR-Set (Observed-Remove Set) solves the concurrent add/remove problem. Each element is tagged，包含a unique identifier,和remove only removes tags that have been observed.

**Problem，包含naive sets**: if 节点 A adds "x"和节点 B concurrently removes "x", what happens? With a naive set, the result depends on 消息 ordering — non-deterministic.

**OR-Set solution**:
- `add("x")`: store `("x", tag_1)` where tag_1 is a unique UUID
- `remove("x")`: remove ALL currently visible pairs用于"x": `{("x", tag_1)}`
- If 节点 A does `add("x")` concurrently，包含节点 B doing `remove("x")`: 节点 A's add creates tag_2, which 节点 B has never seen. After merge, `("x", tag_2)` survives. **Add wins.**

```JSON
请求:  {"type": "or_set_add", "msg_id": 1, "element": "apple"}
响应: {"type": "or_set_add_ok", "in_reply_to": 1, "tag": "uuid-001"}

请求:  {"type": "or_set_remove", "msg_id": 2, "element": "apple"}
响应: {"type": "or_set_remove_ok", "in_reply_to": 2, "tags_removed": ["uuid-001"]}

请求:  {"type": "or_set_read", "msg_id": 3}
响应: {"type": "or_set_read_ok", "in_reply_to": 3, "elements": ["banana", "cherry"]}
```

## 涉及概念

- `OR-Set`
- `observed-remove`
- `unique tags`
- `add-wins semantics`
- `concurrent remove`

## 实现提示

- Each element is stored，包含a unique tag (UUID) when added
- add(e) creates a new entry: (element, unique_tag)
- remove(e) removes all currently observed (element, tag) pairs用于that element
-并发add + remove: the new add has a tag not yet observed by the remove, so it survives
- Merge: union of all (element, tag) pairs from both replicas

## 测试用例

### 1. 添加和read element

or_set_read_ok elements should include "apple".

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"or_set_add","msg_id":2,"element":"apple"}}
{"src":"c1","dest":"n1","body":{"type":"or_set_read","msg_id":3}}
```

期望输出：

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

### 2. Remove deletes element

or_set_read_ok elements should NOT include "banana" after removal.

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"or_set_add","msg_id":2,"element":"banana"}}
{"src":"c1","dest":"n1","body":{"type":"or_set_remove","msg_id":3,"element":"banana"}}
{"src":"c1","dest":"n1","body":{"type":"or_set_read","msg_id":4}}
```

期望输出：

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

## 参考资料

- [OR-Set CRDT](https://en.wikipedia.org/wiki/Conflict-free_replicated_data_type#OR-Set)：Wikipedia article on OR-Set (Observed-Remove Set) CRDT

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
