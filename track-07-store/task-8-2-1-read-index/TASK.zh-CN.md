# 实现 ReadIndex 线性一致读优化

网页：<https://builddistributedsystem.com/tracks/store/tasks/task-8-2-1-read-index>

课程：7. 存储：线性一致键值存储
任务序号：6
短标题：ReadIndex
难度：高级
子主题：读优化

## 中文导读

在基于 Raft 的系统中，最简单的保证线性一致性的做法是把每个读请求都当作写请求一样走一遍日志。这样虽然正确，但代价太高了。ReadIndex 是一种巧妙的优化：领导者只需要通过一轮心跳确认自己还是领导者，就可以直接从本地状态读取数据，既保证了线性一致性，又大幅降低了延迟。

这道题让你实现 ReadIndex 优化方案，并与朴素的日志读取方式做性能对比，体会两者的差异。

## 题目说明

实现 ReadIndex 读优化方案。具体流程是：领导者（Leader）先记录当前的提交索引（Commit Index），然后通过一轮心跳（Heartbeat）向其他节点确认自己仍然是领导者，确认后直接在本地处理读请求。这种方式保证了线性一致性，同时避免了将读请求写入日志的开销。

你需要实现三种消息处理器：

`read_index` 使用 ReadIndex 方式读取指定键的值：

```json
Request:  {"type": "read_index", "msg_id": 1, "key": "x"}
Response: {"type": "read_index_ok", "in_reply_to": 1, "value": "42", "read_at_index": 5, "heartbeat_confirmed": true, "linearizable": true}
```

`read_via_log` 使用传统的日志方式读取，即把读请求写入 Raft 日志：

```json
Request:  {"type": "read_via_log", "msg_id": 2, "key": "x"}
Response: {"type": "read_via_log_ok", "in_reply_to": 2, "value": "42", "log_index_used": 6, "latency_ms": 15}
```

`compare_read_methods` 对比两种读方式的性能：

```json
Request:  {"type": "compare_read_methods", "msg_id": 3, "num_reads": 100}
Response: {"type": "compare_read_methods_ok", "in_reply_to": 3, "read_index_avg_ms": 2, "read_via_log_avg_ms": 15, "both_linearizable": true}
```

## 涉及概念

- `read index`
- `linearizable reads`
- `heartbeat confirmation`
- `leader lease`

## 实现提示

- 领导者在处理读请求之前，先记下当前的 commitIndex
- 然后发起一轮心跳，确认自己仍然得到多数节点的认可
- 只有在多数节点响应心跳之后，领导者才能基于之前记录的 commitIndex 处理读请求
- 这种方式和走日志一样保证线性一致性，但延迟低得多
- 可以和朴素方案做对比：朴素方案是把每个读请求都经过 Raft 日志提交

## 测试用例

### 1. ReadIndex 返回正确的值

验证 `read_index_ok` 响应中包含 `heartbeat_confirmed: true` 和 `linearizable: true`。

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1","n2","n3"]}}
{"src":"c1","dest":"n1","body":{"type":"read_index","msg_id":2,"key":"x"}}
```

期望输出：

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

### 2. 对比两种读方式的性能差异

验证 `read_index_avg_ms` 应小于 `read_via_log_avg_ms`，且 `both_linearizable` 为 true。

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

- [etcd - Linearizable Read](https://etcd.io/docs/v3.5/learning/api_guarantees/)：etcd 如何通过 ReadIndex 机制实现线性一致读的文档

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
