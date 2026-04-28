# 实现 Multi-Version Concurrency Control

英文标题：Implement Multi-Version Concurrency Control
网页：<https://builddistributedsystem.com/tracks/store/tasks/task-8-3-3-mvcc>

课程：7. 存储：线性一致 KV Store
任务序号：13
短标题：MVCC
难度：advanced
子主题：Transactions on Raft

## 中文导读

本题要求你完成 `实现 Multi-Version Concurrency Control`。

重点关注：`MVCC`、`versioned storage`、`snapshot isolation`、`readers never block writers`。

建议先按提示逐步实现：Keep N versions of each key, each tagged，包含a commit timestamp。

协议字段、消息类型、输入输出格式请以本文件中的代码块和测试用例为准。

## 题目说明

Implement MVCC: keep multiple versions of each key. Readers get a consistent snapshot without blocking writers.

```JSON
请求:  {"type": "mvcc_put", "msg_id": 1, "key": "x", "value": "v1", "timestamp": 100}
响应: {"type": "mvcc_put_ok", "in_reply_to": 1, "version": 1, "timestamp": 100}

请求:  {"type": "mvcc_put", "msg_id": 2, "key": "x", "value": "v2", "timestamp": 200}
响应: {"type": "mvcc_put_ok", "in_reply_to": 2, "version": 2, "timestamp": 200}

请求:  {"type": "mvcc_get", "msg_id": 3, "key": "x", "read_timestamp": 150}
响应: {"type": "mvcc_get_ok", "in_reply_to": 3, "value": "v1", "version": 1, "as_of_timestamp": 100}

请求:  {"type": "mvcc_get", "msg_id": 4, "key": "x", "read_timestamp": 250}
响应: {"type": "mvcc_get_ok", "in_reply_to": 4, "value": "v2", "version": 2, "as_of_timestamp": 200}
```

## 涉及概念

- `MVCC`
- `versioned storage`
- `snapshot isolation`
- `readers never block writers`

## 实现提示

- Keep N versions of each key, each tagged，包含a commit timestamp
- Readers get a consistent snapshot at their start timestamp
- Writers create new versions without blocking readers
- Garbage collect old versions that are no longer needed
- This is how PostgreSQL, MySQL InnoDB,和TiKV work internally

## 测试用例

### 1. Read at old timestamp gets old version

mvcc_get_ok should return value: "old" since read_timestamp 150 < write timestamp 200.

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"mvcc_put","msg_id":2,"key":"x","value":"old","timestamp":100}}
{"src":"c1","dest":"n1","body":{"type":"mvcc_put","msg_id":3,"key":"x","value":"new","timestamp":200}}
{"src":"c1","dest":"n1","body":{"type":"mvcc_get","msg_id":4,"key":"x","read_timestamp":150}}
```

期望输出：

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

### 2. Read at current timestamp gets latest

mvcc_get_ok should return value: "new" since read_timestamp 300 > write timestamp 200.

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"mvcc_put","msg_id":2,"key":"x","value":"old","timestamp":100}}
{"src":"c1","dest":"n1","body":{"type":"mvcc_put","msg_id":3,"key":"x","value":"new","timestamp":200}}
{"src":"c1","dest":"n1","body":{"type":"mvcc_get","msg_id":4,"key":"x","read_timestamp":300}}
```

期望输出：

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

## 参考资料

- [MVCC in PostgreSQL](https://www.postgresql.org/docs/current/mvcc-intro.html)：How PostgreSQL implements MVCC用于concurrent access

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
