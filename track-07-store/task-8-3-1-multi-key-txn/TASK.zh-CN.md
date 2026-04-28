# 实现多键事务的原子日志条目

英文标题：Implement Multi-Key Transactions as Atomic Log Entries
网页：<https://builddistributedsystem.com/tracks/store/tasks/task-8-3-1-multi-key-txn>

课程：7. 存储：线性一致键值存储
任务序号：11
短标题：Multi-Key Transactions
难度：高级
子主题：基于 Raft 的事务

## 中文导读

这道题要求你实现多键事务（Multi-Key Transaction）。之前的任务只涉及单个键的操作，而现实中的应用常常需要同时修改多个键，比如转账时同时扣减一方余额、增加另一方余额。这道题让你把一组操作打包成一条日志条目，保证它们要么全部执行，要么全部不执行。

## 题目说明

实现多键事务。一个事务（Transaction）是一批操作的集合，作为单条日志条目提交，从而保证原子性。

```json
Request:  {"type": "txn_execute", "msg_id": 1, "operations": [
    {"op": "put", "key": "balance_a", "value": "900"},
    {"op": "put", "key": "balance_b", "value": "1100"}
]}
Response: {"type": "txn_execute_ok", "in_reply_to": 1, "committed": true, "log_index": 5, "ops_applied": 2}

Request:  {"type": "txn_execute", "msg_id": 2, "operations": [
    {"op": "get", "key": "balance_a"},
    {"op": "get", "key": "balance_b"}
]}
Response: {"type": "txn_execute_ok", "in_reply_to": 2, "committed": true, "results": [
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

- 一个事务是一批 Get/Put/Delete 操作，作为单条日志条目一起提交
- 批次中的所有操作要么全部成功，要么全部失败（原子性）
- 整个批次作为一条命令序列化写入 Raft 日志
- 状态机在应用时原子地执行批次中的所有操作
- 如果任何一个操作校验失败，整个批次都会被拒绝

## 测试用例

### 1. 原子多键写入

第一个事务应该同时提交两个 put 操作。第二个事务读取时应该返回 a 为 "1"、b 为 "2"。

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

- [TiKV - Distributed Transactions](https://tikv.org/docs/deep-dive/distributed-transaction/introduction/)：TiKV 如何在 Raft 之上实现分布式事务

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
