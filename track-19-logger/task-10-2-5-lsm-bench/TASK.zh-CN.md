# 基准测试 LSM Tree vs B-Tree Performance

英文标题：Benchmark LSM Tree vs B-Tree Performance
网页：<https://builddistributedsystem.com/tracks/logger/tasks/task-10-2-5-lsm-bench>

课程：19. 日志器：WAL、LSM 与分布式日志
任务序号：10
短标题：LSM 基准测试
难度：intermediate
子主题：LSM Tree (日志-Structured Merge Tree)

## 中文导读

本题要求你完成 `基准测试 LSM Tree vs B-Tree Performance`。

重点关注：`write throughput`、`read latency`、`space amplification`、`Bloom filter impact`、`engine comparison`。

建议先按提示逐步实现：Measure write throughput: LSM trees excel at sequential inserts (append-only writes)。

协议字段、消息类型、输入输出格式请以本文件中的代码块和测试用例为准。

## 题目说明

The choice between LSM tree和B-Tree is one of the most important 存储 engine decisions. They represent fundamentally different tradeoffs:

**LSM Tree** (RocksDB, Cassandra, LevelDB):
- Writes are sequential (append to MemTable, flush to SSTable) -> very high write throughput
- Reads may need to check multiple levels -> higher read latency
- Space amplification > 1.0 (old versions exist until compaction)
- Write amplification is high (data rewritten during compaction)

**B-Tree** (PostgreSQL, MySQL InnoDB, SQLite):
- Writes are random I/O (in-place updates) -> lower write throughput
- Reads traverse a balanced tree (O(日志 N) disk reads) -> lower read latency
- Space amplification ~1.0 (in-place updates, no dead versions)
- Write amplification is lower

Benchmark both engines和measure: write ops/sec, read p50 latency,和space amplification.

```JSON
请求:  {"type": "lsm_benchmark", "msg_id": 1, "entries": 100000}
响应: {"type": "lsm_benchmark_ok", "in_reply_to": 1, "lsm": {"write_ops_sec": 200000, "read_p50_us": 50, "read_without_bloom_p50_us": 500, "space_amplification": 1.3}, "btree": {"write_ops_sec": 50000, "read_p50_us": 20, "space_amplification": 1.0}}
```

## 涉及概念

- `write throughput`
- `read latency`
- `space amplification`
- `Bloom filter impact`
- `engine comparison`

## 实现提示

- Measure write throughput: LSM trees excel at sequential inserts (append-only writes)
- Measure read latency，包含and without Bloom filter — the filter should dramatically reduce disk reads
- Space amplification = total bytes on disk / total bytes of unique data (LSM > 1.0 due to duplicate versions)
- Compare to a naive B-Tree: B-Trees have lower read latency but higher write latency (in-place updates)
- LSM wins用于write-heavy workloads; B-Tree wins用于read-heavy workloads

## 测试用例

### 1. Full 基准测试 comparison

lsm_benchmark_ok should include both lsm和btree results. LSM should have higher write_ops_sec, B-Tree should have lower read_p50_us.

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"lsm_benchmark","msg_id":2,"entries":1000}}
```

期望输出：

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

### 2. Bloom filter impact on reads

LSM read_p50_us should be significantly less than read_without_bloom_p50_us.

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"lsm_benchmark","msg_id":2,"entries":5000}}
```

期望输出：

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

## 参考资料

- [Designing Data-Intensive Applications](https://dataintensive.net/)：Martin Kleppmann Chapter 3: deep comparison of LSM vs B-Tree 存储 engine tradeoffs

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
