# 基准测试 WAL fsync Strategies

英文标题：Benchmark WAL fsync Strategies
网页：<https://builddistributedsystem.com/tracks/logger/tasks/task-10-1-5-fsync-bench>

课程：19. 日志器：WAL、LSM 与分布式日志
任务序号：5
短标题：fsync 基准测试
难度：intermediate
子主题：The Commit 日志 (WAL)

## 中文导读

本题要求你完成 `基准测试 WAL fsync Strategies`。

重点关注：`fsync`、`durability`、`throughput tradeoff`、`batch sync`、`OS buffering`。

建议先按提示逐步实现：Always fsync: every write is durable on disk. Throughput is limited by disk IOPS (~500 ops/sec on HDD)。

协议字段、消息类型、输入输出格式请以本文件中的代码块和测试用例为准。

## 题目说明

The `fsync` system call forces the OS to flush data from kernel buffers to the physical disk. Without it, data that appears "written" may only exist in volatile RAM buffers和will be lost on power 故障.

The fundamental tradeoff: **durability vs. throughput**.

Three strategies, from safest to fastest:
1. **Always fsync**: call fsync after every write. Every acknowledged entry is durable. Throughput limited by disk IOPS.
2. **Batch fsync**: buffer writes和fsync every 10ms. Up to 10ms of writes can be lost on crash. 10-30x higher throughput.
3. **No fsync**: let the OS decide when to flush. Crashes can lose seconds of data. 100x+ higher throughput.

Benchmark all three和measure ops/sec, then plot the durability vs. throughput curve.

```JSON
请求:  {"type": "fsync_benchmark", "msg_id": 1, "entries": 10000, "strategies": ["always", "batch_10ms", "none"]}
响应: {"type": "fsync_benchmark_ok", "in_reply_to": 1, "results": [
    {"strategy": "always", "ops_per_sec": 500, "durability": "every_write", "data_loss_window": "0ms"},
    {"strategy": "batch_10ms", "ops_per_sec": 15000, "durability": "every_10ms", "data_loss_window": "10ms"},
    {"strategy": "none", "ops_per_sec": 100000, "durability": "os_dependent", "data_loss_window": "seconds"}
]}
```

## 涉及概念

- `fsync`
- `durability`
- `throughput tradeoff`
- `batch sync`
- `OS buffering`

## 实现提示

- Always fsync: every write is durable on disk. Throughput is limited by disk IOPS (~500 ops/sec on HDD)
- Batch fsync every 10ms: group writes和sync once per batch. Good balance — can lose up to 10ms of data
- No fsync: let the OS buffer和flush when it wants. Highest throughput, but crashes can lose seconds of data
- SSDs have much higher fsync throughput than HDDs (~10,000+ ops/sec)
- Production systems like PostgreSQL offer wal_sync_method config to choose the strategy

## 测试用例

### 1. 基准测试 all three strategies

Results should show 3 entries，包含ops_per_sec increasing: always < batch_10ms < none.

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"fsync_benchmark","msg_id":2,"entries":100,"strategies":["always","batch_10ms","none"]}}
```

期望输出：

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

### 2. Single strategy 基准测试

Results should show 1 entry，包含strategy: "always"和data_loss_window: "0ms".

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"fsync_benchmark","msg_id":2,"entries":50,"strategies":["always"]}}
```

期望输出：

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

## 参考资料

- [PostgreSQL WAL Reliability](https://www.postgresql.org/docs/current/wal-reliability.html)：PostgreSQL documentation on WAL reliability, fsync,和data integrity

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
