# 基准测试 Server 吞吐量和延迟

英文标题：Benchmark Server Throughput和Latency
网页：<https://builddistributedsystem.com/tracks/networker/tasks/task-5-1-5-throughput-bench>

课程：17. 网络器：TCP 与协议基础
任务序号：5
短标题：吞吐量 基准测试
难度：intermediate
子主题：TCP From Scratch

## 中文导读

本题要求你完成 `基准测试 Server 吞吐量和延迟`。

重点关注：`throughput`、`latency percentiles`、`p50`、`p95`、`p99`。

建议先按提示逐步实现：Throughput = total requests / elapsed time (requests/sec)。

协议字段、消息类型、输入输出格式请以本文件中的代码块和测试用例为准。

## 题目说明

Measure your TCP 服务端's throughput (requests/sec)和latency (p50, p95, p99). Profile where the bottleneck is.

Implement a benchmark framework:

```JSON
请求:  {"type": "bench_run", "msg_id": 1, "num_requests": 1000, "payload_size_bytes": 64, "concurrency": 10}
响应: {"type": "bench_run_ok", "in_reply_to": 1, "throughput_rps": 5000, "latency_p50_us": 200, "latency_p95_us": 800, "latency_p99_us": 1500, "elapsed_ms": 200}

请求:  {"type": "bench_profile", "msg_id": 2, "num_requests": 100}
响应: {"type": "bench_profile_ok", "in_reply_to": 2, "breakdown": {
    "accept_pct": 5.2,
    "read_pct": 35.1,
    "process_pct": 12.3,
    "write_pct": 32.4,
    "overhead_pct": 15.0
}, "bottleneck": "read"}

请求:  {"type": "bench_sweep", "msg_id": 3, "concurrency_levels": [1, 5, 10, 50, 100]}
响应: {"type": "bench_sweep_ok", "in_reply_to": 3, "results": [
    {"concurrency": 1, "throughput_rps": 1000, "latency_p50_us": 1000},
    {"concurrency": 10, "throughput_rps": 5000, "latency_p50_us": 200}
]}
```

## 涉及概念

- `throughput`
- `latency percentiles`
- `p50`
- `p95`
- `p99`
- `profiling`
- `bottleneck`

## 实现提示

- Throughput = total requests / elapsed time (requests/sec)
- Measure latency用于each 请求, then sort to compute percentiles
- p50 = median, p95 = the latency at the 95th percentile, p99 = at 99th percentile
- Profile where the bottleneck is: accept(), read(), or processing
- Run，包含varying number of concurrent connections to find saturation point

## 测试用例

### 1. Run 基础 基准测试

bench_run_ok should include throughput_rps > 0,和latency fields p50 <= p95 <= p99.

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"bench_run","msg_id":2,"num_requests":100,"payload_size_bytes":64,"concurrency":1}}
```

期望输出：

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

### 2. Profile breakdown sums to 100%

bench_profile_ok breakdown percentages should sum to approximately 100. bottleneck should be one of: accept, read, process, write.

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"bench_profile","msg_id":2,"num_requests":50}}
```

期望输出：

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

## 参考资料

- [Latency Numbers Every Programmer Should Know](https://colin-scott.github.io/personal_website/research/interactive_latency.html)：Interactive visualization of latency numbers across different system operations

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
