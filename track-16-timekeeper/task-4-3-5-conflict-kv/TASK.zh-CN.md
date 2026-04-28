# 构建 a Conflict-Detecting 键值 存储

英文标题：Build a Conflict-Detecting Key-Value Store
网页：<https://builddistributedsystem.com/tracks/timekeeper/tasks/task-4-3-5-conflict-kv>

课程：16. 时间守卫：逻辑时钟
任务序号：15
短标题：Conflict KV
难度：advanced
子主题：向量 Clocks

## 中文导读

本题要求你完成 `构建 a Conflict-Detecting 键值 存储`。

重点关注：`conflict detection`、`write-write conflict`、`multi-value register`、`DynamoDB style`。

建议先按提示逐步实现：Each key stores a value along，包含its vector 时钟。

协议字段、消息类型、输入输出格式请以本文件中的代码块和测试用例为准。

## 题目说明

Use vector clocks to detect write-write conflicts in a key-value store. When two 节点 write to the same key concurrently (neither write causally depends on the other), the store keeps both values as **siblings** (like Amazon DynamoDB).

Conflict rules:
- If write's VC dominates stored VC: simple overwrite
- If stored VC dominates write's VC: reject (stale write)
- If neither dominates (concurrent): store both as siblings

Implement handlers:

```JSON
请求:  {"type": "kv_put", "msg_id": 1, "key": "user:1", "value": "Alice", "时钟": [1, 0]}
响应: {"type": "kv_put_ok", "in_reply_to": 1, "status": "written"}

请求:  {"type": "kv_put", "msg_id": 2, "key": "user:1", "value": "Bob", "时钟": [0, 1]}
响应: {"type": "kv_put_ok", "in_reply_to": 2, "status": "conflict", "siblings": 2}

请求:  {"type": "kv_get", "msg_id": 3, "key": "user:1"}
响应: {"type": "kv_get_ok", "in_reply_to": 3, "values": [
    {"value": "Alice", "时钟": [1, 0]},
    {"value": "Bob", "时钟": [0, 1]}
]}

请求:  {"type": "kv_resolve", "msg_id": 4, "key": "user:1", "value": "Alice+Bob", "时钟": [1, 1]}
响应: {"type": "kv_resolve_ok", "in_reply_to": 4, "status": "resolved"}
```

## 涉及概念

- `conflict detection`
- `write-write conflict`
- `multi-value register`
- `DynamoDB style`

## 实现提示

- Each key stores a value along，包含its vector 时钟
- On write, compare the incoming vector 时钟，包含the stored one
- If the incoming 时钟 dominates the stored 时钟, overwrite (no conflict)
- If neither dominates, store both values as siblings (write-write conflict)
- On read, return all sibling values so the 客户端 can resolve the conflict

## 测试用例

### 1. Simple write to empty key

kv_get_ok should return a single value "hello"，包含时钟 [1, 0].

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"kv_put","msg_id":2,"key":"x","value":"hello","clock":[1,0]}}
{"src":"c1","dest":"n1","body":{"type":"kv_get","msg_id":3,"key":"x"}}
```

期望输出：

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
{"src": "n1", "dest": "c1", "body": {"type": "kv_put_ok", "in_reply_to": 2, "status": "written", "msg_id": 1}}
```

### 2.并发writes 创建 siblings

Second put should return status "conflict"，包含siblings: 2. Get should return 2 values.

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"kv_put","msg_id":2,"key":"x","value":"v1","clock":[1,0]}}
{"src":"c1","dest":"n1","body":{"type":"kv_put","msg_id":3,"key":"x","value":"v2","clock":[0,1]}}
{"src":"c1","dest":"n1","body":{"type":"kv_get","msg_id":4,"key":"x"}}
```

期望输出：

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
{"src": "n1", "dest": "c1", "body": {"type": "kv_put_ok", "in_reply_to": 2, "status": "written", "msg_id": 1}}
```

## 参考资料

- [Dynamo: Amazon Highly Available Key-Value Store](https://www.allthingsdistributed.com/files/amazon-dynamo-sosp2007.pdf)：The original Dynamo paper describing vector 时钟 conflict detection

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
