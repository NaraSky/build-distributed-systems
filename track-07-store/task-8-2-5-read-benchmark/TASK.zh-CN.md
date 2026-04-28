# 混合负载下的读策略基准测试

英文标题：Benchmark Read Strategies Under Mixed Workload
网页：<https://builddistributedsystem.com/tracks/store/tasks/task-8-2-5-read-benchmark>

课程：7. 存储：线性一致键值存储
任务序号：10
短标题：Read Benchmark
难度：进阶
子主题：读优化

## 中文导读

这道题要求你对三种读策略进行基准测试，在 80% 读、20% 写的混合负载下，分别测量它们的吞吐量和延迟。通过实际数据对比，你能直观地感受到不同一致性级别对性能的影响，从而在实际系统设计中做出合理的权衡选择。

## 题目说明

在 80% 读、20% 写的混合负载下，对三种读策略进行基准测试，分别测量每种策略的吞吐量和延迟。

```json
Request:  {"type": "read_benchmark", "msg_id": 1, "read_pct": 80, "write_pct": 20, "total_ops": 1000, "strategies": ["linearizable", "lease", "follower"]}
Response: {"type": "read_benchmark_ok", "in_reply_to": 1, "results": [
    {"strategy": "linearizable", "throughput_ops": 2000, "p50_ms": 5, "p99_ms": 20, "consistency": "linearizable"},
    {"strategy": "lease", "throughput_ops": 8000, "p50_ms": 1, "p99_ms": 5, "consistency": "linearizable_if_clocks_correct"},
    {"strategy": "follower", "throughput_ops": 15000, "p50_ms": 0.5, "p99_ms": 2, "consistency": "bounded_staleness"}
]}
```

## 涉及概念

- `throughput benchmark`
- `read/write ratio`
- `latency comparison`
- `scalability`

## 实现提示

- 使用 80% 读、20% 写的工作负载进行测试（这是生产环境中常见的比例）
- 对比三种读策略：严格线性一致读、租约读、跟随者读
- 线性一致读延迟最高但一致性保证最强
- 跟随者读延迟最低但一致性保证较弱
- 分别测量每种策略的吞吐量（操作数/秒）和延迟（p50、p99）

## 测试用例

### 1. 对三种策略进行基准测试

验证结果包含 3 个条目，跟随者读应该具有最高的吞吐量和最低的延迟。

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

- [YCSB Benchmark](https://github.com/brianfrankcooper/YCSB)：Yahoo 云服务基准测试工具，用于数据库性能评估

## 本地文件

```text
src/main/java/Main.java
```

提交到网页时，主要提交上面这个 Java 文件的内容。
