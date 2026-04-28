# 实现 Optimistic Concurrency Control

英文标题：Implement Optimistic Concurrency Control
网页：<https://builddistributedsystem.com/tracks/store/tasks/task-8-3-2-occ>

课程：7. 存储：线性一致 KV Store
任务序号：12
短标题：OCC
难度：advanced
子主题：Transactions on Raft

## 中文导读

本题要求你完成 `实现 Optimistic Concurrency Control`。

重点关注：`OCC`、`version check`、`conflict detection`、`abort和retry`。

建议先按提示逐步实现：Read a set of keys和record their versions。

协议字段、消息类型、输入输出格式请以本文件中的代码块和测试用例为准。

## 题目说明

Implement optimistic concurrency control (OCC). Read keys，包含version tracking, then commit only if no versions changed since the read.

```JSON
请求:  {"type": "occ_begin", "msg_id": 1}
响应: {"type": "occ_begin_ok", "in_reply_to": 1, "txn_id": "t1"}

请求:  {"type": "occ_read", "msg_id": 2, "txn_id": "t1", "key": "x"}
响应: {"type": "occ_read_ok", "in_reply_to": 2, "value": "42", "version": 5}

请求:  {"type": "occ_commit", "msg_id": 3, "txn_id": "t1", "writes": [{"key": "x", "value": "43"}], "read_versions": [{"key": "x", "version": 5}]}
响应: {"type": "occ_commit_ok", "in_reply_to": 3, "committed": true, "new_version": 6}
```

## 涉及概念

- `OCC`
- `version check`
- `conflict detection`
- `abort和retry`

## 实现提示

- Read a set of keys和record their versions
- At commit time, check that none of the versions have changed
- If versions match, the 事务 commits. Otherwise, abort和重试
- OCC works well when conflicts are rare (optimistic assumption)
- High contention leads to many aborts和retries

## 测试用例

### 1. OCC commit succeeds，包含matching versions

occ_commit_ok should show committed: true.

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"occ_begin","msg_id":2}}
{"src":"c1","dest":"n1","body":{"type":"occ_commit","msg_id":3,"txn_id":"t1","writes":[{"key":"x","value":"1"}],"read_versions":[]}}
```

期望输出：

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

### 2. OCC aborts on version mismatch

occ_commit_ok should show committed: false because version 999 does not match actual.

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"occ_commit","msg_id":2,"txn_id":"t1","writes":[{"key":"x","value":"new"}],"read_versions":[{"key":"x","version":999}]}}
```

期望输出：

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

## 参考资料

- [Optimistic Concurrency Control](https://en.wikipedia.org/wiki/Optimistic_concurrency_control)：OCC overview: read, validate, write phases

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
