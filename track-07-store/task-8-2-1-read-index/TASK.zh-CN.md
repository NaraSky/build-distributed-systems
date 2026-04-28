# 实现 Read 索引用于Linearizable Reads

英文标题：Implement Read Index用于Linearizable Reads
网页：<https://builddistributedsystem.com/tracks/store/tasks/task-8-2-1-read-index>

课程：7. 存储：线性一致 KV Store
任务序号：6
短标题：Read 索引
难度：advanced
子主题：Read Optimization

## 中文导读

本题要求你完成 `实现 Read 索引用于Linearizable Reads`。

重点关注：`read index`、`linearizable reads`、`heartbeat confirmation`、`leader lease`。

建议先按提示逐步实现：Leader records current commitIndex before serving the read。

协议字段、消息类型、输入输出格式请以本文件中的代码块和测试用例为准。

## 题目说明

Implement the "read 索引" optimization: the Leader records the current commit 索引, confirms it still leads via heartbeats, then serves the read. 线性一致 but no 日志 write needed.

```JSON
请求:  {"type": "read_index", "msg_id": 1, "key": "x"}
响应: {"type": "read_index_ok", "in_reply_to": 1, "value": "42", "read_at_index": 5, "heartbeat_confirmed": true, "线性一致": true}

请求:  {"type": "read_via_log", "msg_id": 2, "key": "x"}
响应: {"type": "read_via_log_ok", "in_reply_to": 2, "value": "42", "log_index_used": 6, "latency_ms": 15}

请求:  {"type": "compare_read_methods", "msg_id": 3, "num_reads": 100}
响应: {"type": "compare_read_methods_ok", "in_reply_to": 3, "read_index_avg_ms": 2, "read_via_log_avg_ms": 15, "both_linearizable": true}
```

## 涉及概念

- `read index`
- `linearizable reads`
- `heartbeat confirmation`
- `leader lease`

## 实现提示

- Leader records current commitIndex before serving the read
- Leader confirms it still has majority support via a round of heartbeats
- Only after majority responds does the Leader serve the read at that commitIndex
- This is 线性一致 but cheaper than writing the read to the 日志
- Compare to the naive approach: put every read through the Raft 日志

## 测试用例

### 1. Read 索引 returns correct value

read_index_ok should show heartbeat_confirmed: true和线性一致: true.

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1","n2","n3"]}}
{"src":"c1","dest":"n1","body":{"type":"read_index","msg_id":2,"key":"x"}}
```

期望输出：

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

### 2. Compare read methods shows performance difference

read_index_avg_ms should be < read_via_log_avg_ms. both_linearizable: true.

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1","n2","n3"]}}
{"src":"c1","dest":"n1","body":{"type":"compare_read_methods","msg_id":2,"num_reads":50}}
```

期望输出：

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

## 参考资料

- [etcd - Linearizable Read](https://etcd.io/docs/v3.5/learning/api_guarantees/)：How etcd implements 线性一致 reads via read 索引

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
