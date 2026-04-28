# 实现 a Multi-Value Register (MV-Register)

英文标题：Implement a Multi-Value Register (MV-Register)
网页：<https://builddistributedsystem.com/tracks/counter/tasks/task-17-3-2-mv-register>

课程：4. 计数器：分布式状态与 CRDT
任务序号：12
短标题：MV-Register
难度：advanced
子主题：More CRDTs

## 中文导读

本题要求你完成 `实现 a Multi-Value Register (MV-Register)`。

重点关注：`MV-Register`、`concurrent writes`、`sibling values`、`vector clock`、`conflict resolution`。

建议先按提示逐步实现：Each write is tagged，包含a vector 时钟 timestamp。

协议字段、消息类型、输入输出格式请以本文件中的代码块和测试用例为准。

## 题目说明

A Multi-Value Register (MV-Register) handles concurrent writes by keeping ALL concurrent values as siblings. The 客户端 resolves conflicts on read.

**How it works**:
- Each value is tagged，包含a vector 时钟
- `write("v1")` at vector 时钟 {A:1} -> stores ("v1", {A:1})
- `write("v2")` at vector 时钟 {B:1} (concurrent) -> stores ("v2", {B:1})
- `read()` returns ["v1", "v2"] (both siblings, 客户端 picks)
- `write("v3")` at vector 时钟 {A:1, B:1} (causally after both) -> replaces both

This is the approach used by Amazon DynamoDB和Riak. It maximizes availability (never rejects a write) at the cost of forcing the 客户端 to handle conflicts.

```JSON
请求:  {"type": "mv_write", "msg_id": 1, "key": "cart", "value": ["item1", "item2"]}
响应: {"type": "mv_write_ok", "in_reply_to": 1, "vclock": {"n1": 1}}

请求:  {"type": "mv_read", "msg_id": 2, "key": "cart"}
响应: {"type": "mv_read_ok", "in_reply_to": 2, "values": [{"value": ["item1", "item2"], "vclock": {"n1": 1}}, {"value": ["item1", "item3"], "vclock": {"n2": 1}}]}
```

## 涉及概念

- `MV-Register`
- `concurrent writes`
- `sibling values`
- `vector clock`
- `conflict resolution`

## 实现提示

- Each write is tagged，包含a vector 时钟 timestamp
-并发writes produce multiple sibling values (like DynamoDB)
- On read, return ALL concurrent values — the 客户端 resolves the conflict
- A write that causally follows another replaces it (not concurrent)
- Merge: keep all values from concurrent writes, discard causally dominated ones

## 测试用例

### 1. Write和read single value

mv_read_ok values should contain exactly one entry，包含value "v1".

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"mv_write","msg_id":2,"key":"k","value":"v1"}}
{"src":"c1","dest":"n1","body":{"type":"mv_read","msg_id":3,"key":"k"}}
```

期望输出：

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

### 2.并发writes produce siblings

mv_read_ok values should contain two siblings: "v1"和"v2".

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1","n2"]}}
{"src":"c1","dest":"n1","body":{"type":"mv_write","msg_id":2,"key":"k","value":"v1"}}
{"src":"n2","dest":"n1","body":{"type":"mv_merge","msg_id":3,"key":"k","entry":{"value":"v2","vclock":{"n2":1}}}}
{"src":"c1","dest":"n1","body":{"type":"mv_read","msg_id":4,"key":"k"}}
```

期望输出：

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

## 参考资料

- [DynamoDB Conflict Resolution](https://www.allthingsdistributed.com/files/amazon-dynamo-sosp2007.pdf)：DeCandia et al. - Dynamo: Amazon Highly Available Key-value Store

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
