# 基准测试 Read Strategies Under Mixed Workload

英文标题：Benchmark Read Strategies Under Mixed Workload
网页：<https://builddistributedsystem.com/tracks/store/tasks/task-8-2-5-read-benchmark>

课程：7. 存储：线性一致 KV Store
任务序号：10
短标题：Read 基准测试
难度：intermediate
子主题：Read Optimization

## 中文导读

本题要求你完成 `基准测试 Read Strategies Under Mixed Workload`。

重点关注：`throughput benchmark`、`read/write ratio`、`latency comparison`、`scalability`。

建议先按提示逐步实现：Test，包含80% reads, 20% writes workload (common in production)。

协议字段、消息类型、输入输出格式请以本文件中的代码块和测试用例为准。

## 题目说明

Benchmark three read strategies under an 80% read / 20% write workload. Measure throughput和latency用于each.

```JSON
请求:  {"type": "read_benchmark", "msg_id": 1, "read_pct": 80, "write_pct": 20, "total_ops": 1000, "strategies": ["线性一致", "lease", "Follower"]}
响应: {"type": "read_benchmark_ok", "in_reply_to": 1, "results": [
    {"strategy": "线性一致", "throughput_ops": 2000, "p50_ms": 5, "p99_ms": 20, "consistency": "线性一致"},
    {"strategy": "lease", "throughput_ops": 8000, "p50_ms": 1, "p99_ms": 5, "consistency": "linearizable_if_clocks_correct"},
    {"strategy": "Follower", "throughput_ops": 15000, "p50_ms": 0.5, "p99_ms": 2, "consistency": "bounded_staleness"}
]}
```

## 涉及概念

- `throughput benchmark`
- `read/write ratio`
- `latency comparison`
- `scalability`

## 实现提示

- Test，包含80% reads, 20% writes workload (common in production)
- Compare: strict 线性一致 reads vs lease reads vs Follower reads
- 线性一致 reads have highest latency but strongest guarantees
- Follower reads have lowest latency but weaker guarantees
- Measure throughput (ops/sec)和latency (p50, p99)用于each strategy

## 测试用例

### 1. 基准测试 all three strategies

Results should show 3 entries. Follower reads should have highest throughput和lowest latency.

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1","n2","n3"]}}
{"src":"c1","dest":"n1","body":{"type":"read_benchmark","msg_id":2,"read_pct":80,"write_pct":20,"total_ops":100,"strategies":["linearizable","lease","follower"]}}
```

期望输出：

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

## 参考资料

- [YCSB Benchmark](https://github.com/brianfrankcooper/YCSB)：Yahoo Cloud Serving Benchmark用于database performance evaluation

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
