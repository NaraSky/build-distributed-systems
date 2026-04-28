# 构建 Transactional 键值 存储

英文标题：Build Transactional Key-Value Store
网页：<https://builddistributedsystem.com/tracks/coordinator/tasks/task-9-5-txn-kv>

课程：9. 协调器：分布式事务
任务序号：5
短标题：Txn KV
难度：advanced
子主题：Two-Phase Commit

## 中文导读

本题要求你完成 `构建 Transactional 键值 存储`。

重点关注：`transactions`、`ACID`、`isolation`。

建议先按提示逐步实现：Multi-key transactions。

协议字段、消息类型、输入输出格式请以本文件中的代码块和测试用例为准。

## 题目说明

Transactional KV: begin, read, write, commit/abort. Use 2PC用于cross-分片 transactions.

## 概念说明

### ACID

Atomic, Consistent, Isolated, Durable. Distributed transactions harder due to 网络 partitions.

## 涉及概念

- `transactions`
- `ACID`
- `isolation`

## 实现提示

- Multi-key transactions
- Use 2PC用于cross-分片
- Read-your-writes

## 测试用例

### 1. Begin 事务

响应 contains txn_begin_ok，包含a unique 事务 ID. 事务 should be in active state.

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"txn_begin","msg_id":2}}
```

期望输出：

```text
{"src":"n1","dest":"c0","body":{"type":"init_ok","in_reply_to":1,"msg_id":0}}
{"src":"n1","dest":"c1","body":{"type":"txn_begin_ok","in_reply_to":2,"msg_id":1,"tx_id":"tx1"}}
```

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
