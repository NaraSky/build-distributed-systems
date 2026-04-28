# 基准测试 Gossip KV 存储 Performance

英文标题：Benchmark Gossip KV Store Performance
网页：<https://builddistributedsystem.com/tracks/gossiper/tasks/task-3-4-5-gossip-kv-bench>

课程：3. 传播者：Gossip 信息传播
任务序号：20
短标题：Gossip KV Bench
难度：advanced
子主题：Epidemic Algorithms和CRDT Gossip

## 中文导读

本题要求你完成 `基准测试 Gossip KV 存储 Performance`。

重点关注：`benchmarking`、`convergence time`、`message overhead`、`consistency`。

建议先按提示逐步实现：Track total 消息 exchanged用于gossip sync。

协议字段、消息类型、输入输出格式请以本文件中的代码块和测试用例为准。

## 题目说明

Benchmark your gossip KV store to measure real-world performance characteristics:

1. **Convergence time**: How long until all replicas have the same value?
2. **消息 overhead**: How many gossip 消息 per write operation?
3. **Consistency violations**: How often does a read return stale data?

Implement a `bench_write` that tracks timing:
```JSON
请求:  {"type": "bench_write", "msg_id": 1, "key": "x", "value": "v1"}
响应: {"type": "bench_write_ok", "in_reply_to": 1, "write_id": 1}
```

And a `bench_report` endpoint:
```JSON
请求:  {"type": "bench_report", "msg_id": 2}
响应: {"type": "bench_report_ok", "in_reply_to": 2,
           "total_writes": 10, "total_gossip_msgs": 45,
           "msgs_per_write": 4.5, "keys_stored": 5}
```

## 涉及概念

- `benchmarking`
- `convergence time`
- `message overhead`
- `consistency`

## 实现提示

- Track total 消息 exchanged用于gossip sync
- Measure time from write to full convergence (all replicas agree)
- Count consistency violations: reads that return stale data
- Compare metrics under normal vs partition conditions
- Expose metrics via a bench_stats endpoint

## 测试用例

### 1. Bench write returns write_id

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"bench_write","msg_id":2,"key":"x","value":"v1"}}
```

期望输出：

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
{"src": "n1", "dest": "c1", "body": {"type": "bench_write_ok", "write_id": 1, "in_reply_to": 2, "msg_id": 1}}
```

### 2. Bench report，包含zero writes

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"bench_report","msg_id":2}}
```

期望输出：

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
{"src": "n1", "dest": "c1", "body": {"type": "bench_report_ok", "total_writes": 0, "total_gossip_msgs": 0, "msgs_per_write": 0, "keys_stored": 0, "in_reply_to": 2, "msg_id": 1}}
```

## 参考资料

- [Maelstrom Broadcast Workload](https://github.com/jepsen-io/maelstrom/blob/main/doc/workloads.md#broadcast)：Maelstrom 广播 workload specification

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
