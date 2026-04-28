# 实现 Multi-Key Transactions as Atomic 日志 Entries

英文标题：Implement Multi-Key Transactions as Atomic Log Entries
网页：<https://builddistributedsystem.com/tracks/store/tasks/task-8-3-1-multi-key-txn>

课程：7. 存储：线性一致 KV Store
任务序号：11
短标题：Multi-Key Transactions
难度：advanced
子主题：Transactions on Raft

## 中文导读

本题要求你完成 `实现 Multi-Key Transactions as Atomic 日志 Entries`。

重点关注：`multi-key transaction`、`atomic batch`、`log entry`、`all-or-nothing`。

建议先按提示逐步实现：A 事务 is a batch of Get/Put/Delete operations committed as a single 日志 entry。

协议字段、消息类型、输入输出格式请以本文件中的代码块和测试用例为准。

## 题目说明

Implement multi-key transactions. A 事务 is a batch of operations committed as a single 日志 entry用于atomicity.

```JSON
请求:  {"type": "txn_execute", "msg_id": 1, "operations": [
    {"op": "put", "key": "balance_a", "value": "900"},
    {"op": "put", "key": "balance_b", "value": "1100"}
]}
响应: {"type": "txn_execute_ok", "in_reply_to": 1, "committed": true, "log_index": 5, "ops_applied": 2}

请求:  {"type": "txn_execute", "msg_id": 2, "operations": [
    {"op": "get", "key": "balance_a"},
    {"op": "get", "key": "balance_b"}
]}
响应: {"type": "txn_execute_ok", "in_reply_to": 2, "committed": true, "results": [
    {"op": "get", "key": "balance_a", "value": "900"},
    {"op": "get", "key": "balance_b", "value": "1100"}
]}
```

## 涉及概念

- `multi-key transaction`
- `atomic batch`
- `log entry`
- `all-or-nothing`

## 实现提示

- A 事务 is a batch of Get/Put/Delete operations committed as a single 日志 entry
- All operations in the batch succeed or fail together (atomicity)
- The batch is serialized as a single command in the Raft 日志
- The state machine applies all operations in the batch atomically
- If any operation fails validation, the entire batch is rejected

## 测试用例

### 1. Atomic multi-key write

First txn should commit both puts. Second txn should read a: "1"和b: "2".

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"txn_execute","msg_id":2,"operations":[{"op":"put","key":"a","value":"1"},{"op":"put","key":"b","value":"2"}]}}
{"src":"c1","dest":"n1","body":{"type":"txn_execute","msg_id":3,"operations":[{"op":"get","key":"a"},{"op":"get","key":"b"}]}}
```

期望输出：

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

## 参考资料

- [TiKV - Distributed Transactions](https://tikv.org/docs/deep-dive/distributed-transaction/introduction/)：How TiKV implements distributed transactions on top of Raft

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
