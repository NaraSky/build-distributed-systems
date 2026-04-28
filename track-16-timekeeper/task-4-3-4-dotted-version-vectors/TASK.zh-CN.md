# 实现 Dotted Version Vectors

英文标题：Implement Dotted Version Vectors
网页：<https://builddistributedsystem.com/tracks/timekeeper/tasks/task-4-3-4-dotted-version-vectors>

课程：16. 时间守卫：逻辑时钟
任务序号：14
短标题：Dotted Version Vectors
难度：advanced
子主题：向量 Clocks

## 中文导读

本题要求你完成 `实现 Dotted Version Vectors`。

重点关注：`dotted version vectors`、`space optimization`、`version vectors`、`Riak`。

建议先按提示逐步实现：Standard vector clocks grow linearly，包含the number of 节点 that ever participated。

协议字段、消息类型、输入输出格式请以本文件中的代码块和测试用例为准。

## 题目说明

Standard vector clocks have an O(N) 存储 cost that grows，包含every 节点 that ever participated. Dotted version vectors (DVVs), used in Riak, solve this by separating the **causal context** from the **event dot**.

A DVV has two parts:
- **dot**: `(node_id, 计数器)` — the single event this value represents
- **version_vector**: the causal context (everything that happened before the dot)

Implement a DVV-based versioning system:

```JSON
请求:  {"type": "dvv_update", "msg_id": 1, "key": "x", "value": "hello", "context": {}}
响应: {"type": "dvv_update_ok", "in_reply_to": 1, "dot": ["n1", 1], "version_vector": {}}

请求:  {"type": "dvv_update", "msg_id": 2, "key": "x", "value": "world", "context": {"n1": 1}}
响应: {"type": "dvv_update_ok", "in_reply_to": 2, "dot": ["n1", 2], "version_vector": {"n1": 1}}

请求:  {"type": "dvv_get", "msg_id": 3, "key": "x"}
响应: {"type": "dvv_get_ok", "in_reply_to": 3, "values": [{"value": "world", "dot": ["n1", 2]}], "context": {"n1": 2}}
```

## 涉及概念

- `dotted version vectors`
- `space optimization`
- `version vectors`
- `Riak`

## 实现提示

- Standard vector clocks grow linearly，包含the number of 节点 that ever participated
- Dotted version vectors separate the causal context (version vector) from the event dot
- A dot is a (node_id, 计数器) pair representing a single event
- The version vector represents everything that happened before the dot
- This allows pruning of old entries while preserving correctness

## 测试用例

### 1. First write creates a dot

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"dvv_update","msg_id":2,"key":"x","value":"hello","context":{}}}
```

期望输出：

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
{"src": "n1", "dest": "c1", "body": {"type": "dvv_update_ok", "in_reply_to": 2, "dot": ["n1", 1], "version_vector": {}, "msg_id": 1}}
```

### 2. Sequential update，包含context supersedes old value

dvv_get_ok should return only value v2，包含dot [n1, 2] since v1 was superseded by context.

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"dvv_update","msg_id":2,"key":"x","value":"v1","context":{}}}
{"src":"c1","dest":"n1","body":{"type":"dvv_update","msg_id":3,"key":"x","value":"v2","context":{"n1":1}}}
{"src":"c1","dest":"n1","body":{"type":"dvv_get","msg_id":4,"key":"x"}}
```

期望输出：

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

## 参考资料

- [Dotted Version Vectors - Riak Core Concepts](https://riak.com/posts/technical/vector-clocks-revisited-part-2-dotted-version-vectors/)：How Riak replaced vector clocks，包含dotted version vectors用于efficiency

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
