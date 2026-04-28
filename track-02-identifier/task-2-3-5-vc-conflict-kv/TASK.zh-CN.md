# 向量 时钟 Conflict Detection in 键值 存储

英文标题：Vector Clock Conflict Detection in Key-Value Store
网页：<https://builddistributedsystem.com/tracks/identifier/tasks/task-2-3-5-vc-conflict-kv>

课程：2. 标识符：分布式唯一 ID
任务序号：15
短标题：VC Conflict KV
难度：advanced
子主题：Logical Clocks as IDs

## 中文导读

本题要求你完成 `向量 时钟 Conflict Detection in 键值 存储`。

重点关注：`conflict detection`、`key-value store`、`sibling values`、`last-writer-wins`。

建议先按提示逐步实现：Each key stores a value paired，包含the vector 时钟 at write time。

协议字段、消息类型、输入输出格式请以本文件中的代码块和测试用例为准。

## 题目说明

In databases like Riak, vector clocks detect **write conflicts**. When two clients write to the same key concurrently (neither saw the other's write), the database stores both values as **siblings** instead of silently losing one.

Implement a key-value store，包含vector 时钟-based conflict detection:

```JSON
Write: {"type": "vc_write", "msg_id": 1, "key": "x", "value": "a", "context": {"n1": 0}}
Read:  {"type": "vc_read", "msg_id": 2, "key": "x"}
```

Read 响应，包含single value:
```JSON
{"type": "vc_read_ok", "values": [{"value": "a", "vc": {"n1": 1}}], "siblings": 1}
```

Read 响应 after concurrent writes (conflict):
```JSON
{"type": "vc_read_ok", "values": [
    {"value": "a", "vc": {"n1": 1}},
    {"value": "b", "vc": {"n2": 1}}
], "siblings": 2}
```

## 涉及概念

- `conflict detection`
- `key-value store`
- `sibling values`
- `last-writer-wins`

## 实现提示

- Each key stores a value paired，包含the vector 时钟 at write time
- On write, the 客户端 provides the vector 时钟 it read (context)
- If the write VC dominates the stored VC, it is a simple update
- If the VCs are concurrent, store both values as siblings
- A read returns all sibling values和their VCs

## 测试用例

### 1. Write和read a single value

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"vc_write","msg_id":2,"key":"x","value":"hello","context":{}}}
{"src":"c1","dest":"n1","body":{"type":"vc_read","msg_id":3,"key":"x"}}
```

期望输出：

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
{"src": "n1", "dest": "c1", "body": {"type": "vc_write_ok", "key": "x", "vc": {"c1": 1}, "in_reply_to": 2, "msg_id": 1}}
{"src": "n1", "dest": "c1", "body": {"type": "vc_read_ok", "values": [{"value": "hello", "vc": {"c1": 1}}], "siblings": 1, "in_reply_to": 3, "msg_id": 2}}
```

### 2. Read nonexistent key returns empty

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"vc_read","msg_id":2,"key":"missing"}}
```

期望输出：

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
{"src": "n1", "dest": "c1", "body": {"type": "vc_read_ok", "values": [], "siblings": 0, "in_reply_to": 2, "msg_id": 1}}
```

## 参考资料

- [Dynamo: Amazon Highly Available Key-Value Store](https://www.allthingsdistributed.com/files/amazon-dynamo-sosp2007.pdf)：Amazon Dynamo paper describing vector 时钟 conflict resolution

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
