# 服务器吞吐量与延迟基准测试

英文标题：Benchmark Server Throughput and Latency
网页：<https://builddistributedsystem.com/tracks/networker/tasks/task-5-1-5-throughput-bench>

课程：17. 网络器：TCP 与协议基础
任务序号：5
短标题：吞吐量基准测试
难度：进阶
子主题：从零实现 TCP

## 中文导读

这道题让你为 TCP 服务器编写一个基准测试框架，测量服务器的吞吐量（每秒处理多少请求）和延迟的百分位数（p50、p95、p99），并分析性能瓶颈在哪里。这就像给服务器做一次"体检"，找出它最慢的环节，为后续优化提供方向。掌握基准测试的方法论，是进行任何性能调优的前提。

## 题目说明

测量你的 TCP 服务器的吞吐量（每秒请求数）和延迟（p50、p95、p99 百分位数），并分析瓶颈所在。

实现一个基准测试框架：

```json
Request:  {"type": "bench_run", "msg_id": 1, "num_requests": 1000, "payload_size_bytes": 64, "concurrency": 10}
Response: {"type": "bench_run_ok", "in_reply_to": 1, "throughput_rps": 5000, "latency_p50_us": 200, "latency_p95_us": 800, "latency_p99_us": 1500, "elapsed_ms": 200}

Request:  {"type": "bench_profile", "msg_id": 2, "num_requests": 100}
Response: {"type": "bench_profile_ok", "in_reply_to": 2, "breakdown": {
    "accept_pct": 5.2,
    "read_pct": 35.1,
    "process_pct": 12.3,
    "write_pct": 32.4,
    "overhead_pct": 15.0
}, "bottleneck": "read"}

Request:  {"type": "bench_sweep", "msg_id": 3, "concurrency_levels": [1, 5, 10, 50, 100]}
Response: {"type": "bench_sweep_ok", "in_reply_to": 3, "results": [
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

- 吞吐量 = 总请求数 / 总耗时（单位：请求/秒）
- 记录每个请求的延迟，然后排序计算百分位数
- p50 即中位数，p95 是第 95 百分位的延迟，p99 是第 99 百分位的延迟
- 分析瓶颈出在哪个环节：accept()、read() 还是处理逻辑
- 使用不同数量的并发连接运行测试，找到服务器的饱和点

## 测试用例

### 1. 运行基础基准测试

验证说明：bench_run_ok 应包含 throughput_rps 大于 0，且延迟字段满足 p50 <= p95 <= p99。

输入：

```json
{"src":"c0","dest":"n1","body":{"type":"init","msg_id":1,"node_id":"n1","node_ids":["n1"]}}
{"src":"c1","dest":"n1","body":{"type":"bench_run","msg_id":2,"num_requests":100,"payload_size_bytes":64,"concurrency":1}}
```

期望输出：

```text
{"src": "n1", "dest": "c0", "body": {"type": "init_ok", "in_reply_to": 1, "msg_id": 0}}
```

### 2. 性能分析各阶段耗时占比合计为 100%

验证说明：bench_profile_ok 中各阶段百分比之和应约等于 100。bottleneck 应为 accept、read、process、write 其中之一。

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

- [Latency Numbers Every Programmer Should Know](https://colin-scott.github.io/personal_website/research/interactive_latency.html)：各种系统操作延迟数据的交互式可视化展示

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
