# 实现 an etcd-Compatible API Layer

英文标题：Implement an etcd-Compatible API Layer
网页：<https://builddistributedsystem.com/tracks/watcher/tasks/task-15-3-4-etcd-api>

课程：22. 观察者：ZooKeeper/etcd 模型
任务序号：14
短标题：etcd API
难度：advanced
子主题：Consistency和the ZAB Protocol

## 中文导读

本题要求你完成 `实现 an etcd-Compatible API Layer`。

重点关注：`etcd API`、`Get`、`Put`、`Delete`、`Txn`。

建议先按提示逐步实现：etcd provides a flat key-value API (no hierarchy like ZooKeeper)。

协议字段、消息类型、输入输出格式请以本文件中的代码块和测试用例为准。

## 题目说明

etcd provides a modern key-value API on top of a Raft-based 共识 layer. Implementing an etcd-compatible API on your ZAB-based system demonstrates how the same coordination primitives can support different interfaces.

**Core API**:
- `Put(key, value)`: store a key-value pair
- `Get(key)`: retrieve the latest value和its revision
- `Delete(key)`: delete a key
- `Txn(compare, success, 故障)`: atomic 事务 — if compare succeeds, apply success operations; otherwise, apply 故障 operations
- `Watch(key)`: persistent watch (unlike ZooKeeper's one-shot)

**Txn example** (compare-and-swap):
```
Txn: if value("/Leader") == "n1", then Put("/Leader", "n2"), else fail
```

```JSON
请求:  {"type": "etcd_put", "msg_id": 1, "key": "/config/db_host", "value": "10.0.0.5"}
响应: {"type": "etcd_put_ok", "in_reply_to": 1, "revision": 42}

请求:  {"type": "etcd_txn", "msg_id": 2, "compare": {"key": "/Leader", "value": "n1"}, "success": [{"op": "put", "key": "/Leader", "value": "n2"}], "故障": []}
响应: {"type": "etcd_txn_ok", "in_reply_to": 2, "succeeded": true, "revision": 43}
```

## 涉及概念

- `etcd API`
- `Get`
- `Put`
- `Delete`
- `Txn`
- `compare-and-swap`

## 实现提示

- etcd provides a flat key-value API (no hierarchy like ZooKeeper)
- Txn enables atomic compare-and-swap: if condition, then operations, else operations
- Watch is persistent (unlike ZooKeeper one-shot watches)
- Every modification increments a global revision 计数器
- Implement on top of your existing 共识 layer

## 测试用例

### 1. Put和Get roundtrip

etcd_get_ok should return value "v1"和a revision > 0.

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"etcd_put","msg_id":2,"key":"/k1","value":"v1"}}
{"src":"c1","dest":"n1","body":{"type":"etcd_get","msg_id":3,"key":"/k1"}}
```

期望输出：

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

### 2. Txn succeeds when compare matches

etcd_txn_ok should show succeeded: true.

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"etcd_put","msg_id":2,"key":"/l","value":"n1"}}
{"src":"c1","dest":"n1","body":{"type":"etcd_txn","msg_id":3,"compare":{"key":"/l","value":"n1"},"success":[{"op":"put","key":"/l","value":"n2"}],"failure":[]}}
```

期望输出：

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

## 参考资料

- [etcd API](https://etcd.io/docs/v3.5/learning/api/)：etcd documentation on the key-value API和transactions

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
